import pygame
from PIL import Image
import math
import time
import enum
from Components import Component
from Components import ComponentTransform
from Components import ComponentSprite
from Components import ComponentCannon
from Components.Component import ComponentType
import GlobalVars
from Vector import Vec2

class ButtonType(enum.Enum):
    Scene = enum.auto()
    Button = enum.auto()
    Selectable = enum.auto()
    Exit = enum.auto()
    
    def Decode(value):
        members = list(vars(ButtonType).values())
        members = members[GlobalVars.membersOffset:len(members)-1]
        for member in members:
            if value == member.value:
                return member

class Button(Component.Component):
    def __init__(self, nPoly = 4, lenX = None, lenY = None, radius = 0.2, position = None, spritePath="data/ButtonLocked.png", onEscape = False, function = None):
        '''If lenX and lenY aren't specified, 2*radius is chosen for both sidelengths'''
        self.name = ComponentType.Button
        
        self.nPoly = nPoly
        self.lenX = lenX if lenX is not None else radius * 2
        self.lenY = lenY if lenY is not None else radius * 2
        self.initPos = position
        self.animDuration = 0.2
        self.animScale = 0.1
        self.animate = False
        self.buttonType = ButtonType.Button
        self.spritePath = spritePath
        self.onEscape = onEscape
        self.function = function
        
    def Start(self):
        self.transform = self.parent.GetComponent(ComponentType.Transform)
        self.transform.position = self.initPos if self.initPos is not None else self.transform.position
        self.verts = self.GetVertices()
        
        self.parent.AddComponent(ComponentSprite.SpriteUI(self.spritePath, lenX=self.lenX, lenY=self.lenY))
        
    def Update(self, deltaTime):
        self.verts = self.GetVertices()
        # self.DisplayButtonOutline((220,20,220))
        self.CheckClick()
        if self.animate:
            self.Animate()
        # camera = self.parent.GetParentScene().camera
        # self.cameraScale = camera.scale
        # self.parent.GetComponent(ComponentType.Transform).position = self.parent.GetComponent(ComponentType.Transform).position / self.cameraScale

    def CheckClick(self):
        if self.onEscape and GlobalVars.escapeKey:
            self.OnClick()
        if GlobalVars.mouseLeft:
            mousePosWorld = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen,self.parent.GetParentScene().camera)
            if self.PointInPolygon(mousePosWorld):
                self.OnClick()
    
    def OnClick(self):
        '''To use animation, super() this function'''
        self.clickStart = time.time()
        self.animate = True
        if self.function is not None:
            self.function()
        
    def EndOfClick(self):
        pass
    
    def CubicEase(self,x):
        return 4*math.pow(x,3) if x < 0.5 else 1 - math.pow(-2 * x + 2, 3)/2.0
    
    def Cubic(self,x):
        return x**3
    
    def EaseOutQuint(self,x):
        return 1 - math.pow(1 - x, 6)
    
    def Animate(self):
        t = (time.time()-self.clickStart)/self.animDuration
        if t > 1:
            self.animate = False
            self.transform.scale = Vec2(1,1)
            self.EndOfClick()
            return
        self.transform.scale.Normalize()
        self.transform.scale *= 1 + self.animScale * math.sin(math.pi * self.EaseOutQuint(t))
        
    def PointInPolygon(self,point):
        inside = True
        for i in range(self.nPoly):
            A = self.verts[i]
            B = self.verts[(i+1)%self.nPoly]
            normal = (B-A).Perp()
            AP = point-A
            if normal.Dot(AP) < 0:
                inside = False
        return inside
    
    def GetVertices(self):
        verts = list()
        deltaPhi = 2*math.pi/self.nPoly
        for i in range(self.nPoly):
            verts.append(self.transform.position + Vec2(math.cos(deltaPhi*i+deltaPhi/2.0)*self.transform.scale.x*self.lenX/2.0, math.sin(deltaPhi*i+deltaPhi/2.0)*self.transform.scale.y*self.lenY/2.0))
        return verts
    
    def DisplayButtonOutline(self, color):
        vertices = []
        for v in self.verts:
            vertScreen = ComponentTransform.Transform.WorldToScreenPos(v,self.parent.GetParentScene().camera)
            vertices.append((vertScreen.x,vertScreen.y))
        pygame.draw.polygon(GlobalVars.UILayer,color,vertices,1)
    
    def Decode(self, obj):
        super().Decode(obj)
        self.nPoly = obj["nPoly"]
        self.lenX = obj["lenX"]
        self.lenY = obj["lenY"]
        self.animate = obj["animate"]
        self.animDuration = obj["animDuration"]
        self.animScale = obj["animScale"]
        self.initPos = Vec2.FromList(obj["initPos"])
        self.buttonType = ButtonType.Decode(obj["buttonType"])
        self.onEscape = obj["onEscape"]
        
class ButtonScene(Button):
    def __init__(self, nPoly=4, lenX = None, lenY = None, radius = 0.2, position=Vec2(0, 0), spritePath="data/ButtonLocked.png", scenePath = None, setupFunc = None, sceneName = None, onEscape = False, number = None):
        '''Since the setup func cannot be saved, it can only be used on scenes that don't get saved, e.g. the main menu, the editor, level select. To return back to the editor, level select or main menu from a saved level, only the sceneName should be assigned.'''
        super().__init__(nPoly, lenX, lenY, radius, position, spritePath, onEscape)
        self.scenePath = scenePath
        self.setupFunc = setupFunc
        self.sceneName = sceneName
        self.buttonType = ButtonType.Scene
        self.number = number
        
    def Start(self):
        self.transform = self.parent.GetComponent(ComponentType.Transform)
        self.transform.position = self.initPos
        self.verts = self.GetVertices()
        
        self.parent.AddComponent(ComponentSprite.SpriteUI(self.spritePath, lenX=self.lenX, lenY=self.lenY, number=self.number))
    
    def EndOfClick(self):
        import Scene
        scene = Scene.Scene()
        if self.scenePath is not None:
            scene.FromJSON(self.scenePath)
            self.sceneName = scene.name
            
            world = self.parent.GetParentScene().world
            world.AddScene(scene)
            world.SetActiveScene(scene.name)
        else:
            # loads scenes that cannot be saved to JSON. Since the setup func cannot be saved, it can only be used on scenes that don't get saved, i.e. the main menu, the editor etc. To return back to the editor, level select or main menu from a saved level, only the sceneName should be assigned
            if self.setupFunc is not None:
                self.setupFunc(self.parent.GetParentScene().world)
            self.parent.GetParentScene().world.SetActiveScene(self.sceneName)
        
    def Decode(self, obj):
        super().Decode(obj)
        self.scenePath = obj["scenePath"]
        self.sceneName = obj["sceneName"]
        
class ButtonSelectable(Button):
    def __init__(self, nPoly=4, lenX=None, lenY=None, radius=0.2, position=Vec2(0, 0), spritePath="data/ButtonLocked.png", editor = None, componentInit = None, onEscape = False):
        super().__init__(nPoly, lenX, lenY, radius, position, spritePath, onEscape)
        self.buttonType = ButtonType.Selectable
        self.editor = editor
        self.componentInit = componentInit
        
    def Start(self):
        super().Start()
        self.CreateButtonSprite()
        
    def EndOfClick(self):
        self.editor.SelectType(self.componentInit)
        
    def Decode(self, obj):
        super().Decode(obj)
        self.editorID = obj["editor"]
        
    def CreateButtonSprite(self):
        canvas = pygame.Surface((150,150), pygame.SRCALPHA, 32)
        canvas = canvas.convert_alpha()
        
        width = canvas.get_width()
        height = canvas.get_height()
        imgScale = 0.8
        
        image = pygame.transform.scale(pygame.image.load("Bouncy-Balls/data/ButtonSelectableBackground.png"), (width,height))
        canvas.blit(image, (0,0))
        
        if self.componentInit is not None:
            comp = self.componentInit()
            compLen = Vec2(comp.lenX,comp.lenY)
            compLen = compLen/comp.lenX if comp.lenX > comp.lenY else compLen/comp.lenY
            topLeft = (width * (1 - compLen.x * imgScale)/2.0, height * (1 - compLen.y * imgScale)/2.0)
            sprite = pygame.image.load("Bouncy-Balls/" + self.spritePath)
            image = pygame.transform.scale(sprite, (width * compLen.x * imgScale, height * compLen.y * imgScale))
            canvas.blit(image, topLeft)
        
        imageData = pygame.image.tobytes(canvas, 'RGBA')
        img = Image.frombytes('RGBA', (width,height), imageData)
        img.save("Bouncy-Balls/data/" + self.spritePath[:-4] + "Button.png",'PNG')
        
        self.parent.AddComponent(ComponentSprite.SpriteUI("data/" + self.spritePath[:-4] + "Button.png", lenX=self.lenX, lenY=self.lenY))
        
class ButtonBall(Button):
    def __init__(self, nPoly=4, lenX=None, lenY=None, radius=0.2, position=Vec2(0, 0), spritePath="data/ButtonLocked.png", onEscape = False, ballType = None):
        super().__init__(nPoly, lenX, lenY, radius, position, spritePath, onEscape)
        self.buttonType = ButtonType.Selectable
        self.ballType = ballType
        
    def Start(self):
        super().Start()
        self.parent.AddComponent(ComponentSprite.SpriteUI(self.spritePath, lenX=self.lenX, lenY=self.lenY))
        
    def EndOfClick(self):
        cannon = self.parent.GetParentScene().GetObjectsWithComponent(ComponentType.Cannon)[0]
        cannon.GetComponent(ComponentType.Cannon).SelectBall(self.ballType)
        # ball = self.parent.GetParentScene().GetObjectsWithComponent(ComponentType.Ball)
        # ball.AddComponent()
        
    def Decode(self, obj):
        super().Decode(obj)
        self.editorID = obj["editor"]
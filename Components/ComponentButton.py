import pygame
from PIL import Image
import math
import time
import enum
from Components import Component
from Components import ComponentTransform
from Components import ComponentSprite
from Components.Component import ComponentType
from lib import GlobalVars
from Vector import Vec2

class ButtonType(enum.Enum):
    Level = enum.auto()
    Button = enum.auto()
    Selectable = enum.auto()
    
    def Decode(value):
        members = list(vars(ButtonType).values())
        members = members[8:len(members)-1]
        for member in members:
            if value == member.value:
                return member

class Button(Component.Component):
    def __init__(self, nPoly = 4, lenX = None, lenY = None, radius = 0.2, position = Vec2(0,0), spritePath="data/ButtonLocked.png"):
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
        
    def Start(self):
        self.transform = self.parent.GetComponent(ComponentType.Transform)
        self.transform.position = self.initPos
        self.verts = self.GetVertices()
        
        self.parent.AddComponent(ComponentSprite.Sprite(self.spritePath, lenX=self.lenX, lenY=self.lenY))
        
    def Update(self, deltaTime):
        self.verts = self.GetVertices()
        # self.DisplayButtonOutline((220,20,220))
        self.CheckClick()
        if self.animate:
            self.Animate()

    def CheckClick(self):
        if GlobalVars.mouseLeft:
            mousePosWorld = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen,self.parent.GetParentScene().camera)
            if self.PointInPolygon(mousePosWorld):
                self.OnClick()
    
    def OnClick(self):
        '''To use animation, super() this function'''
        self.clickStart = time.time()
        self.animate = True
        
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
            self.transform.scale = 1
            self.EndOfClick()
            return
        self.transform.scale = 1 + self.animScale * math.sin(math.pi * self.EaseOutQuint(t))
        
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
            verts.append(self.transform.position + Vec2(math.cos(deltaPhi*i+deltaPhi/2.0)*self.lenX/2.0, math.sin(deltaPhi*i+deltaPhi/2.0)*self.lenY/2.0))
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
        
class ButtonLevel(Button):
    def __init__(self, nPoly=4, lenX = None, lenY = None, radius = 0.2, position=Vec2(0, 0), spritePath="data/ButtonLocked.png", scenePath = None):
        super().__init__(nPoly, lenX, lenY, radius, position, spritePath)
        self.scenePath = scenePath
        self.buttonType = ButtonType.Level
        
    def EndOfClick(self):
        import Scene
        scene = Scene.Scene()
        try:
            scene.FromJSON(self.scenePath)
            self.sceneName = scene.name
            
            world = self.parent.GetParentScene().world
            world.AddScene(scene)
            world.SetActiveScene(scene.name)
        except:
            pass
        
    def Decode(self, obj):
        super().Decode(obj)
        self.scenePath = obj["scenePath"]
        
class ButtonSelectable(Button):
    def __init__(self, nPoly=4, lenX=None, lenY=None, radius=0.2, position=Vec2(0, 0), spritePath="data/ButtonLocked.png", editor = None, componentInit = None):
        super().__init__(nPoly, lenX, lenY, radius, position, spritePath)
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
        
        image = pygame.transform.scale(pygame.image.load("Bouncy-Balls/data/ButtonSelectableBackground.png"), (width,height))
        canvas.blit(image, (0,0))
        
        comp = self.componentInit()
        topLeft = (width * (1-comp.lenX* 0.9)/2.0, height * (1-comp.lenY* 0.9)/2.0)
        sprite = pygame.image.load("Bouncy-Balls/" + self.spritePath)
        image = pygame.transform.scale(sprite, (width * comp.lenX * 0.9, height * comp.lenY * 0.9))
        canvas.blit(image, topLeft)
        
        imageData = pygame.image.tobytes(canvas, 'RGBA')
        img = Image.frombytes('RGBA', (width,height), imageData)
        img.save("Bouncy-Balls/data/" + self.spritePath[:-4] + "Button.png",'PNG')
        
        self.parent.AddComponent(ComponentSprite.Sprite("data/" + self.spritePath[:-4] + "Button.png", lenX=self.lenX, lenY=self.lenY))
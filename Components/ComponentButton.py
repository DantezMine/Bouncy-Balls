import pygame
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
    
    def Decode(value):
        members = list(vars(ButtonType).values())
        members = members[8:len(members)-1]
        for member in members:
            if value == member.value:
                return member

class Button(Component.Component):
    def __init__(self, nPoly = 4, radius = 0.2, position = Vec2(0,0)):
        self.name = ComponentType.Button
        
        self.nPoly = nPoly
        self.radius = radius
        self.initPos = position
        self.animDuration = 0.4
        self.animScale = 0.1
        self.animate = False
        self.buttonType = ButtonType.Button
        
    def Start(self):
        self.transform = self.parent.GetComponent(ComponentType.Transform)
        self.transform.position = self.initPos
        self.verts = self.GetVertices()
        
        self.parent.AddComponent(ComponentSprite.Sprite(spritePath="data/ButtonLocked.png",diameter=self.radius))
        
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
    
    def CubicEase(self,x):
        return 4*math.pow(x,3) if x < 0.5 else 1 - math.pow(-2 * x + 2, 3)/2.0
    
    def Animate(self):
        t = (time.time()-self.clickStart)/self.animDuration
        if t > 1:
            self.animate = False
            self.transform.scale = 1
            return
        self.transform.scale = 1 + self.animScale * math.sin(math.pi * self.CubicEase(t))
        
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
            verts.append(self.transform.position + Vec2(math.cos(deltaPhi*i+deltaPhi/2.0), math.sin(deltaPhi*i+deltaPhi/2.0)) * self.radius)
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
        self.radius = obj["radius"]
        self.animate = obj["animate"]
        self.animDuration = obj["animDuration"]
        self.animScale = obj["animScale"]
        self.initPos = Vec2.FromList(obj["initPos"])
        self.buttonType = ButtonType.Decode(obj["buttonType"])
        
class ButtonLevel(Button):
    def __init__(self, nPoly=4, radius=0.2, position=Vec2(0, 0), scenePath = None):
        super().__init__(nPoly, radius, position)
        self.scenePath = scenePath
        self.buttonType = ButtonType.Level
        
    def OnClick(self):
        import Scene
        super().OnClick()
        scene = Scene.Scene()
        scene.FromJSON(self.scenePath)
        self.sceneName = scene.name
        
        world = self.parent.GetParentScene().world
        world.AddScene(scene)
        world.SetActiveScene(scene.name)
        
    def Decode(self, obj):
        super().Decode(obj)
        self.scenePath = obj["scenePath"]
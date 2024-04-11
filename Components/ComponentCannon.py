from Components import ComponentTransform
from Components import ComponentSprite
from Components import Component
from Components.Component import Components
from Vector import Vec2
from lib import GlobalVars
import pygame
import math

class Cannon(Component.Component):
    def __init__(self, position = Vec2(0,0)):
        self.name = Components.Cannon
        self.parent = None
        self.initPos = position
        
    def Start(self):
        self.transform = self.parent.GetComponent(Components.Transform)
        self.transform.position = self.initPos
        self.parent.AddComponent(ComponentSprite.Sprite("data/WoodStructure.png", 0.7, 0.2))
        # self.parent.AddComponent(Base(self.initPos + self.baseOffset))
    
    def Update(self, deltaTime):
        mousePosWorld = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen, self.parent.GetParentScene().camera)
        if GlobalVars.mouseLeft:
            delta = mousePosWorld - self.initPos
            self.transform.rotation = math.atan(float(delta.y)/delta.x)
                
    def Encode(self, obj):
        outDict = super().Encode(obj)
        outDict["initPos"] = self.initPos
        return outDict
    
class Base(Component.Component):
    def __init__(self, position=Vec2(0, 0)):
        self.name = Components.Cannon
        self.parent = None
        self.initPos = position + Vec2(0, 50)
        
    def Start(self):
        transform = self.parent.GetComponent(Components.Transform)
        transform.position = self.initPos
        transform.rotation = math.pi/2
        self.parent.AddComponent(ComponentSprite.Sprite("data/StructureMetal.png", 0.7, 0.2))
from Components.Component import ComponentType
from Components import ComponentTransform
from Components import ComponentSprite
from Components import Component
import GameObject
from Vector import Vec2
import GlobalVars
import pygame
import math

class Cannon(Component.Component):
    def __init__(self, position = Vec2(0,0), cannonScale = 1, rotation = 0):
        self.name = ComponentType.Cannon
        self.parent = None
        self.initPos = position
        self.rotation = rotation
        self.mousePressed = False
        self.mouseLeft = False
        self.cannonScale = 2
        
    def Start(self):
        transform = self.parent.GetComponent(ComponentType.Transform)
        transform.position = self.initPos
        self.parent.AddComponent(ComponentSprite.Sprite("data/Barrel.png", self.cannonScale*0.580, self.cannonScale*0.402))
        # self.parent.AddComponent(Base(self.initPos + self.baseOffset))
        
        scene = self.parent.GetParentScene()
        #only create base if it doesn't exist in the scene yet
        if len(scene.GetComponents(ComponentType.Base)) == 0:
            cannonBase = GameObject.GameObject(scene)
            cannonBase.AddComponent(Base(Vec2(-1,-0.95)))
            scene.AddGameObject(cannonBase)
    
    def Update(self, deltaTime):
        transform = self.parent.GetComponent(ComponentType.Transform)
        mousePos = pygame.mouse.get_pos()
        mousePos = Vec2(mousePos[0],mousePos[1])
        mousePosWorld = ComponentTransform.Transform.ScreenToWorldPos(mousePos, self.parent.GetParentScene().camera)
        for event in GlobalVars.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mousePressed = True
                if event.button == 1:
                    self.mouseLeft = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mousePressed = False
                self.mouseLeft = False
                    
        if self.mousePressed:
            if self.mouseLeft:
                delta = mousePosWorld - self.initPos
                self.rotation = math.atan(float(delta.y)/float(delta.x)) - 0.35
                if delta.x > 0:
                    self.rotation += math.pi
                transform.rotation = self.rotation
                
    def Decode(self, obj):
        super().Decode(obj)
        self.rotation = obj["rotation"]
        self.mousePressed = obj["mousePressed"]
        self.mouseLeft = obj["mouseLeft"]
        self.cannonScale = obj["cannonScale"]
        self.initPos = Vec2.FromList(obj["initPos"])
    
class Base(Component.Component):
    def __init__(self, position=Vec2(0, 0), baseScale=1):
        self.name = ComponentType.Base
        self.parent = None
        self.initPos = position
        self.baseScale = 2
        
    def Start(self):
        self.initPos += Vec2(self.baseScale*-0.1, self.baseScale*-0.15)
        transform = self.parent.GetComponent(ComponentType.Transform)
        transform.position = self.initPos
        self.parent.AddComponent(ComponentSprite.Sprite("data/Base.png", self.baseScale*0.615, self.baseScale*0.345))
        
    def Decode(self, obj):
        super().Decode(obj)
        self.baseScale = obj["baseScale"]
        self.initPos = Vec2.FromList(obj["initPos"])
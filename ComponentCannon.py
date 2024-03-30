import ComponentSprite
import Component
from Component import Components
from Vector import Vec2
from lib import GlobalVars
import pygame
import math

class Cannon(Component.Component):
    def __init__(self, position = Vec2(0,0)):
        self.name = Components.Cannon
        self.parent = None
        self.initPos = position
        self.baseOffset = Vec2(0, 50)
        self.rotation = 0

    def Start(self):
        self.transform = self.parent.GetComponent(Components.Transform)
        self.transform.position = self.initPos
        self.parent.AddComponent(ComponentSprite.Sprite("data/WoodStructure.png", 150, 30))
        # self.parent.AddComponent(Base(self.initPos + self.baseOffset))
    
    def Update(self, deltaTime):
        mousePressed = False
        mouseLeft = False
        mousePos = Vec2(0,0)
        for event in GlobalVars.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = True
                mousePos = Vec2(event.pos[0],event.pos[1])
                if event.button == 1:
                    mouseLeft = True
                    
        if mousePressed:
            if mouseLeft:
                delta = mousePos - self.initPos
                self.rotation = math.atan(float(delta.y)/delta.x)
                print(delta, self.rotation)
                self.transform.rotation = self.rotation
    
class Base(Component.Component):
    def __init__(self, position=Vec2(0, 0)):
        self.name = Components.Cannon
        self.parent = None
        self.initPos = position
        
    def Start(self):
        transform = self.parent.GetComponent(Components.Transform)
        transform.position = self.initPos
        transform.rotation = math.pi/2
        self.parent.AddComponent(ComponentSprite.Sprite("data/MetalStructure.png", 150, 30))
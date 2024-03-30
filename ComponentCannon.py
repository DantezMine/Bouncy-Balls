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
        self.rotation = 0
        self.mousePressed = False
        self.mouseLeft = False
        
    def Start(self):
        self.transform = self.parent.GetComponent(Components.Transform)
        self.transform.position = self.initPos
        self.parent.AddComponent(ComponentSprite.Sprite("data/WoodStructure.png", 150, 30))
        # self.parent.AddComponent(Base(self.initPos + self.baseOffset))
    
    def Update(self, deltaTime):
        mousePos = pygame.mouse.get_pos()
        mousePos = Vec2(mousePos[0],mousePos[1])
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
                delta = mousePos - self.initPos
                self.rotation = math.atan(float(delta.y)/delta.x)
                print(delta, self.rotation)
                self.transform.rotation = self.rotation
    
class Base(Component.Component):
    def __init__(self, position=Vec2(0, 0)):
        self.name = Components.Cannon
        self.parent = None
        self.initPos = position + Vec2(0, 50)
        
    def Start(self):
        transform = self.parent.GetComponent(Components.Transform)
        transform.position = self.initPos
        transform.rotation = math.pi/2
        self.parent.AddComponent(ComponentSprite.Sprite("data/MetalStructure.png", 150, 30))
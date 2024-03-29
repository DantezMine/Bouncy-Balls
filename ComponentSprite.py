import math
import Component
from Component import Components
from Vector import Vec2
import pygame
from lib import GlobalVars

class Sprite(Component.Component):
    def __init__(self, spritePath = None, lenX = 50, lenY = 50, diameter = None): #s_spritePath must be given
        self.name = Components.Sprite
        self.spritePath = spritePath
        self.parent = None
        self.lenX = diameter if diameter is not None else lenX
        self.lenY = diameter if diameter is not None else lenY
        
    def Update(self,deltaTime):
        self.DisplayImg()
    
    def DisplayImg(self):
        parentTransform = self.parent.GetComponent(Components.Transform)
        sprite = pygame.image.load("Bouncy-Balls/"+self.spritePath)
        
        topLeft = (parentTransform.position-Vec2(self.lenX,self.lenY)*(parentTransform.scale/2.0)).Rotate(parentTransform.rotation)
        rect = (topLeft.x,topLeft.y)
        image = pygame.transform.rotate(pygame.transform.scale(sprite,(self.lenX*parentTransform.scale,self.lenY*parentTransform.scale)),parentTransform.rotation)
        
        GlobalVars.screen.blit(image,rect)
        
    def Encode(self,obj):
        outDict = super(Sprite,self).Encode(obj)
        outDict["spritePath"] = obj.spritePath
        outDict["lenX"] = obj.lenX
        outDict["lenY"] = obj.lenY
        return outDict
import math
from Components import Component
from Components.Component import Components
from Vector import Vec2
import pygame
from lib import GlobalVars

class Sprite(Component.Component):
    def __init__(self, spritePath = None, lenX = 0.5, lenY = 0.5, diameter = None): #s_spritePath must be given
        self.name = Components.Sprite
        self.spritePath = spritePath
        self.parent = None
        self.lenX = diameter if diameter is not None else lenX
        self.lenY = diameter if diameter is not None else lenY
        self.sprite = pygame.image.load("Bouncy-Balls/"+self.spritePath)
        
    def Update(self,deltaTime):
        self.DisplayImg()
    
    def DisplayImg(self):
        sceneCam = self.parent.GetParentScene().camera
        parentTransform = self.parent.GetComponent(Components.Transform)
        width = GlobalVars.screen.get_width()
        height = GlobalVars.screen.get_height()
        
        #World Space
        topLeft = (Vec2(self.lenX,-self.lenY)*(parentTransform.scale/2.0)).Rotate(parentTransform.rotation)
        botLeft = (Vec2(self.lenX, self.lenY)*(parentTransform.scale/2.0)).Rotate(parentTransform.rotation)
        #get extrems of AABB
        dx = max(abs(topLeft.x),abs(botLeft.x))
        dy = max(abs(topLeft.y),abs(botLeft.y))
        xWorld = parentTransform.position.x-dx
        yWorld = parentTransform.position.y+dy
        
        #Screen Space
        vScreen = parentTransform.WorldToScreenPos(Vec2(xWorld,yWorld), sceneCam)
        xScreen = vScreen.x
        yScreen = vScreen.y
        screenScale = Vec2(self.lenX*width,self.lenY*height) * (parentTransform.scale * sceneCam.scale / 2.0)
                
        image = pygame.transform.scale(self.sprite,(screenScale.x,screenScale.y))
        image = pygame.transform.rotate(image,parentTransform.rotation*180.0/math.pi)
        
        GlobalVars.foreground.blit(image,(xScreen,yScreen))
        
    def Encode(self,obj):
        outDict = super(Sprite,self).Encode(obj)
        outDict["spritePath"] = obj.spritePath
        outDict["lenX"] = obj.lenX
        outDict["lenY"] = obj.lenY
        return outDict
    
class SpriteBackground(Sprite):
    def DisplayImg(self):
        width = GlobalVars.background.get_width()
        height = GlobalVars.background.get_height()
        image = pygame.transform.scale(self.sprite,(width,height))
        GlobalVars.background.blit(image,(0,0))
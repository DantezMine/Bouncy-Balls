import math
from Components import Component
from Components import ComponentTransform
from Components.Component import ComponentType
from Vector import Vec2
import pygame
import GlobalVars
import enum

class SpriteType(enum.Enum):
    Sprite = enum.auto()
    Background = enum.auto()
    UI = enum.auto()
    
    def Decode(value):
        members = list(vars(SpriteType).values())
        members = members[8:len(members)-1]
        for member in members:
            if value == member.value:
                return member

class Sprite(Component.Component):
    def __init__(self, spritePath = None, lenX = 0.5, lenY = 0.5, diameter = None): #s_spritePath must be given
        self.name = ComponentType.Sprite
        self.spritePath = spritePath
        self.parent = None
        self.lenX = diameter*math.sqrt(2) if diameter is not None else lenX
        self.lenY = diameter*math.sqrt(2) if diameter is not None else lenY
        self.spriteType = SpriteType.Sprite
        
    def Start(self):
        self.sprite = pygame.image.load("Bouncy-Balls/"+self.spritePath)
        
    def Update(self,deltaTime):
        self.DisplayImg()
    
    def DisplayImg(self):
        sceneCam = self.parent.GetParentScene().camera
        parentTransform = self.parent.GetComponent(ComponentType.Transform)
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
        vScreen = ComponentTransform.Transform.WorldToScreenPos(Vec2(xWorld,yWorld), sceneCam)
        xScreen = vScreen.x
        yScreen = vScreen.y
        screenScale = Vec2(self.lenX*width,self.lenY*height) * (parentTransform.scale * sceneCam.scale / 2.0)
                
        image = pygame.transform.scale(self.sprite,(screenScale.x,screenScale.y))
        image = pygame.transform.rotate(image,parentTransform.rotation*180.0/math.pi)
        self.BlitImage(image,(xScreen,yScreen))
        
    def BlitImage(self, image, coord):
        GlobalVars.foreground.blit(image, coord)
    
    def Decode(self, obj):
        super().Decode(obj)
        self.spritePath = obj["spritePath"]
        self.spriteType = SpriteType.Decode(obj["spriteType"])
        self.lenX = obj["lenX"]
        self.lenY = obj["lenY"]
    
class SpriteBackground(Sprite):
    def __init__(self, spritePath=None, lenX=0.5, lenY=0.5, diameter=None):
        super().__init__(spritePath, lenX, lenY, diameter)
        self.spriteType = SpriteType.Background
    
    def DisplayImg(self):
        width = GlobalVars.background.get_width()
        height = GlobalVars.background.get_height()
        image = pygame.transform.scale(self.sprite,(width,height))
        GlobalVars.background.blit(image,(0,0))
        
class SpriteUI(Sprite):
    def __init__(self, spritePath=None, lenX=0.5, lenY=0.5, diameter=None):
        super().__init__(spritePath, lenX, lenY, diameter)
        self.spriteType = SpriteType.UI
        
    def BlitImage(self, image, coord):
        GlobalVars.UILayer.blit(image, coord)
        
class SpriteGizmo(Sprite):
    def __init__(self, lenX=0.5, lenY=0.5, diameter=None, targetID = None):
        super().__init__(None, lenX, lenY, diameter)
        self.gizmoVal = 0
        self.targetID = targetID
        self.spritePaths = ("data/GizmoEditor.png","data/GizmoEditorSquare.png","data/GizmoEditorCircle.png","data/GizmoEditorArrowX.png","data/GizmoEditorArrowY.png")
        
    def Start(self):
        self.sprites = [None] * len(self.spritePaths)
        for i in range(len(self.spritePaths)):
            self.sprites[i] = pygame.image.load("Bouncy-Balls/"+self.spritePaths[i])
        
    def DisplayImg(self):
        if self.targetID is None:
            return
        sceneCam = self.parent.GetParentScene().camera
        targetTransform = self.parent.GetParentScene().GameObjectWithID(self.targetID).GetComponent(ComponentType.Transform)
        width = GlobalVars.screen.get_width()
        height = GlobalVars.screen.get_height()
        
        #World Space
        topLeft = (Vec2(self.lenX,-self.lenY)/(sceneCam.scale*2.0)).Rotate(targetTransform.rotation)
        botLeft = (Vec2(self.lenX, self.lenY)/(sceneCam.scale*2.0)).Rotate(targetTransform.rotation)
        #get extrems of AABB
        dx = max(abs(topLeft.x),abs(botLeft.x))
        dy = max(abs(topLeft.y),abs(botLeft.y))
        xWorld = targetTransform.position.x-dx
        yWorld = targetTransform.position.y+dy
        
        #Screen Space
        vScreen = ComponentTransform.Transform.WorldToScreenPos(Vec2(xWorld,yWorld), sceneCam)
        xScreen = vScreen.x
        yScreen = vScreen.y
        screenScale = Vec2(self.lenX*width,self.lenY*height)/ 2.0
                
        image = pygame.transform.scale(self.sprites[self.gizmoVal],(screenScale.x,screenScale.y))
        self.BlitImage(image,(xScreen,yScreen))
        
    def BlitImage(self, image, coord):
        GlobalVars.UILayer.blit(image, coord)
    
    def Decode(self, obj):
        super().Decode(obj)
        self.gizmoVal = obj["gizmoVal"]
        self.targetID = obj["targetID"]
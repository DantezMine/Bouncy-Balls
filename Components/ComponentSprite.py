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
    Gizmo = enum.auto()
    
    def Decode(value):
        members = list(vars(SpriteType).values())
        members = members[GlobalVars.membersOffset:len(members)-1]
        for member in members:
            if value == member.value:
                return member

class Sprite(Component.Component):
    def __init__(self, spritePath = None, lenX = 0.5, lenY = 0.5, diameter = None): #s_spritePath must be given
        self.name = ComponentType.Sprite
        self.parent = None
        self.spriteType = SpriteType.Sprite
        self.spritePath = spritePath
        self.lenX = diameter*math.sqrt(2) if diameter is not None else lenX
        self.lenY = diameter*math.sqrt(2) if diameter is not None else lenY
        self.draw = True
        self.sprite = None
        
    def Start(self):
        if self.spritePath is not None:
            self.sprite = pygame.image.load("Bouncy-Balls/"+self.spritePath)
        
    def Update(self,deltaTime):
        self.DisplayImg()
    
    def DisplayImg(self):
        sceneCam = self.parent.GetParentScene().camera
        parentTransform = self.parent.GetComponent(ComponentType.Transform)
        width = GlobalVars.screen.get_width()
        height = GlobalVars.screen.get_height()
        
        #World Space
        topLeft = (Vec2(self.lenX*parentTransform.scale.x,-self.lenY*parentTransform.scale.y)/2.0).Rotate(parentTransform.rotation)
        botLeft = (Vec2(self.lenX*parentTransform.scale.x, self.lenY*parentTransform.scale.y)/2.0).Rotate(parentTransform.rotation)
        #get extremes of AABB
        dx = max(abs(topLeft.x),abs(botLeft.x))
        dy = max(abs(topLeft.y),abs(botLeft.y))
        xWorld = parentTransform.position.x-dx
        yWorld = parentTransform.position.y+dy

        #Screen Space
        vScreen = ComponentTransform.Transform.WorldToScreenPos(Vec2(xWorld,yWorld), sceneCam)
        xScreen = vScreen.x
        yScreen = vScreen.y
        screenScale = Vec2(self.lenX*width*parentTransform.scale.x,self.lenY*height*parentTransform.scale.y) * (sceneCam.scale / 2.0)

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
    def __init__(self, spritePath=None, lenX=0.5, lenY=0.5, diameter=None, scale = 1):
        super().__init__(spritePath, lenX, lenY, diameter)
        self.spriteType = SpriteType.Background
        self.scale = scale
    
    def Update(self, deltaTime):
        if self.parent.GetParentScene().GetObjectsWithComponent(ComponentType.Cannon) == []:
            self.scale = 1
        camera = self.parent.GetParentScene().camera
        pos = self.parent.GetComponent(ComponentType.Transform).position + camera.parent.GetComponent(ComponentType.Transform).position * 5
        self.DisplayImg(pos)
    
    def DisplayImg(self, pos):
        width = GlobalVars.background.get_width() * self.scale
        height = GlobalVars.background.get_height() * self.scale
        image = pygame.transform.scale(self.sprite,(width,height))
        GlobalVars.background.blit(image,(-pos.x,pos.y))
        
class SpriteUI(Sprite):
    def __init__(self, spritePath=None, lenX=0.5, lenY=0.5, diameter = None, number = None):
        super().__init__(spritePath, lenX, lenY, diameter)
        self.spriteType = SpriteType.UI
        self.number = number
        self.numbers = pygame.image.load("Bouncy-Balls/data/NumberImages.png") if number is not None else None
        
    def DisplayImg(self):
        parentTransform = self.parent.GetComponent(ComponentType.Transform)
        width = GlobalVars.screen.get_width()
        height = GlobalVars.screen.get_height()
        
        #World Space
        topLeft = (Vec2(self.lenX*parentTransform.scale.x,-self.lenY*parentTransform.scale.y)/2.0).Rotate(parentTransform.rotation)
        botLeft = (Vec2(self.lenX*parentTransform.scale.x, self.lenY*parentTransform.scale.y)/2.0).Rotate(parentTransform.rotation)
        #get extremes of AABB
        dx = max(abs(topLeft.x),abs(botLeft.x))
        dy = max(abs(topLeft.y),abs(botLeft.y))
        xWorld = parentTransform.position.x-dx
        yWorld = parentTransform.position.y+dy

        #Screen Space
        vScreen = ComponentTransform.Transform.WorldToScreenPos(Vec2(xWorld,yWorld), self.parent.GetParentScene().defaultCam)
        xScreen = vScreen.x
        yScreen = vScreen.y
        screenScale = Vec2(self.lenX*width*parentTransform.scale.x,self.lenY*height*parentTransform.scale.y) * (1 / 2.0)

        image = pygame.transform.scale(self.sprite,(screenScale.x,screenScale.y))
        image = pygame.transform.rotate(image,parentTransform.rotation*180.0/math.pi)
        self.BlitImage(image,(xScreen,yScreen))

    def BlitImage(self, image, coord):
        if self.draw:
            GlobalVars.UILayer.blit(image, coord)
            if self.number is not None:
                parentTransform = self.parent.GetComponent(ComponentType.Transform)
                width = GlobalVars.screen.get_width()
                height = GlobalVars.screen.get_height()
                screenScale = Vec2(self.lenX*10*width*parentTransform.scale.x,self.lenY*height*parentTransform.scale.y) * (1/2.0)
                self.numbers = pygame.transform.scale(self.numbers,(screenScale.x,screenScale.y))
                GlobalVars.UILayer.blit(self.numbers, coord, area=pygame.Rect(self.number * screenScale.x * parentTransform.scale.x / 10, 0, screenScale.x * parentTransform.scale.x / 10, screenScale.y * parentTransform.scale.y))
        
class SpriteGizmo(Sprite):
    def __init__(self, lenX=0.5, lenY=0.5, diameter=None, targetID = None):
        super().__init__(None, lenX, lenY, diameter)
        self.gizmoVal = 0
        self.targetID = targetID
        self.spriteType = SpriteType.Gizmo
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
        topLeft = (Vec2(self.lenX,-self.lenY)/(sceneCam.scale*2.0))
        botLeft = (Vec2(self.lenX, self.lenY)/(sceneCam.scale*2.0))
        #get extremes of AABB
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
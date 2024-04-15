from Components import ComponentSprite
from Components import Component
from Components.Component import ComponentType
from Vector import Vec2
import enum

class BackgroundType(enum.Enum):
    Background = enum.auto()
    Nature = enum.auto()
    Skyline = enum.auto()
    
    def Decode(value):
        members = list(vars(BackgroundType).values())
        members = members[8:len(members)-1]
        for member in members:
            if value == member.value:
                return member

class Background(Component.Component):
    def __init__(self, position = Vec2(0,0),lenX=50,lenY=50):
        self.name = ComponentType.Background
        self.parent = None
        
        self.backgroundType = BackgroundType.Background
        self.initPos = position
        self.lenX = lenX
        self.lenY = lenY
        
    def Start(self):
        self.parent.GetComponent(ComponentType.Transform).position = self.initPos
    
    def Decode(self, obj):
        super().Decode(obj)
        self.backgroundType = BackgroundType.Decode(obj["backgroundType"])
        self.lenX = obj["lenX"]
        self.lenY = obj["lenY"]
        self.initPos = Vec2.FromList(obj["initPos"])

class BackgroundNature(Background):
    def __init__(self, position=Vec2(0, 0), lenX=50, lenY=50):
        super().__init__(position, lenX, lenY)
        self.backgroundType = BackgroundType.Nature
    
    def Start(self):
        super().Start()
        self.parent.AddComponent(ComponentSprite.SpriteBackground("data/BackgroundNature-Sky.png",self.lenX,self.lenY))

class BackgroundSkyline(Background):
    def __init__(self, position=Vec2(0, 0), lenX=50, lenY=50):
        super().__init__(position, lenX, lenY)
        self.backgroundType = BackgroundType.Skyline
        
    def Start(self):
        super().Start()
        self.parent.AddComponent(ComponentSprite.SpriteBackground("data/BackgroundSkyline-Sky.png",self.lenX,self.lenY))
from Components import ComponentSprite
from Components import Component
from Components.Component import ComponentType
import GlobalVars
from Vector import Vec2
import enum

class BackgroundType(enum.Enum):
    Background = enum.auto()
    Nature = enum.auto()
    Skyline = enum.auto()
    
    def Decode(value):
        members = list(vars(BackgroundType).values())
        members = members[GlobalVars.membersOffset:len(members)-1]
        for member in members:
            if value == member.value:
                return member

class Background(Component.Component):
    def __init__(self, position = Vec2(0,0),lenX=50,lenY=50, spritePath = "data/BackgroundNature-Sky.png"):
        self.name = ComponentType.Background
        self.parent = None
        
        self.backgroundType = BackgroundType.Background
        self.initPos = position
        self.lenX = lenX
        self.lenY = lenY
        self.spritePath = spritePath
        
    def Start(self):
        self.parent.GetComponent(ComponentType.Transform).position = self.initPos
        self.parent.AddComponent(ComponentSprite.SpriteBackground(self.spritePath,self.lenX,self.lenY))
    
    def Decode(self, obj):
        super().Decode(obj)
        self.backgroundType = BackgroundType.Decode(obj["backgroundType"])
        self.lenX = obj["lenX"]
        self.lenY = obj["lenY"]
        self.initPos = Vec2.FromList(obj["initPos"])
        self.spritePath = obj["spritePath"]

class BackgroundNature(Background):
    def __init__(self, position=Vec2(0, 0), lenX=50, lenY=50):
        super().__init__(position, lenX, lenY, "data/BackgroundNature-Sky.png")
        self.backgroundType = BackgroundType.Nature

class BackgroundSkyline(Background):
    def __init__(self, position=Vec2(0, 0), lenX=50, lenY=50):
        super().__init__(position, lenX, lenY, "data/BackgroundSkyline-Sky.png")
        self.backgroundType = BackgroundType.Skyline
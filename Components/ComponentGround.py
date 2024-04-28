from Components.Component import ComponentType
from Vector import Vec2
from Components import Component
from Components import ComponentCollider
from Components import ComponentPhysics
from Components import ComponentSprite
import enum

class GroundType(enum.Enum):
    Dirt = enum.auto()
    
    def Decode(value):
        members = list(vars(GroundType).values())
        members = members[8:len(members)-1]
        for member in members:
            if value == member.value:
                return member

class Ground(Component.Component):
    def __init__(self, position = Vec2(0,0), lenX = 1, lenY = 1, rotation = 0.0):
        self.name = ComponentType.Ground
        self.parent = None

        self.initPos = position
        self.initRot = rotation
        self.lenX = lenX
        self.lenY = lenY
    
    def Start(self):
        transform = self.parent.GetComponent(ComponentType.Transform)
        transform.position = self.initPos
        transform.rotation = self.initRot
        
        physics = ComponentPhysics.Physics()
        physics.constraintPosition = True
        physics.constraintRotation = True
        self.parent.AddComponent(physics)
        
        self.parent.AddComponent(ComponentCollider.ColliderRect(lenX = self.lenX, lenY = self.lenY, tags=["Ground"]))
    
    def Decode(self, obj):
        super().Decode(obj)
        self.lenX = obj["lenX"]
        self.lenY = obj["lenY"]
        self.groundType = GroundType.Decode(obj["groundType"])
        self.initPos = Vec2.FromList(obj["initPos"])
        self.initRot = obj["initRot"]
        
class GroundDirt(Ground):
    def __init__(self, position=Vec2(0, 0), lenX=2, lenY=1, rotation=0.0):
        super().__init__(position, lenX, lenY, rotation)
        self.groundType = GroundType.Dirt
    
    def Start(self):
        super().Start()
        self.sprite = self.parent.AddComponent(ComponentSprite.Sprite("data/GroundDirt.png",self.lenX,self.lenY))
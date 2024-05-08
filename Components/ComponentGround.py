from Components.Component import ComponentType
from Vector import Vec2
from Components import Component
from Components import ComponentCollider
from Components import ComponentPhysics
from Components import ComponentSprite
import GlobalVars
import enum

class GroundType(enum.Enum):
    Dirt = enum.auto()
    
    def Decode(value):
        members = list(vars(GroundType).values())
        members = members[GlobalVars.membersOffset:len(members)-1]
        for member in members:
            if value == member.value:
                return member

class Ground(Component.Component):
    def __init__(self, position = None, lenX = 1, lenY = 1, rotation = None):
        self.name = ComponentType.Ground
        self.parent = None

        self.initPos = position
        self.initRot = rotation
        self.lenX = lenX
        self.lenY = lenY
    
    def Start(self):
        transform = self.parent.GetComponent(ComponentType.Transform)
        transform.position = self.initPos if self.initPos is not None else transform.position
        transform.rotation = self.initRot if self.initRot is not None else transform.rotation
        
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
    def __init__(self, position=None, lenX=2, lenY=1, rotation=None):
        super().__init__(position, lenX, lenY, rotation)
        self.groundType = GroundType.Dirt
    
    def Start(self):
        super().Start()
        self.parent.AddComponent(ComponentSprite.Sprite("data/GroundDirt.png",self.lenX,self.lenY))
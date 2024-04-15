from Components.Component import Components
from Vector import Vec2
from Components import Component
from Components import ComponentCollider
from Components import ComponentPhysics
from Components import ComponentSprite
import enum

class GroundType(enum.Enum):
    Dirt = enum.auto()
    
    def Encode(self):
        return self.name

class Ground(Component.Component):
    def __init__(self, position = Vec2(0,0), lenX = 50, lenY = 50, rotation = 0.0):
        self.name = Components.Ground
        self.parent = None

        self.initPos = position
        self.initRot = rotation
        self.lenX = lenX
        self.lenY = lenY
    
    def Start(self):
        transform = self.parent.GetComponent(Components.Transform)
        transform.position = self.initPos
        transform.rotation = self.initRot
        
        physics = ComponentPhysics.Physics()
        physics.constraintPosition = True
        physics.constraintRotation = True
        self.parent.AddComponent(physics)
        
        self.parent.AddComponent(ComponentCollider.ColliderRect(lenX = self.lenX, lenY = self.lenY, tags=["Ground"]))
        
    def Encode(self, obj):
        outDict = super().Encode(obj)
        outDict["lenX"] = obj.lenX
        outDict["lenY"] = obj.lenY
        outDict["groundType"] = obj.groundType.Encode()
        return outDict
        
class GroundDirt(Ground):
    def __init__(self, position=Vec2(0, 0), lenX=50, lenY=50, rotation=0.0):
        super().__init__(position, lenX, lenY, rotation)
        self.groundType = GroundType.Dirt
    
    def Start(self):
        super().Start()
        self.sprite = self.parent.AddComponent(ComponentSprite.Sprite("data/GroundDirt.png",self.lenX,self.lenY))
        
    # def Update(self, deltaTime):
    #     self.parent.GetComponent(Components.Collider).DisplayCollider()
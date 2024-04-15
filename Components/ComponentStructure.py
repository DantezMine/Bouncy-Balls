from Components import ComponentCollider
from Components import ComponentPhysics
from Components import ComponentSprite
from Components import Component
from Components.Component import ComponentType
from Vector import Vec2
import time
import enum

class StructureType(enum.Enum):
    Wood = enum.auto()
    Metal = enum.auto()
    
    def Decode(value):
        members = list(vars(StructureType).values())
        members = members[9:len(members)-1]
        for member in members:
            if value == member.value:
                return member

class Structure(Component.Component):
    def __init__(self, position = Vec2(0,0), lenX = 50, lenY = 50, rotation = 0):
        self.name = ComponentType.Structure
        self.parent = None
        self.initPos = position
        self.initRot = rotation
        self.lenX = lenX
        self.lenY = lenY
        self.destructionMomentum = 100
        self.destroyed = False

    def Start(self):
        transform = self.parent.GetComponent(ComponentType.Transform)
        transform.position = self.initPos
        transform.rotation = self.initRot
        self.parent.AddComponent(ComponentCollider.ColliderRect(lenX = self.lenX, lenY = self.lenY))
        self.parent.AddComponent(ComponentPhysics.Physics())
    
    def Update(self, deltaTime):
        if self.destroyed:
            if time.time() - self.destructionTime >= 5000:
                self.parent.RemoveFromScene()
                
    def CalculateMomentOfInertia(self,mass):
        return 1/12.0 * mass * (self.lenX**2 + self.lenY**2)

    def OnCollision(self, collider):
        self.DestructionCheck(collider)

    def DestructionCheck(self,collider):
        return
        physicsComponent = self.parent.GetComponent(ComponentType.Physics)
        otherPhysicsComponent = collider.parent.GetComponent(ComponentType.Physics)
        momentum = 0
        if physicsComponent == None:
            pass
        else:
            momentum += physicsComponent.mass * physicsComponent.velocity.Mag()
        if otherPhysicsComponent == None:
            pass
        else:
            momentum += physicsComponent.mass * physicsComponent.velocity.Mag()
        if self.destructionMomentum < momentum:
            self.Destruct()
        
    def Destruct(self):
        self.parent.RemoveComponent(ComponentType.Collider)
        self.destroyed = True
        self.destructionTime = time.time()
    
    def Decode(self, obj):
        super().Decode(obj)
        self.structureType = StructureType.Decode(obj["structureType"])
        self.lenX = obj["lenX"]
        self.lenY = obj["lenY"]
        self.destructionMomentum = obj["destructionMomentum"]
        self.destroyed = obj["destroyed"]
        self.initPos = Vec2.FromList(obj["initPos"])
        self.initRot = obj["initRot"]

class StructureWood(Structure):
    '''type : "Wood"'''
    def __init__(self, position = Vec2(0,0), lenX=50, lenY=50, rotation = 0):
        super(StructureWood, self).__init__(position, lenX, lenY, rotation)
        self.structureType = StructureType.Wood

    def Start(self):
        super(StructureWood,self).Start()
        self.destructionMomentum = 2500
        mass = 3
        self.parent.GetComponent(ComponentType.Physics).mass = mass
        self.parent.GetComponent(ComponentType.Physics).momentOfInertia = self.CalculateMomentOfInertia(mass)
        self.parent.AddComponent(ComponentSprite.Sprite(spritePath="data/WoodStructure.png",lenX = self.lenX, lenY = self.lenY))

class StructureMetal(Structure):
    '''type : "Metal"'''
    def __init__(self, position = Vec2(0,0), lenX=50, lenY=50, rotation = 0):
        super(StructureWood, self).__init__(position, lenX, lenY, rotation)
        self.structureType = StructureType.Metal

    def Start(self):
        self.destructionMomentum = 3500
        super(StructureWood,self).Start()
        mass = 5
        self.parent.GetComponent(ComponentType.Physics).mass = mass
        self.parent.GetComponent(ComponentType.Physics).momentOfInertia = self.CalculateMomentOfInertia(mass)
        self.parent.AddComponent(ComponentSprite.Sprite(spritePath="data/StructureMetal.png"))

from Components import ComponentCollider
from Components import ComponentPhysics
from Components import ComponentSprite
from Components import Component
from Components import ComponentStructure
from Components.Component import ComponentType
from Vector import Vec2
import time
import enum
import math
import GameObject
import random

class StructureType(enum.Enum):
    Wood = enum.auto()
    Metal = enum.auto()
    
    def Decode(value):
        members = list(vars(StructureType).values())
        members = members[8:len(members)-1]
        for member in members:
            if value == member.value:
                return member

class Structure(Component.Component):
    def __init__(self, position = Vec2(0,0), lenX = 0.25, lenY = 1, rotation = 0):
        self.name = ComponentType.Structure
        self.parent = None
        self.initPos = position
        self.initRot = rotation
        self.lenX = lenX
        self.lenY = lenY
        self.destructionMomentum = 0
        self.destroyed = False

    def Start(self):
        transform = self.parent.GetComponent(ComponentType.Transform)
        transform.position = self.initPos
        transform.rotation = self.initRot
        if self.destroyed:
            self.parent.RemoveComponent(ComponentType.Collider)
            self.destroyed = True
            self.destructionTime = time.time()
        else:
            self.parent.AddComponent(ComponentCollider.ColliderRect(lenX = self.lenX, lenY = self.lenY))
        self.parent.AddComponent(ComponentPhysics.Physics())
    
    def Update(self, deltaTime):
        # if self.destroyed:
        #     if time.time() - self.destructionTime >= 5000:
        #         self.parent.RemoveFromScene()
        pass
                
    def CalculateMomentOfInertia(self,mass):
        return 1/12.0 * mass * (self.lenX**2 + self.lenY**2)

    def OnCollision(self, collider):
        if not self.destroyed:
            self.DestructionCheck(collider)

    def DestructionCheck(self,collider):
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
        self.destroyed = True
        
        scene = self.parent.GetParentScene()
        self.parent.RemoveFromScene()
        
        transform = self.parent.GetComponent(ComponentType.Transform)
        dir = Vec2(math.cos(transform.rotation+math.pi/2.0),math.sin(transform.rotation+math.pi/2.0))
        offset = dir*(self.lenY/4.0)
        
        fragment1 = GameObject.GameObject(scene)
        fragment1.AddComponent(ComponentStructure.StructureWood(transform.position+offset,self.lenX,self.lenY/2.0,transform.rotation))
        scene.AddGameObject(fragment1)
        
        fragment2 = GameObject.GameObject(scene)
        fragment2.AddComponent(ComponentStructure.StructureWood(transform.position-offset,self.lenX,self.lenY/2.0,transform.rotation))
        scene.AddGameObject(fragment2)
        
        fragment1.RemoveComponent(ComponentType.Collider)
        fragment2.RemoveComponent(ComponentType.Collider)
        
        physicsState = self.parent.GetComponent(ComponentType.Physics).SaveState()
        
        sprayAngle1 = random.random() * math.pi
        sprayAngle2 = (random.random() + 1) * math.pi
        sprayDir1 = Vec2(math.cos(sprayAngle1),math.sin(sprayAngle1))
        sprayDir2 = Vec2(math.cos(sprayAngle2),math.sin(sprayAngle2))
        physics1 = fragment1.GetComponent(ComponentType.Physics)
        physics2 = fragment2.GetComponent(ComponentType.Physics)
        physics1.LoadState(physicsState)
        physics2.LoadState(physicsState)
        physics1.AddForce(sprayDir1 * 1000 - physics1.velocity * 1500, transform.position)
        physics2.AddForce(sprayDir2 * 1000 - physics2.velocity * 1500, transform.position)
    
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
    def __init__(self, position = Vec2(0,0), lenX=0.3, lenY=0.8, rotation = 0):
        super().__init__(position, lenX, lenY, rotation)
        self.structureType = StructureType.Wood

    def Start(self):
        super().Start()
        self.destructionMomentum = 25
        mass = 5
        self.parent.GetComponent(ComponentType.Physics).mass = mass
        self.parent.GetComponent(ComponentType.Physics).momentOfInertia = self.CalculateMomentOfInertia(mass)
        self.parent.AddComponent(ComponentSprite.Sprite(spritePath="data/WoodStructure.png",lenX = self.lenX, lenY = self.lenY))

class StructureMetal(Structure):
    '''type : "Metal"'''
    def __init__(self, position = Vec2(0,0), lenX=0.25, lenY=1.0, rotation = 0):
        super().__init__(position, lenX, lenY, rotation)
        self.structureType = StructureType.Metal

    def Start(self):
        super().Start()
        self.destructionMomentum = 35
        mass = 10
        self.parent.GetComponent(ComponentType.Physics).mass = mass
        self.parent.GetComponent(ComponentType.Physics).momentOfInertia = self.CalculateMomentOfInertia(mass)
        self.parent.AddComponent(ComponentSprite.Sprite(spritePath="data/StructureMetal.png",lenX = self.lenX, lenY = self.lenY))

import ComponentCollider
import ComponentPhysics
import ComponentSprite
import Component
from Vector import Vec2
import time


class Structure(Component.Component):
    def __init__(self, position = Vec2(0,0), lenX = 50, lenY = 50):
        self.name = "Structure"
        self.parent = None
        self.initPos = position
        self.lenX = lenX
        self.lenY = lenY
        self.destructionMomentum = 100
        self.destroyed = False

    def Start(self):
        self.parent.GetComponent("Transform").position = self.initPos
        self.parent.AddComponent(ComponentCollider.ColliderRect(lenX = self.lenX, lenY = self.lenY))
        self.parent.AddComponent(ComponentPhysics.Physics())
    
    def Update(self, deltaTime):
        if self.destroyed:
            if time.time() - self.destructionTime >= 5000:
                self.parent.RemoveFromScene()

    def OnCollision(self, collider):
        self.DestructionCheck(collider)

    def DestructionCheck(self,collider):
        physicsComponent = self.parent.GetComponent("Physics")
        otherPhysicsComponent = collider.parent.GetComponent("Physics")
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
        self.parent.RemoveComponent("Collider")
        self.destroyed = True
        self.destructionTime = time.time()
    
    def Encode(self,obj):
        outDict = super(Structure,self).Encode(obj)
        outDict["structureType"] = obj.structureType
        outDict["lenX"] = obj.lenX
        outDict["lenY"] = obj.lenY
        outDict["destructionMomentum"] = obj.destructionMomentum
        if obj.destroyed != False:
            outDict["destroyed"] = obj.destroyed
        return outDict

class StructureWood(Structure):
    '''type : "Wood"'''
    def __init__(self, position, lenX=50, lenY=50):
        super(StructureWood, self).__init__(position, lenX, lenY)
        self.structureType = "Wood"

    def Start(self):
        super(StructureWood,self).Start()
        self.destructionMomentum = 20
        self.parent.GetComponent("Physics").mass = 30
        self.parent.AddComponent(ComponentSprite.Sprite(spritePath="data/WoodStructure.png",lenX = self.lenX, lenY = self.lenY))

class StructureMetal(Structure):
    '''type : "Metal"'''
    def __init__(self, position, lenX=50, lenY=50):
        super(StructureWood, self).__init__(position, lenX, lenY)
        self.structureType = "Metal"

    def Start(self):
        self.destructionMomentum = 20
        super(StructureWood,self).Start()
        self.parent.GetComponent("Physics").mass = 50
        self.parent.AddComponent(ComponentSprite.Sprite(spritePath="data/StructureMetal.png"))

import ComponentCollider
import ComponentPhysics
import ComponentSprite
import Component
import time

class Structure(Component.Component):
    def __init__(self, height, width):
        self.name = "Structure"
        self.parent = None
        self.height = height
        self.width = width
        self.destructionMomentum = 100
        self.destroyed = False
        

    def Start(self):
        self.parent.AddComponent(ComponentCollider.ColliderRect(lenX = self.width, lenY = self.height))
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
        self.destructionTime = time.time

class StructureWood(Structure):

    def Start(self):
        self.destructionMomentum = 20
        self.parent.AddComponent(ComponentCollider.ColliderRect(lenX = self.width, lenY = self.height))
        self.parent.AddComponent(ComponentPhysics.Physics()) 
        self.parent.AddComponent(ComponentSprite.Sprite(b_proc=False, s_spritePath="data/WoodStructure.png"))

class StructureMetal(Structure):

    def Start(self):
         self.destructionMomentum = 20
         self.parent.AddComponent(ComponentCollider.ColliderRect(lenX = self.width, lenY = self.height))
         self.parent.AddComponent(ComponentPhysics.Physics()) 
         self.parent.AddComponent(ComponentSprite.Sprite(b_proc=False, s_spritePath="data/StructureMetal.png"))

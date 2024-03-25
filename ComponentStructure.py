import ComponentCollider
import ComponentPhysics
import ComponentSprite
import Component

class Structure(Component.Component):
    def __init__(self, height, width):
        self.name = "Structure"
        self.parent = None
        self.height = height
        self.width = width
        self.destructionMomentum = 100

    def Start(self):
        self.parent.AddComponent(ComponentCollider.ColliderRect(lenX = self.width, lenY = self.height))
        self.parent.AddComponent(ComponentPhysics.Physics())

    def OnCollision(self, collider):
        pass


class StructureWood(Structure):

    def Start(self):
        self.destructionMomentum = 20
        self.parent.AddComponent(ComponentCollider.ColliderRect(lenX = self.width, lenY = self.height))
        self.parent.AddComponent(ComponentPhysics.Physics()) 
        self.parent.AddComponent(ComponentSprite.Sprite(b_proc=False, s_spritePath="data/WoodStructure.png"))
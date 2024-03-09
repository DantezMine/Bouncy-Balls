import ComponentSprite
import ComponentCollider
import Component
from Vector import Vec2

class MovingCollision(Component.Component):
    def __init__(self):
        self.name = "MovingCollision"
        self.parent = None
    
    def Start(self):
        rectColl = ComponentCollider.ColliderRect()
        rectColl.SetCollider(100,50)
        self.parent.AddComponent(rectColl)
    
    def Update(self,deltaTime):
        collider = self.parent.GetComponent("Collider")
        collider.DisplayCollider()
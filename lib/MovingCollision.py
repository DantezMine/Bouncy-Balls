import ComponentSprite
import ComponentCollider
import Component
from Vector import Vec2

class MovingCollision(Component.Component):
    def __init__(self):
        self.name = "MovingCollision"
        self.parent = None
        
        self.inputForce = Vec2(0,0)
        self.jumpForce = 10000
        self.controllable = False
        self.keyReleased = True
    
    def Start(self):
        rectColl = ComponentCollider.ColliderRect()
        rectColl.SetCollider(100,50)
        self.parent.AddComponent(rectColl)
    
    def Update(self,deltaTime):
        self.HandleInput(deltaTime)
        self.parent.GetComponent("Physics").AddForce(Vec2(0,200*self.parent.GetComponent("Physics").mass))
        self.parent.GetComponent("Physics").AddForce(self.inputForce*self.jumpForce)
        
        collider = self.parent.GetComponent("Collider")
        collider.DisplayCollider()
        allColliders = self.parent.GetParentScene().GetComponents("Collider")
        collisionPoint = collider.CheckCollision(allColliders)
        if collisionPoint is not None:
            fill(0)
            stroke(0)
            ellipse(collisionPoint.x,collisionPoint.y,5,5)
            
    def HandleInput(self,deltaTime):
        self.inputForce = Vec2(0,0)
        if keyPressed:
            if self.controllable and self.keyReleased:
                if key == " ":
                    self.inputForce = Vec2(0,-1)
            self.keyReleased = False
        else:
            self.keyReleased = True
        
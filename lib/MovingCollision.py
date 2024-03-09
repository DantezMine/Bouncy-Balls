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
        self.parent.GetComponent("Physics").AddTorque(1)
        self.parent.GetComponent("Physics").AddForce(self.inputForce*self.jumpForce)
        
        collider = self.parent.GetComponent("Collider")
        collider.DisplayCollider()
        allColliders = self.parent.GetParentScene().GetComponents("Collider")
        collisionInfo = collider.CheckCollision(allColliders)
        if collisionInfo is not None:
            p = collisionInfo.collisionPoint
            n = collisionInfo.collisionNormal
            stroke(220,30,30)
            strokeWeight(1)
            line(p.x,p.y,p.x+n.x*20,p.y+n.y*20)
            self.parent.GetComponent("Physics").CollisionResponseDynamic(collisionInfo)
            
    def HandleInput(self,deltaTime):
        self.inputForce = Vec2(0,0)
        if keyPressed:
            if self.controllable and self.keyReleased:
                if key == " ":
                    self.inputForce = Vec2(0,-1)
            self.keyReleased = False
        else:
            self.keyReleased = True
        
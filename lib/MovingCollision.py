import ComponentSprite
import ComponentCollider
import Component
from Vector import Vec2

class MovingCollision(Component.Component):
    def __init__(self):
        self.name = "MovingCollision"
        self.parent = None
        
        self.velocity = Vec2(0,0)
        self.speed = 60
        self.controllable = False
        self.keyPressedLastFrame = False
        self.keyReleasedLastFrame = False
    
    def Start(self):
        rectColl = ComponentCollider.ColliderRect()
        rectColl.SetCollider(100,50)
        self.parent.AddComponent(rectColl)
    
    def Update(self,deltaTime):
        self.HandleInput(deltaTime)
        self.parent.GetComponent("Transform").position += self.velocity * self.speed * deltaTime
        
        collider = self.parent.GetComponent("Collider")
        collider.DisplayCollider()
        allColliders = self.parent.GetParentScene().GetComponents("Collider")
        collisionPoint = collider.CheckCollision(allColliders)
        if collisionPoint is not None:
            fill(0)
            stroke(0)
            ellipse(collisionPoint.x,collisionPoint.y,5,5)
            
    def HandleInput(self,deltaTime):
        if keyPressed:
            if self.controllable:
                if key == "w":
                    self.velocity = Vec2(0,-1)
                elif key == "s":
                    self.velocity = Vec2(0,1)
                elif key == "a":
                    self.velocity = Vec2(-1,0)
                elif key == "d":
                    self.velocity = Vec2(1,0)
                elif key == "q":
                    self.parent.GetComponent("Transform").Rotate(-deltaTime*0.5)
                elif key == "r":
                    self.parent.GetComponent("Transform").Rotate(deltaTime*0.5)
            self.keyPressedLastFrame = True
        else:
            if self.keyPressedLastFrame:
                self.keyReleasedLastFrame = True
                self.velocity = Vec2(0,0)
            self.keyPressedLastFrame = False
        
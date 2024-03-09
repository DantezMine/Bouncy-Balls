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
        # self.parent.GetComponent("Physics").AddForce(Vec2(0,200*self.parent.GetComponent("Physics").mass))
        # self.parent.GetComponent("Physics").AddTorque(1)
        # self.parent.GetComponent("Physics").AddForce(self.inputForce*self.jumpForce)
        
        collider = self.parent.GetComponent("Collider")
        collider.DisplayCollider()
        allColliders = self.parent.GetParentScene().GetComponents("Collider")
        collisionInfo = collider.CheckCollision(allColliders)
        print("Object ID: %s, Position: %s, Velocity: %s"%(self.parent.GetID(),self.parent.GetComponent("Transform").position,self.parent.GetComponent("Physics").velocity))
        if collisionInfo is not None:
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
        
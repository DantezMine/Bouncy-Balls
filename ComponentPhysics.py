from Vector import Vec2
import Component

class Physics(Component.Component):
    def __init__(self):
        self.name = "Physics"
        self.mass = 1 #kg
        self.momentOfInertia = 1 #
        self.velocity = Vec2(0,0) #m/s
        self.acceleration = Vec2(0,0) #m/s^2
        self.netForce = Vec2(0,0) #N
        self.constraintPositionX = False
        self.constraintPositionY = False
        self.constraintRotation = False
        self.parent = None
        
    def Update(self,deltaTime):
        transform = self.parent.GetComponent("Transform")
        nextPos = transform.position + self.velocity * deltaTime + self.acceleration * (deltaTime*deltaTime*0.5)
        nextVel = self.velocity + self.acceleration * (deltaTime * 0.5)
        nextAcc = self.ApplyForces()
        nextVel = nextVel + nextAcc * (deltaTime * 0.5)
        
        transform.position = nextPos
        self.velocity = nextVel
        self.acceleration = nextAcc
        self.netForce = Vec2(0,0)
        
    def ApplyForces(self):
        if self.constraintPositionX:
            self.netForce.x = 0
        if self.constraintPositionY:
            self.netForce.y = 0
        return self.netForce/float(self.mass)
    
    def AddForce(self, force): #force is a Vec2
        self.netForce += force
from Vector import Vec2
import Component

class Physics(Component.Component):
    def __init__(self):
        self.name = "Physics"
        self.mass = 1.0 #kg
        self.momentOfInertia = 1.0 #
        self.coefficientOfRestitution = 0.8
        
        self.velocity = Vec2(0,0) #m/s
        self.acceleration = Vec2(0,0) #m/s^2
        self.netForce = Vec2(0,0) #N
        
        self.angularSpeed = 0 #radians/s
        self.angularAcc = 0 #radians/s^s
        self.netTorque = 0 #Nm
        
        self.constraintPosition = False #doesn't consider rotation
        self.constraintRotation = False
        self.parent = None
        
    def Update(self,deltaTime):
        transform = self.parent.GetComponent("Transform")
        if self.constraintPosition:
            self.velocity.x = 0
            self.acceleration.x = 0
            self.velocity.y = 0
            self.acceleration.y = 0
        
        if self.constraintRotation:
            self.angularSpeed = 0
            self.angularAcc = 0
            
        nextPos = transform.position + self.velocity * deltaTime + self.acceleration * (deltaTime * deltaTime * 0.5)
        nextVel = self.velocity + self.acceleration * (deltaTime * 0.5)
        nextAcc = self.ApplyForces()
        nextVel = nextVel + nextAcc * (deltaTime * 0.5)
        
        transform.position = nextPos
        self.velocity = nextVel
        self.acceleration = nextAcc
        self.netForce = Vec2(0,0)
        
        nextAngle = transform.rotation + self.angularSpeed * deltaTime + self.angularAcc * (deltaTime * deltaTime * 0.5)
        nextAngSpeed = self.angularSpeed + self.angularAcc * (deltaTime * 0.5)
        nextAngAcc = self.ApplyTorque()
        nextAngSpeed = nextAngSpeed + nextAngAcc * (deltaTime * 0.5)
        
        transform.rotation = nextAngle
        self.angularSpeed =nextAngSpeed
        self.angularAcc = nextAngAcc
        self.netTorque = 0
        
        
    def ApplyForces(self):
        if self.constraintPosition:
            self.netForce = Vec2(0,0)
        return self.netForce/float(self.mass)
    
    def AddForce(self, force): #force is a Vec2
        self.netForce += force
    
    def AddTorque(self,torque): #torque is a scalar
        self.netTorque += torque
        
    def ApplyTorque(self):
        if self.constraintRotation:
            self.netTorque = 0
        return self.netTorque/float(self.momentOfInertia)
        
    #Collision response under the assumption that the bodies cannot rotate, as per p.709
    def CollisionResponseLinear(self,collisionInfo):
        if self.constraintPosition:
            return
        physicsB = collisionInfo.objectB.GetComponent("Physics")
        if physicsB is None or physicsB.constraintPosition: #objectB will not move
            deltaV = collisionInfo.collisionNormal * (-1 * (self.coefficientOfRestitution+1) * self.velocity.Dot(collisionInfo.collisionNormal))
            self.velocity += deltaV
        else:
            topLeft = (self.coefficientOfRestitution+physicsB.coefficientOfRestitution)/2 + 1
            topRight = physicsB.velocity.Dot(collisionInfo.collisionNormal) - self.velocity.Dot(collisionInfo.collisionNormal)
            bottom = (1.0/self.mass) + (1/physicsB.mass)
            deltaP = collisionInfo.collisionNormal * (topLeft * topRight / bottom)
            deltaV = deltaP / self.mass
            self.velocity += deltaV
            physicsB.velocity -= deltaV
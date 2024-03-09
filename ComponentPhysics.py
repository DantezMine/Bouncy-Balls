from Vector import Vec2
import Component
from lib import GlobalVars

class Physics(Component.Component):
    def __init__(self):
        self.name = "Physics"
        self.mass = 1.0 #kg
        self.momentOfInertia = 50 #
        self.coefficientOfRestitution = 1
        
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
    
    def CollisionResponse(self,collisionInfo): #uh rethink this logic
        if self.constraintRotation:
            self.CollisionResponseLinear(collisionInfo)
        else:
            self.CollisionResponseDynamic(collisionInfo)
        
    #Collision response under the assumption that the bodies cannot rotate, as per p.709
    def CollisionResponseLinear(self,collisionInfo):
        if self.constraintPosition:
            return
        physicsB = collisionInfo.objectB.GetComponent("Physics")
        if physicsB is None or physicsB.constraintPosition: #objectB will not move
            deltaV = collisionInfo.collisionNormal * (-1 * (self.coefficientOfRestitution+1) * self.velocity.Dot(collisionInfo.collisionNormal))
            self.velocity += deltaV
            return
        topLeft = (self.coefficientOfRestitution+physicsB.coefficientOfRestitution)/2 + 1
        topRight = physicsB.velocity.Dot(collisionInfo.collisionNormal) - self.velocity.Dot(collisionInfo.collisionNormal)
        bottom = (1.0/self.mass) + (1/physicsB.mass)
        deltaP = collisionInfo.collisionNormal * (topLeft * topRight / bottom)
        deltaV = deltaP / self.mass
        self.velocity += deltaV
        physicsB.velocity -= deltaV
    
    #Fully dynamic collision response as per Chris Hecker: http://www.chrishecker.com/images/e/e7/Gdmphys3.pdf
    def CollisionResponseDynamic(self,collisionInfo):
        if self.constraintPosition:
            return
        physicsB = collisionInfo.objectB.GetComponent("Physics")
        transfA = self.parent.GetComponent("Transform")
        transfB = physicsB.parent.GetComponent("Transform")
        if physicsB is None:# or physicsB.constraintPosition: #objectB will not move
            pass
            return
        vAB = self.velocity-physicsB.velocity
        rAP_ = (collisionInfo.collisionPoint - transfA.position).Perp().Normalize()
        rBP_ = (collisionInfo.collisionPoint - transfB.position).Perp().Normalize()
        normal = collisionInfo.collisionNormal
        top = -1 * (1 + (self.coefficientOfRestitution+physicsB.coefficientOfRestitution)/2.0) * vAB.Dot(normal)
        bottomLeft= normal.Dot(normal*(1.0/self.mass+1.0/physicsB.mass))
        bottomMid = (rAP_.Dot(normal)**2)/self.momentOfInertia
        bottomRight = (rBP_.Dot(normal)**2)/physicsB.momentOfInertia
        deltaP = top / (bottomLeft + bottomMid + bottomRight)
        
        deltaVA = normal * (deltaP/self.mass)
        deltaVB = normal * (-deltaP/physicsB.mass)
        deltaWA = rAP_.Dot(normal*deltaP)/self.momentOfInertia
        deltaWB = rBP_.Dot(normal*-deltaP)/physicsB.momentOfInertia
        
        # stroke(30,30,200)
        # strokeWeight(1)
        # line(transfA.position.x, transfA.position.y, transfA.position.x + self.velocity.x * 1, transfA.position.y + self.velocity.y * 1)
        # line(collisionInfo.collisionPoint.x,collisionInfo.collisionPoint.y,collisionInfo.collisionPoint.x+deltaVA.x*1,collisionInfo.collisionPoint.y+deltaVA.y*1)
        # print("Object ID: %s, Collision Point: %s, Velocity: %s, deltaV: %s, Rotational Speed: %s, deltaW: %s"%(self.parent.GetID(),collisionInfo.collisionPoint,self.velocity,deltaVA,self.angularSpeed,deltaWA))
        # print("Object ID: %s, Collision Point: %s, Velocity: %s, deltaV: %s, Rotational Speed: %s, deltaW: %s"%(physicsB.parent.GetID(),collisionInfo.collisionPoint,physicsB.velocity,deltaVA,physicsB.angularSpeed,deltaWB))
        #GlobalVars.update = False
        self.velocity += deltaVA
        self.angularSpeed += deltaWA
        
        physicsB.velocity += deltaVB
        physicsB.angularSpeed += deltaWB
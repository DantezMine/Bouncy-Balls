from Vector import Vec2
import Component
from lib import GlobalVars

class Physics(Component.Component):
    def __init__(self):
        self.name = "Physics"
        self.mass = 1.0 #kg
        self.momentOfInertia = 50 #
        self.restitution = 0.1
        
        self.velocity = Vec2(0,0) #m/s
        self.acceleration = Vec2(0,0) #m/s^2
        self.netForce = Vec2(0,0) #N
        self.deltaV = Vec2(0,0)
        
        self.angularSpeed = 0 #radians/s
        self.angularAcc = 0 #radians/s^s
        self.netTorque = 0 #Nm
        self.deltaW = 0
        self.deltaPhi = 0
        
        self.constraintPosition = False #doesn't consider rotation
        self.constraintRotation = False
        self.parent = None
        
    def Update(self,deltaTime, mode):
        if mode == 0:
            collisions = self.parent.GetComponent("Collider").collisions
            for collision in collisions:
                self.CollisionResponseDynamic(collision)
        elif mode == 1:
            self.VelocityVerletIntegration(deltaTime)
    
    def VelocityVerletIntegration(self,deltaTime):
        transform = self.parent.GetComponent("Transform")
            
        #add deltaV from collision response
        self.velocity += self.deltaV
        self.deltaV    = Vec2(0,0)
        
        #Velocity verlet p.696
        nextPos = transform.position + self.velocity * deltaTime + self.acceleration * (deltaTime * deltaTime * 0.5)
        nextVel = self.velocity + self.acceleration * (deltaTime * 0.5)
        nextAcc = self.ApplyForces()
        nextVel = nextVel + nextAcc * (deltaTime * 0.5)
        
        transform.position = nextPos
        self.velocity      = nextVel
        self.acceleration  = nextAcc
        self.netForce      = Vec2(0,0)
        
        #add deltaW and deltaPhi from collision response
        transform.Rotate(self.deltaPhi)
        self.angularSpeed += self.deltaW
        self.deltaW   = 0
        self.deltaPhi = 0
        
        #Solving the angular equations of motion in two dimension p.700
        nextAngle    = transform.rotation + self.angularSpeed * deltaTime + self.angularAcc * (deltaTime * deltaTime * 0.5)
        nextAngSpeed = self.angularSpeed + self.angularAcc * (deltaTime * 0.5)
        nextAngAcc   = self.ApplyTorque()
        nextAngSpeed = nextAngSpeed + nextAngAcc * (deltaTime * 0.5)
        
        transform.rotation = nextAngle
        self.angularSpeed  = nextAngSpeed
        self.angularAcc    = nextAngAcc
        self.netTorque     = 0
        
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
        
    #not used anymore
    #Collision response under the assumption that the bodies cannot rotate, as per p.709
    def CollisionResponseLinear(self,collisionInfo):
        physicsB = collisionInfo.objectB.GetComponent("Physics")
        if physicsB is None or physicsB.constraintPosition: #objectB will not move
            deltaV = collisionInfo.collisionNormal * (-(self.restitution+1) * self.velocity.Dot(collisionInfo.collisionNormal))
            self.velocity += deltaV
            return
        if self.constraintPosition: #self will not move
            deltaV = collisionInfo.collisionNormal * (-(physicsB.restitution+1) * physicsB.velocity.Dot(collisionInfo.collisionNormal))
            physicsB.velocity += deltaV
            return
        
        topLeft  = (self.restitution+physicsB.restitution)/2 + 1
        topRight =  physicsB.velocity.Dot(collisionInfo.collisionNormal) - self.velocity.Dot(collisionInfo.collisionNormal)
        bottom   = (1.0/self.mass) + (1/physicsB.mass)
        deltaP   =  collisionInfo.collisionNormal * (topLeft * topRight / bottom)
        deltaV   =  deltaP / self.mass
        self.velocity += deltaV
        physicsB.velocity -= deltaV
    
    #Fully dynamic collision response as per Chris Hecker: http://www.chrishecker.com/images/e/e7/Gdmphys3.pdf with own modificiations
    def CollisionResponseDynamic(self,collisionInfo):        
        physicsB = collisionInfo.objectB.GetComponent("Physics")
        transfA = self.parent.GetComponent("Transform")
        transfB = physicsB.parent.GetComponent("Transform")
        
        moveA, moveB, rotateA, rotateB = 1,1,1,1
        if physicsB is None or physicsB.constraintPosition: #objectB is immovable
            moveB = 0
        if self.constraintPosition or not moveA: #self is immovable
            moveA = 0
        if physicsB is None or physicsB.constraintRotation: #objectB is nonrotatable
            rotateB = 0
        if self.constraintRotation: #self is nonrotatable
            rotateA = 0
            
        if collisionInfo.collisionType == "edge":
            #check whether COM falls over the edge and, if the other object can't move or rotate, don't allow for rotation, and align the faces
            if collisionInfo.edgeVector.Dot(transfB.position-collisionInfo.collisionPoint) > 0:                
                deltaPhi =  collisionInfo.collisionNormal.AngleBetween(collisionInfo.otherNormal*-1)
                if rotateA and rotateB:
                    self.deltaPhi     =  deltaPhi/2
                    physicsB.deltaPhi = -deltaPhi/2
                elif rotateA and not rotateB:
                    self.deltaPhi     =  deltaPhi
                elif not rotateA and rotateB:
                    physicsB.deltaPhi = -deltaPhi
                    
                if not moveB and not rotateB: #object B is immovable and nonrotatable
                    rotateA = 0
                if not moveA and not rotateA: #self is immovable and nonrotatable
                    rotateB = 0
         
            
        normal = collisionInfo.collisionNormal
        rAP_   =  (collisionInfo.collisionPoint - transfA.position).Perp().Normalize()
        rBP_   =  (collisionInfo.collisionPoint - transfB.position).Perp().Normalize()
        vAP    =   self.velocity + rAP_ * self.angularSpeed
        vBP    =   physicsB.velocity + rBP_ * physicsB.angularSpeed
        vAB    =   vAP - vBP
        top    = -(1 + (self.restitution+physicsB.restitution)/2.0) * vAB.Dot(normal)
        
        #if an object is immovable, its mass approaches infinity, thus 1/mass goes to zero
        if moveA and moveB: #both objects will move
            bottomLeft = normal.Dot(normal*(1.0/self.mass+1.0/physicsB.mass))
        if not moveB: #objectB is immovable
            bottomLeft = normal.Dot(normal*(1.0/self.mass))
        if not moveA: #self is immovable
            bottomLeft = normal.Dot(normal*(1.0/physicsB.mass))
        
        #if an object is nonrotatable, its moment of inertia approaches infinity, thus 1/momentOfInertia goes to zero
        if not rotateA and not rotateB: #both objects will rotate
            bottomMid   = (rAP_.Dot(normal)**2)/self.momentOfInertia
            bottomRight = (rBP_.Dot(normal)**2)/physicsB.momentOfInertia
        if not rotateB: #objectB is nonrotatable
            bottomMid   = (rAP_.Dot(normal)**2)/self.momentOfInertia
            bottomRight = 0
        if not rotateA: #self is nonrotatable
            bottomMid   = 0
            bottomRight = (rBP_.Dot(normal)**2)/physicsB.momentOfInertia
            
        deltaP = top / (bottomLeft + bottomMid + bottomRight)
        
        #in the future maybe change to account for collisions that involve the same game objects, calculated in Scene.py
        if collisionInfo.collisionType == "edge":
            deltaP /= 2.0
        
        deltaVA = normal * (deltaP/self.mass) * moveA
        deltaVB = normal * (-deltaP/physicsB.mass) * moveB
        deltaWA = rAP_.Dot(normal*deltaP)/self.momentOfInertia * rotateA
        deltaWB = rBP_.Dot(normal*-deltaP)/physicsB.momentOfInertia * rotateB
        
        print("Collision Type: %s"%(collisionInfo.collisionType))
        print("Object A ID: %s, Collision Point: %s, Collision Normal: %s, Collision Edge Vector: %s, Velocity: %s, deltaV: %s, Rotational Speed: %s, deltaW: %s"%(self.parent.GetID(),collisionInfo.collisionPoint, collisionInfo.collisionNormal,collisionInfo.edgeVector,self.velocity,deltaVA,self.angularSpeed,deltaWA))
        print("moveA: %s, rotateA: %s"%(moveA,rotateA))
        print("Object B ID: %s, Collision Point: %s, Collision Normal: %s, Collision Edge Vector: %s, Velocity: %s, deltaV: %s, Rotational Speed: %s, deltaW: %s"%(physicsB.parent.GetID(),collisionInfo.collisionPoint,collisionInfo.collisionNormal, collisionInfo.edgeVector,physicsB.velocity,deltaVB,physicsB.angularSpeed,deltaWB))
        print("moveB: %s, rotateB: %s"%(moveB,rotateB))
        print("")
        GlobalVars.update = False
        
        self.deltaV += deltaVA
        self.deltaW += deltaWA
        physicsB.deltaV += deltaVB
        physicsB.deltaW += deltaWB
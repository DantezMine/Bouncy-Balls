from Vector import Vec2
import math
import Component
from lib import GlobalVars

class Physics(Component.Component):
    def __init__(self):
        self.name = "Physics"
        self.parent = None
        self.mass = 1.0 #kg
        self.momentOfInertia = 50 #
        self.restitution = 0.2
        
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
        self.gravity = False
        self.gravForce = Vec2(0,300)
        
    def Update(self,deltaTime, allCollisions, mode):
        if mode == 0:
            collisions = self.parent.GetComponent("Collider").collisions
            collisionCounts = self.DetermineSimilarCollisions(collisions, allCollisions)
            for i in range(len(collisions)):
                if collisions[i].collisionResponseTag:
                    self.CollisionResponseDynamic(collisions[i], collisionCounts, i)
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
        
    
    #Fully dynamic collision response as per Chris Hecker: http://www.chrishecker.com/images/e/e7/Gdmphys3.pdf with own modificiations
    def CollisionResponseDynamic(self,collisionInfo, collisionCounts, collisionIndex):        
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
                if not collisionInfo.collisionNormal == -collisionInfo.otherNormal:
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
        rAP_   =  (collisionInfo.collisionPoint - transfA.position).Perp()
        rBP_   =  (collisionInfo.collisionPoint - transfB.position).Perp()
        vAP    =   self.velocity + rAP_ * self.angularSpeed
        vBP    =   physicsB.velocity + rBP_ * physicsB.angularSpeed
        vAB    =   vAP - vBP
        top    = -(1 + (self.restitution+physicsB.restitution)/2.0) * vAB.Dot(normal)
        
        #if an object is immovable, its mass approaches infinity, thus 1/mass goes to zero          
        bottomLeftLeft = 1.0/self.mass if moveA else 0.0
        bottomLeftRight = 1.0/physicsB.mass if moveB else 0.0
        bottomLeft = normal.Dot(normal*(bottomLeftLeft+bottomLeftRight))
        
        #if an object is nonrotatable, its moment of inertia approaches infinity, thus 1/momentOfInertia goes to zero
        bottomMid   = (rAP_.Dot(normal)**2)/self.momentOfInertia if rotateA else 0.0
        bottomRight = (rBP_.Dot(normal)**2)/physicsB.momentOfInertia if rotateB else 0.0
        
        deltaP = top / (bottomLeft + bottomMid + bottomRight)
        
        #divide total change in momentum by amount of collisions with the same object
        deltaP /= collisionCounts[collisionIndex]
                
        cosNormalA = 1#math.cos(normal.AngleBetween(self.gravForce))
        cosNormalB = 1#math.cos(normal.AngleBetween(physicsB.gravForce))
        deltaAccA, deltaAccB = Vec2(0,0), Vec2(0,0) 
        if self.gravity:
            deltaAccA = -self.gravForce * cosNormalA * self.mass / collisionCounts[collisionIndex]
        if physicsB.gravity:
            deltaAccB = -physicsB.gravForce * cosNormalB * physicsB.mass / collisionCounts[collisionIndex]
                
        deltaVA = normal * (deltaP/self.mass) * moveA
        deltaVB = normal * (-deltaP/physicsB.mass) * moveB
        deltaWA = rAP_.Dot(normal*deltaP)/self.momentOfInertia * rotateA
        deltaWB = rBP_.Dot(normal*-deltaP)/physicsB.momentOfInertia * rotateB
        
        
        print("Collision Info: %s"%(collisionInfo))
        print("Object A ID: %s, Velocity: %s, deltaV: %s, Rotational Speed: %s, deltaW: %s"%(self.parent.GetID(),self.velocity,deltaVA,self.angularSpeed,deltaWA))
        print("moveA: %s, rotateA: %s"%(moveA,rotateA))
        print("Object B ID: %s, Velocity: %s, deltaV: %s, Rotational Speed: %s, deltaW: %s"%(physicsB.parent.GetID(),physicsB.velocity,deltaVB,physicsB.angularSpeed,deltaWB))
        print("moveB: %s, rotateB: %s"%(moveB,rotateB))
        print("")
        GlobalVars.update = False
        
        self.deltaV += deltaVA
        self.deltaW += deltaWA
        self.AddForce(deltaAccA)
        
        physicsB.deltaV += deltaVB
        physicsB.deltaW += deltaWB
        physicsB.AddForce(deltaAccB)
    
    #count how many collisions in the list are with the same object for each collision
    def DetermineSimilarCollisions(self, collisions, allCollisions):
        collisionCounts = [1.0 for x in range(len(collisions))]
        ID = self.parent.GetID()
        for i in range(len(collisions)):
            objectBID = collisions[i].objectB.GetID()
            for k in range(len(allCollisions)):
                if allCollisions[k].objectA.GetID() == objectBID and allCollisions[k].objectB.GetID() == ID:
                    collisionCounts[i] += 1.0
        return collisionCounts

    def ApplyForces(self):
        if self.constraintPosition:
            self.netForce = Vec2(0,0)
        elif self.gravity:
            self.netForce += self.gravForce * self.mass
        return self.netForce/float(self.mass)
    
    def AddForce(self, force): #force is a Vec2
        self.netForce += force
    
    def AddTorque(self,torque): #torque is a scalar
        self.netTorque += torque
        
    def ApplyTorque(self):
        if self.constraintRotation:
            self.netTorque = 0
        return self.netTorque/float(self.momentOfInertia)
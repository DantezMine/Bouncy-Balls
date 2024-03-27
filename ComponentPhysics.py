import json
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
        
        self.prevPosition = Vec2(0,0)
        self.velocity = Vec2(0,0)
        self.acceleration = Vec2(0,0)
        self.netForce = Vec2(0,0)
        self.deltaV = Vec2(0,0)
        
        self.angularSpeed = 0 #radians/s
        self.angularAcc = 0 #radians/s^s
        self.netTorque = 0
        self.deltaW = 0
        self.deltaPhi = 0
        
        self.constraintPosition = False
        self.constraintRotation = False
        self.gravity = True
        self.gravForce = Vec2(0,980)
    
    def Start(self):
        self.prevPosition = self.parent.GetComponent("Transform").position
        
    def Update(self,deltaTime, allCollisions, mode):
        if mode == 0:
            self.TempNextState(deltaTime)
        if mode == 1:
            collider = self.parent.GetComponent("Collider")
            if collider is not None:
                collisions = collider.collisions
                collisionCounts = self.DetermineSimilarCollisions(collisions, allCollisions)
                for i in range(len(collisions)):
                    if collisions[i].collisionResponseTag:
                        self.CollisionResponseDynamic(collisions[i], collisionCounts, i)
        elif mode == 2:
            self.VelocityVerletIntegration(deltaTime)
    
    def TempNextState(self,deltaTime):
        transform          = self.parent.GetComponent("Transform")
        self.tempNextPos   = transform.position + self.velocity * deltaTime + self.acceleration * (deltaTime * deltaTime * 0.5)
        self.tempNextAngle = transform.rotation + self.angularSpeed * deltaTime + self.angularAcc * (deltaTime * deltaTime * 0.5)
    
    def VelocityVerletIntegration(self,deltaTime):
        transform = self.parent.GetComponent("Transform")
        self.prevPosition = transform.position
            
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
        
        #add deltaW from collision response
        self.angularSpeed += self.deltaW
        self.deltaW   = 0
        
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
        
        collisionPointA = collisionInfo.collisionPoint
        collisionPointB = collisionInfo.otherCollisionPoint
        
        normal = collisionInfo.collisionNormal
        rAP_   =  (collisionPointA - transfA.position).Perp()
        rBP_   =  (collisionPointB - transfB.position).Perp()
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
            
        #angle between negative normal and gravity
        alpha = (-normal).AngleBetween(self.gravForce)
        if alpha > math.pi/2.0:
            alpha -= math.pi/2.0
            
        forceNormalA, forceNormalB = Vec2(0,0), Vec2(0,0)
        forceNormal = normal * -self.gravForce.Mag() * math.cos(alpha)
        if self.gravity:
            forceNormalA = forceNormal * self.mass / collisionCounts[collisionIndex]
        if physicsB.gravity:
            forceNormalB = -forceNormal * physicsB.mass / collisionCounts[collisionIndex]
                
        deltaVA = normal * (deltaP/self.mass) * moveA
        deltaVB = normal * (-deltaP/physicsB.mass) * moveB
        deltaWA = rAP_.Dot(normal*deltaP)/self.momentOfInertia * rotateA
        deltaWB = rBP_.Dot(normal*-deltaP)/physicsB.momentOfInertia * rotateB
        
        if GlobalVars.debug:
            GlobalVars.update = False
            print("Collision Info: %s"%(collisionInfo))
            print("Object A ID: %s, Position: %s, Velocity: %s, deltaV: %s, Rotational Speed: %s, deltaW: %s"%(self.parent.GetID(),self.parent.GetComponent("Transform").position,self.velocity,deltaVA,self.angularSpeed,deltaWA))
            print("moveA: %s, rotateA: %s"%(moveA,rotateA))
            print("Object B ID: %s, Position: %s, Velocity: %s, deltaV: %s, Rotational Speed: %s, deltaW: %s"%(physicsB.parent.GetID(),physicsB.parent.GetComponent("Transform").position,physicsB.velocity,deltaVB,physicsB.angularSpeed,deltaWB))
            print("moveB: %s, rotateB: %s"%(moveB,rotateB))
            print("")
            
            print("forceNormal", forceNormal, "alpha", math.degrees(alpha))
            print("A: ", forceNormalA, collisionPointA)
            print("B: ", forceNormalB, collisionPointB)
            print("")
        
        self.deltaV += deltaVA
        self.deltaW += deltaWA
        # self.deltaPos += deltaPosA
        self.AddForce(forceNormalA, collisionPointA)
        
        physicsB.deltaV += deltaVB
        physicsB.deltaW += deltaWB
        # physicsB.deltaPos += deltaPosB
        physicsB.AddForce(forceNormalB, collisionPointB)
    
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
    
    def AddForce(self, force, point = None): #force is a Vec2
        self.netForce += force
        if point is None:
            return
        #calculate distance from force direction to COM
        posCOM = self.parent.GetComponent("Transform").position
        rAP = posCOM - point
        sign = 1 if rAP.Dot(force.Perp()) > 0 else -1
        phi = force.AngleBetween(rAP)
        distance = rAP.Mag()*math.sin(phi)
        torque = force.Mag() * distance * sign
        self.AddTorque(torque)
        if GlobalVars.debug:
            print("Torque from force %s at point %s with angle %s: %s"%(force,point,phi,torque))
    
    def AddTorque(self,torque): #torque is a scalar
        self.netTorque += torque
        
    def ApplyTorque(self):
        if self.constraintRotation:
            self.netTorque = 0
        return self.netTorque/float(self.momentOfInertia)
    
    def Encode(self,obj):
        outDict = super(Physics,self).Encode(obj)
        outDict["mass"] = obj.mass
        outDict["inertia"] = obj.momentOfInertia
        outDict["restitution"] = obj.restitution
        if obj.prevPosition != Vec2(0,0):
            outDict["prevPosition"] = obj.prevPosition.Encode()
        if obj.velocity != Vec2(0,0):
            outDict["velocity"] = obj.velocity.Encode()
        if obj.acceleration != Vec2(0,0):
            outDict["acceleration"] = obj.acceleration.Encode()
        if obj.angularSpeed != 0:
            outDict["angularSpeed"] = obj.angularSpeed
        if obj.angularAcc != 0:
            outDict["angularAcc"] = obj.angularAcc
        if obj.constraintPosition != False:
            outDict["constraintPosition"] = obj.constraintPosition
        if obj.constraintRotation != False:
            outDict["constraintRotation"] = obj.constraintRotation
        if obj.gravity != False:
            outDict["gravity"] = obj.gravity
        if obj.gravForce != Vec2(0,300):
            outDict["gravForce"] = obj.gravForce.Encode()
        return outDict
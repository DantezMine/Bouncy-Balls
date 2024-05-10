import pygame
from Vector import Vec2
import math
from Components import Component
from Components import ComponentCollider
from Components import ComponentPhysics
from Components.Component import ComponentType
import GlobalVars

class PhysicsState:
    def __init__(self, physics):
        self.prevPosition  = physics.prevPosition
        self.velocity      = physics.velocity
        self.acceleration  = physics.acceleration
        self.deltaV        = physics.deltaV
        self.angularSpeed  = physics.angularSpeed
        self.angularAcc    = physics.angularAcc
        self.deltaW        = physics.deltaW
        self.constraintPos = physics.constraintPosition
        self.constraintRot = physics.constraintRotation

class Physics(Component.Component):
    def __init__(self):
        self.name = ComponentType.Physics
        self.parent = None
        self.mass = 1.0 #kg
        self.momentOfInertia = 5 #
        self.restitution = 0.1
        self.velDamping = 0.999
        self.rotDamping = 0.99
        self.forceMargin = 0
        self.torqueMargin = 0
        self.velMargin = 0
        self.rotMargin = 0
        self.posMargin = 0
        
        self.friction = 0.001
        
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
        self.gravAcc = Vec2(0,-9.8)
    
    def Start(self):
        self.prevPosition = self.parent.GetComponent(ComponentType.Transform).position
        
    def Update(self,deltaTime, allCollisions, mode):
        collider = self.parent.GetComponent(ComponentType.Collider)
        if mode == 0:
            self.TempNextState(deltaTime)
        
        #collect collisions and count duplicates (same objects colliding)
        elif mode == 1:
            if collider is not None:
                collisions = collider.collisions
                collisionCounts = self.DetermineSimilarCollisions(collisions, allCollisions)
                for i in range(len(collisions)):
                    if collisions[i].collisionResponseTag:
                        self.CollisionResponseDynamic(collisions[i], collisionCounts, i)
        
        elif mode == 2:
            self.VelocityVerletIntegration(deltaTime)
            
        elif mode == 3:
            self.TempNextState(deltaTime)
            if collider is not None:
                collisions = collider.collisions
                collisionCounts = self.DetermineSimilarCollisions(collisions, allCollisions)
                for i in range(len(collisions)):
                    if collisions[i].tags.__contains__("Ground"):
                        if collisions[i].collisionRespoinseTag:
                            self.CollisionResponseDynamic(collisions[i], collisionCounts, i)
            self.VelocityVerletIntegration(deltaTime)
    
    def TempNextState(self,deltaTime):
        transform          = self.parent.GetComponent(ComponentType.Transform)
        self.tempNextPos   = transform.position + self.velocity * deltaTime + self.acceleration * (deltaTime * deltaTime * 0.5)
        self.tempNextAngle = transform.rotation + self.angularSpeed * deltaTime + self.angularAcc * (deltaTime * deltaTime * 0.5)
        coll = self.parent.GetComponent(ComponentType.Collider)
        if coll is not None:
            coll.Recalculate(temp=True)
    
    def VelocityVerletIntegration(self,deltaTime):
        transform = self.parent.GetComponent(ComponentType.Transform)
        self.prevPosition = transform.position
            
        #add deltaV from collision response
        self.velocity += self.deltaV
        self.deltaV    = Vec2(0,0)
        
        #Velocity verlet p.696
        deltaS = self.velocity * deltaTime + self.acceleration * (deltaTime * deltaTime * 0.5)
        if deltaS.SqMag() > self.posMargin:
            nextPos = transform.position + deltaS
        else:
            nextPos = transform.position
        nextVel = self.velocity + self.acceleration * (deltaTime * 0.5)
        nextAcc = self.ApplyForces()
        nextVel = (nextVel + nextAcc * (deltaTime * 0.5)) * self.velDamping
        
        transform.position = nextPos
        self.velocity      = nextVel if nextVel.SqMag() > self.velMargin else Vec2(0,0)
        self.acceleration  = nextAcc
        self.netForce      = Vec2(0,0)
        
        #add deltaW from collision response
        self.angularSpeed += self.deltaW
        self.deltaW   = 0
        
        #Solving the angular equations of motion in two dimension p.700
        nextAngle    = transform.rotation + self.angularSpeed * deltaTime + self.angularAcc * (deltaTime * deltaTime * 0.5)
        nextAngSpeed = self.angularSpeed + self.angularAcc * (deltaTime * 0.5)
        nextAngAcc   = self.ApplyTorque()
        nextAngSpeed = (nextAngSpeed + nextAngAcc * (deltaTime * 0.5)) * self.rotDamping
        
        transform.rotation = nextAngle
        self.angularSpeed  = nextAngSpeed if nextVel.SqMag() > self.rotMargin else 0
        self.angularAcc    = nextAngAcc
        self.netTorque     = 0
        
        coll = self.parent.GetComponent(ComponentType.Collider)
        if coll is not None:
            coll.Recalculate(temp=False) 
    
    #Fully dynamic collision response as per Chris Hecker: http://www.chrishecker.com/images/e/e7/Gdmphys3.pdf with own modificiations
    def CollisionResponseDynamic(self,collisionInfo : ComponentCollider.CollisionInfo, collisionCounts, collisionIndex):
        physicsB = collisionInfo.objectB.GetComponent(ComponentType.Physics)
        transfA = self.parent.GetComponent(ComponentType.Transform)
        transfB = collisionInfo.objectB.GetComponent(ComponentType.Transform)
        
        moveA, moveB, rotateA, rotateB = 1,1,1,1
        if physicsB is None or physicsB.constraintPosition: #objectB is immovable
            moveB = 0
        if self.constraintPosition: #self is immovable
            moveA = 0
        if physicsB is None or physicsB.constraintRotation: #objectB is nonrotatable
            rotateB = 0
        if self.constraintRotation: #self is nonrotatable
            rotateA = 0
            
        if not moveA and not moveB:
            return
        
        collisionPointA = collisionInfo.collisionPoint
        collisionPointB = collisionInfo.otherCollisionPoint
        
        normal = collisionInfo.collisionNormal
        rAP_   =  (collisionPointA - transfA.position).Perp()
        rBP_   =  (collisionPointB - transfB.position).Perp()
        vAP    =   self.velocity + rAP_ * self.angularSpeed
        vBP    =   physicsB.velocity + rBP_ * physicsB.angularSpeed if moveB else Vec2(0,0)
        vAB    =   vAP - vBP
        top    = -(1 + (self.restitution+physicsB.restitution)/2.0) * vAB.Dot(normal) if moveB else -2
        
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
        alpha = (-normal).AngleBetween(self.gravAcc)
        if alpha > math.pi/2.0:
            alpha -= math.pi/2.0
            
        forceNormalA, forceNormalB = Vec2(0,0), Vec2(0,0)
        accNormal = normal * -self.gravAcc.Mag() * math.cos(alpha)
        if self.gravity:
            forceNormalA = accNormal * (self.mass / collisionCounts[collisionIndex])
        if moveB and physicsB.gravity:
            forceNormalB = -accNormal * (physicsB.mass / collisionCounts[collisionIndex])
                
        deltaVA = normal * (deltaP/self.mass) * moveA - self.velocity * self.friction
        deltaVB = normal * (-deltaP/physicsB.mass) * moveB - physicsB.velocity * physicsB.friction if moveB else Vec2(0,0)
        deltaWA = rAP_.Dot(normal*deltaP)/self.momentOfInertia * rotateA
        deltaWB = rBP_.Dot(normal*-deltaP)/physicsB.momentOfInertia * rotateB if moveB else 0
        
        if GlobalVars.debug:
            GlobalVars.update = False
            print("Collision Info: %s"%(collisionInfo))
            print("Object A ID: %s, Position: %s, Velocity: %s, deltaV: %s, Rotational Speed: %s, deltaW: %s"%(self.parent.GetID(),self.parent.GetComponent(ComponentType.Transform).position,self.velocity,deltaVA,self.angularSpeed,deltaWA))
            print("moveA: %s, rotateA: %s"%(moveA,rotateA))
            print("Object B ID: %s, Position: %s, Velocity: %s, deltaV: %s, Rotational Speed: %s, deltaW: %s"%(physicsB.parent.GetID(),physicsB.parent.GetComponent(ComponentType.Transform).position,physicsB.velocity,deltaVB,physicsB.angularSpeed,deltaWB))
            print("moveB: %s, rotateB: %s"%(moveB,rotateB))
            print("")
            
            print("accNormal", accNormal, "alpha", math.degrees(alpha))
            print("A: ", forceNormalA, collisionPointA)
            print("B: ", forceNormalB, collisionPointB)
            print("")
        
        if moveA:
            self.deltaV += deltaVA
            self.deltaW += deltaWA
            self.AddForce(forceNormalA, collisionPointA)
        if moveB:
            physicsB.deltaV += deltaVB
            physicsB.deltaW += deltaWB
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
            self.netForce += self.gravAcc * self.mass
        netAcc = self.netForce*(1.0/float(self.mass))
        return netAcc if netAcc.SqMag() > self.forceMargin else Vec2(0,0)
    
    def AddForce(self, force, point = None): #force is a Vec2
        self.netForce += force
        if point is None:
            return
        #calculate distance from force direction to COM
        posCOM = self.parent.GetComponent(ComponentType.Transform).position
        rAP = posCOM - point
        sign = 1 if rAP.Dot(force.Perp()) > 0 else -1
        phi = force.AngleBetween(rAP)
        distance = rAP.Mag()*math.sin(phi)
        torque = force.Mag() * distance * sign
        self.AddTorque(torque)
        if GlobalVars.debug:
            startPoint = self.parent.GetComponent(ComponentType.Transform).WorldToScreenPos(point, self.parent.GetParentScene().camera)
            endPoint = self.parent.GetComponent(ComponentType.Transform).WorldToScreenPos(point+force, self.parent.GetParentScene().camera)
            pygame.draw.line(GlobalVars.UILayer,(220,20,20),(startPoint.x,startPoint.y),(endPoint.x,endPoint.y))
            print("Torque from force %s at point %s with angle %s and distance %s: %s, effectively deltaW: %s\n"%(force,point,phi*180/math.pi,distance,torque,torque/(self.mass*1200)))
    
    def AddTorque(self,torque): #torque is a scalar
        self.netTorque += torque
        
    def ApplyTorque(self):
        if self.constraintRotation:
            self.netTorque = 0
        netAngAcc = self.netTorque/float(self.momentOfInertia)
        return netAngAcc if abs(netAngAcc) > self.torqueMargin else 0
    
    def AddImpulse(self, impulse):
        self.deltaV += impulse * (1 / self.mass)
    
    def SaveState(self):
        return PhysicsState(self)
    
    def LoadState(self,state):
        self.prevPosition = state.prevPosition
        self.velocity     = state.velocity
        self.acceleration = state.acceleration
        self.deltaV       = state.deltaV
        self.angularSpeed = state.angularSpeed
        self.angularAcc   = state.angularAcc
        self.deltaW       = state.deltaW
        self.constraintPosition = state.constraintPos
        self.constraintRotation = state.constraintRot
    
    def Decode(self, obj):
        super().Decode(obj)
        self.mass = obj["mass"]
        self.momentOfInertia = obj["momentOfInertia"]
        self.restitution = obj["restitution"]
        self.prevPosition = Vec2.FromList(obj["prevPosition"])
        self.velocity = Vec2.FromList(obj["velocity"])
        self.acceleration = Vec2.FromList(obj["acceleration"])
        self.angularSpeed = obj["angularSpeed"]
        self.angularAcc = obj["angularAcc"]
        self.constraintPosition = obj["constraintPosition"]
        self.constraintRotation = obj["constraintRotation"]
        self.gravity = obj["gravity"]
        self.gravAcc = Vec2.FromList(obj["gravAcc"])
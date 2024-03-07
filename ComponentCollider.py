from Vector import Vec2
import Component
import math

class CollisionInfo:
    def __init__(self,collisionPoint,collisionNormal,objectB):
        self.collisionPoint = collisionPoint
        self.collisionNormal = collisionNormal
        self.objectB = objectB

class Collider(Component.Component):
    def __init__(self):
        self.name = "Collider"
        self.parent = None
    
    def SetCollider(self, colliderType,localPosition,localRotation,localScale): #tried to use super(), but shit doesn't work and I don't understand why
        self.colliderType = colliderType
        self.localPosition = localPosition
        self.localRotation = localRotation
        self.localScale = localScale
        
    def BoolCollision(self):
        pass

class ColliderCircle(Collider):
    def SetCollider(self, radius = 50, localPosition = Vec2(0,0), localRotation = 0, localScale = 1):
        self.colliderType = "Circle"
        self.localPosition = localPosition
        self.localRotation = localRotation
        self.localScale = localScale        
        self.radius = radius
        
    def BoolCollision(self):
        pass

class ColliderRect(Collider):
    def SetCollider(self, lenX = 50, lenY = 50, localPosition = Vec2(0,0), localRotation = 0, localScale = 1):
        self.colliderType = "Rect"
        self.localPosition = localPosition
        self.localRotation = localRotation
        self.localScale = localScale
        self.lenX = lenX
        self.lenY = lenY
        
    def CheckCollision(self, colliders):
        for collider in colliders:
            if collider.parent.GetID() == self.parent.GetID():
                continue
            if collider.colliderType == "Rect":
                verts = self.GetVertices()
                collVerts = collider.GetVertices()
                for p in collVerts:
                    inside = True
                    for i in range(4):
                        AB = verts[(i+1)%4] - verts[i]
                        AP = p - verts[i]
                        normal = Vec2(-AB.y,AB.x)
                        if AP.Dot(normal) >= 0:
                            inside = False
                            break
                    if inside: #find face whose normal most opposes direction of combined velocity, i.e. normal that was most likely hit
                        parentPhysics = self.parent.GetComponent("Physics")
                        otherPhysics = collider.parent.GetComponent("Physics")
                        combinedVelocity = Vec2(0,0)
                        
                        #check if objects have a physics component whose velocity we need to consider
                        if parentPhysics is not None:
                            combinedVelocity += parentPhysics.velocity
                        if otherPhysics is not None:
                            combinedVelocity += otherPhysics.velocity
                        if parentPhysics is None and otherPhysics is None:
                            return None
                        #if the velocities cancel out perfectly, the velocity of the other object (with vertex inside this one) is chosen
                        if combinedVelocity.SqMag() == 0:
                            combinedVelocity = otherPhysics.velocity
                        
                        minDot = 0 #i think there should always be a normal going the other way and thus at least one or two dot products should be below zero
                        minNormal = None
                        for i in range(4):
                            ab = verts[(i+1)%4]-verts[i]
                            n = Vec2(-ab.y,ab.x)
                            if combinedVelocity.Dot(n) < minDot:
                                minDot = combinedVelocity.Dot(n)
                                minNormal = n
                        return CollisionInfo(p,minNormal.Normalized(),collider.parent)
                        
                    # if inside: #find closest border/face to the vertex of collision
                    #     minH = 100000
                    #     indX = -1
                    #     for i in range(4):
                    #         AB = verts[(i+1)%4] - verts[i]
                    #         AP = p - verts[i]
                    #         height = AP.Mag() * math.sin(AB.AngleBetween(AP))
                    #         if height < minH:
                    #             minH = height
                    #             indX = i
                    #     A = verts[indX]
                    #     AB = verts[(indX+1)%4] - A
                    #     AP = p - A
                    #     closestPointOnBorder = A + AP.ProjectedOn(AB)
                    #     return closestPointOnBorder
        return None
    
    def GetVertices(self):#CCW starting top left if not rotated
        transf = self.parent.GetComponent("Transform")
        center = transf.position+self.localPosition
        A = center + Vec2(-self.lenX/2,-self.lenY/2).Rotate(transf.rotation+self.localRotation)
        B = center + Vec2(-self.lenX/2, self.lenY/2).Rotate(transf.rotation+self.localRotation)
        C = center + Vec2( self.lenX/2, self.lenY/2).Rotate(transf.rotation+self.localRotation)
        D = center + Vec2( self.lenX/2,-self.lenY/2).Rotate(transf.rotation+self.localRotation)
        return [A,B,C,D]
    
    def DisplayCollider(self):
        verts = self.GetVertices()
        noFill()
        stroke(20,220,20)
        strokeWeight(2)
        beginShape()
        for v in verts:
            vertex(v.x,v.y)
        endShape(CLOSE)
        strokeWeight(1)
        for i in range(4):
            ab = verts[(i+1)%4]-verts[i]
            n = Vec2(-ab.y,ab.x).Normalize()
            mid = verts[i] + ab/2
            line(mid.x,mid.y,mid.x+n.x*20,mid.y+n.y*20)
            
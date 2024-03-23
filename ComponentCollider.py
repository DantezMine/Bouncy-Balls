from Vector import Vec2
import Component
import math

class CollisionInfo:
    def __init__(self, collisionPoint, otherCollisionPoint, collisionDistance, collisionNormal, otherNormal, objectA, objectB, collisionType, collisionResponseTag): #collisionType: "vertEdge","edge"
        '''
        collisionType: "vertEdge","edge"
        '''
        self.collisionPoint = collisionPoint #Point where touch
        self.otherCollisionPoint = otherCollisionPoint #Point where touch if "edge"
        self.collisionDistance = collisionDistance
        self.collisionNormal = collisionNormal #One Normal from touch
        self.otherNormal = otherNormal #opposing to collisionNormal
        self.objectA = objectA #self.parent
        self.objectB = objectB #collider.parent
        self.collisionType = collisionType #best "vertEdge"
        self.collisionResponseTag = collisionResponseTag #tells the physics engine whether the collision requires a response. if either collider has a NoCollisionResponse in its list of tags, no collision response will happen
        
    def __str__(self):
        return ("Object A: %s, Object B: %s, Collision Type: %s, Collision Point: %s, Other Collision Point: %s Collision Distance: %s, Collision Normal: %s, Other Normal: %s, Collision Response: %s"%(self.objectA.GetID(),self.objectB.GetID(),self.collisionType,self.collisionPoint,self.otherCollisionPoint,self.collisionDistance,self.collisionNormal,self.otherNormal,self.collisionResponseTag))

class Collider(Component.Component):
    def __init__(self):
        self.name = "Collider"
        self.parent = None
        
        self.tags = []
                
        self.collisions = []
        self._safetyMargin = 10
        self._edgeAlignmentMargin = 0.01
    
    def SetCollider(self, colliderType,localPosition,localRotation,localScale): #tried to use super(), but shit doesn't work and I don't understand why
        self.colliderType = colliderType
        self.localPosition = localPosition
        self.localRotation = localRotation
        self.localScale = localScale

    def DisplayCollider(self):
        pass
    
    def Update(self,deltaTime,colliders):
        self.collisions = []
        self.CheckCollision(colliders)
        self._UpdateOnCollision()
    
    def _UpdateOnCollision(self):
        for collider in self.collisions:
            self.parent.UpdateOnCollision(collider)
    
class ColliderCircle(Collider):
    def SetCollider(self, radius = 50, localPosition = Vec2(0,0), localRotation = 0, localScale = 1):
        self.colliderType = "Circle"
        self.localPosition = localPosition
        self.localRotation = localRotation
        self.localScale = localScale        
        self.radius = radius
        self.sqRadius = radius**2
        
    def Update(self,deltaTime,colliders):
        self.collisions = []
        self.CheckCollision(colliders)
        self._UpdateOnCollision()
    
    def CheckCollision(self, colliders):
        transform = self.parent.GetComponent("Transform")
        center = transform.position
        for collider in colliders:
            collisionResponseTag = False if self.tags.__contains__("NoCollisionResponse") or collider.tags.__contains__("NoCollisionResponse") else True
            if collider.parent.GetID() == self.parent.GetID():
                continue
            if collider.colliderType == "Circle":
                collTransform = collider.parent.GetComponent("Transform")
                collCenter = collTransform.position
                deltaLocalPosition = center - collCenter
                if (collider.radius + self.radius)**2 >= deltaLocalPosition.SqMag():
                    p2p = collCenter-center
                    collisionPoint = center+p2p.Normalize()*self.radius
                    collisionDistance = (collCenter-center).Mag()
                    self.collisions.append(CollisionInfo(collisionPoint, collisionDistance, (center - collisionPoint).Normalized(), None, None, self.parent, collider.parent, "vertEdge", collisionResponseTag))
        return
    
    def DisplayCollider(self):
        transform = self.parent.GetComponent("Transform")
        center = transform.position
        noFill()
        stroke(20,220,20)
        strokeWeight(2)
        ellipse(center.x, center.y, self.radius*2*transform.scale, self.radius*2*transform.scale)

class ColliderRect(Collider):
    def SetCollider(self, lenX = 50, lenY = 50, localPosition = Vec2(0,0), localRotation = 0, localScale = 1):
        self.colliderType = "Rect"
        self.localPosition = localPosition
        self.localRotation = localRotation
        self.localScale = localScale
        self.lenX = lenX
        self.lenY = lenY
        self.sqRadius = Vec2(lenX/2,lenY/2).SqMag()
    
    def Update(self,deltaTime,colliders):
        self.collisions = []
        self.CheckCollision(colliders)
        self._UpdateOnCollision()
        
    def CheckCollision(self, colliders):
        for collider in colliders:
            if collider.parent.GetID() == self.parent.GetID():
                continue
            if collider.colliderType == "Rect":
                verts = self.GetVertices()
                collVerts = collider.GetVertices()
                
                #edges have priority over vertex collisions
                if self.CheckCollisionEdge(collider,verts,collVerts):
                    continue
                self.CheckCollisionVertEdge(collider,verts,collVerts)
        return
    
    def CheckCollisionEdge(self,collider,verts,collVerts):
        collisionResponseTag = False if self.tags.__contains__("NoCollisionResponse") or collider.tags.__contains__("NoCollisionResponse") else True
        minEdgeEdgeDistance = 1000000
        A_, B_, C_, D_ = None,None,None,None
        #check each edge against each other
        for i in range(len(verts)):
            A, B = verts[i], verts[(i+1)%len(verts)]
            AB = B-A
            normalAB = AB.Perp().Normalize()
            for k in range(len(collVerts)):
                C, D = collVerts[k], collVerts[(k+1)%len(collVerts)]
                CD = D-C
                normalCD = CD.Perp().Normalize()
                
                #keep going if edge normals are mostly opposed, only one per edge
                if not (normalAB.Dot(normalCD) < -1 + self._edgeAlignmentMargin):
                    continue
                #get closest vertex of other edge to current own edge
                closestVertex, onLine, collisionDistance = Vec2(0,0), False, 0.0
                closestVertex, onLine, collisionDistance = self.ClosesetPointToSegment(closestVertex,onLine,collisionDistance,A,B,C,D)
                #check if closest point projects onto the actual segment
                if not onLine:
                    continue
                
                #check if the closest point to edge is inside the rectangle
                if not self.IsPointInsideRect(closestVertex,verts):
                    continue
                
                if collisionDistance < minEdgeEdgeDistance:
                    minEdgeEdgeDistance = collisionDistance
                    A_,B_,C_,D_ = A,B,C,D
        
        if A_ is not None:
            #recalculate normals
            AB = B_-A_
            CD = D_-C_
            normalAB = AB.Perp().Normalized()
            normalCD = CD.Perp().Normalized()
            
            #project COM on other edge segment
            projectionCOMA = self.ClosestPointOnSegment(C_,D_,self.parent.GetComponent("Transform").position)
            collisionPointA = projectionCOMA
            projectionCOMB = self.ClosestPointOnSegment(A_,B_,collider.parent.GetComponent("Transform").position)
            collisionPointB = projectionCOMB
            self.collisions.append(CollisionInfo(collisionPoint=collisionPointA,otherCollisionPoint=collisionPointB,collisionDistance=minEdgeEdgeDistance,collisionNormal=normalAB,otherNormal=normalCD,objectA=self.parent,objectB=collider.parent,collisionType="edge",collisionResponseTag=collisionResponseTag))
            return True
        return False
            
                
    def CheckCollisionVertEdge(self,collider,verts,collVerts):
        collisionResponseTag = False if self.tags.__contains__("NoCollisionResponse") or collider.tags.__contains__("NoCollisionResponse") else True
        for p in collVerts:
            #check if point is inside rectangle
            if not self.IsPointInsideRect(p,verts):
                continue
            
            closestNormal, normalDistance = Vec2(0,0), 0.0
            closestNormal, normalDistance = self.ClosestEdgeToPoint(closestNormal,normalDistance,p,verts)
            self.collisions.append(CollisionInfo(collisionPoint=p, otherCollisionPoint=p, collisionDistance=normalDistance, collisionNormal=closestNormal, otherNormal=None, objectA=self.parent, objectB=collider.parent, collisionType="vertEdge", collisionResponseTag=collisionResponseTag))
            return
    
    def IsPointInsideRect(self,point,verts):
        for i in range(len(verts)):
            AB = verts[(i+1)%4] - verts[i]
            AP = point - verts[i]
            normal = Vec2(-AB.y,AB.x)
            if AP.Dot(normal) >= 0:
                return False
        return True
            
    def ClosestPointOnSegment(self,A,B,point):
        AB = B-A
        projectionPoint = (point-A).ProjectedOn(AB)
        if projectionPoint.Dot(AB) < 0:
            return A
        elif projectionPoint.Dot(AB) > 0 and projectionPoint.SqMag() > AB.SqMag():
            return B
        else:
            return A + projectionPoint
        
    def ClosestEdgeToPoint(self,normal,distance, p,verts):
        minSqDistance = 1000000
        indx = 0
        for i in range(len(verts)):
            A, B = verts[i], verts[(i+1)%len(verts)]
            AB = B-A
            AP = p-A
            v = AP.ProjectedOn(AB)
            dist = (v+A-p).SqMag()
            if dist < minSqDistance:
                minSqDistance = dist
                indx = i
        
        A, B = verts[indx], verts[(indx+1)%len(verts)]
        normal = (B-A).Normalized().Perp()
        distance = math.sqrt(minSqDistance)
        return normal,distance
    
    def ClosesetPointToSegment(self,Vc,onLine,d,A,B,C,D):
        SqDC, SqDD = 0, 0
        SqDC, onLineC = self.SqDistancePointSegment(SqDC,onLine,A,B,C) #square distance from C to edge
        SqDD, onLineD = self.SqDistancePointSegment(SqDD,onLine,A,B,D) #square distance from D to edge
        if SqDC < SqDD:
            Vc = C
            d = math.sqrt(SqDC)
            onLine = onLineC
        else:
            Vc = D
            d = math.sqrt(SqDD)
            onLine = onLineD
        return (Vc, onLine, d)

    def SqDistancePointSegment(self,sqD,onLine,A,B,P):
        AB = B-A
        AP = P-A
        v = AP.ProjectedOn(AB)
        #point is beyond A
        if AB.Dot(v) < 0:
            sqD = AP.SqMag()
            onLine = False
        #point is beyond B
        elif AB.Dot(v) > 0 and AB.SqMag() < v.SqMag():
            sqD = (P-B).SqMag()
            onLine = False
        else:
            sqD = (P-A-v).SqMag()
            onLine = True
        return (sqD, onLine)
    
    def GetRelativeVelocity(self,collider,pointA,pointB): #points on the body whose velocity we use
        parentPhysics = self.parent.GetComponent("Physics")
        otherPhysics = collider.parent.GetComponent("Physics")
        relativeVelocity = Vec2(0,0)
            
        #check if objects have a physics component whose velocity we need to consider
        if parentPhysics is not None:
            rAP_   =  -(pointA - self.parent.GetComponent("Transform").position).Perp()
            vAP    =   parentPhysics.velocity + rAP_ * parentPhysics.angularSpeed
            relativeVelocity -= vAP
        if otherPhysics is not None:
            rBP_   =  -(pointB - otherPhysics.parent.GetComponent("Transform").position).Perp()
            vBP    =   otherPhysics.velocity + rBP_ * otherPhysics.angularSpeed
            relativeVelocity += vBP
        if parentPhysics is None and otherPhysics is None:
            return Vec2(0,0)
        
        #if the velocities cancel out perfectly, the velocity of the other object (with vertex inside this one) is chosen
        if relativeVelocity.SqMag() == 0:
            relativeVelocity = otherPhysics.velocity       
        return relativeVelocity
    
    def GetVertices(self):#CCW starting top left if not rotated
        transf = self.parent.GetComponent("Transform")
        center = transf.position+self.localPosition
        A = center + Vec2(-self.lenX/2,-self.lenY/2).Rotate(transf.rotation+self.localRotation)*self.localScale*transf.scale
        B = center + Vec2(-self.lenX/2, self.lenY/2).Rotate(transf.rotation+self.localRotation)*self.localScale*transf.scale
        C = center + Vec2( self.lenX/2, self.lenY/2).Rotate(transf.rotation+self.localRotation)*self.localScale*transf.scale
        D = center + Vec2( self.lenX/2,-self.lenY/2).Rotate(transf.rotation+self.localRotation)*self.localScale*transf.scale
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
        #display normals
        for i in range(4):
            ab = verts[(i+1)%4]-verts[i]
            n = Vec2(-ab.y,ab.x).Normalize()
            mid = verts[i] + ab/2
            line(mid.x,mid.y,mid.x+n.x*20,mid.y+n.y*20)
            
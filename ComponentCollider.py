from Vector import Vec2
from Component import Components
from lib import GlobalVars
import Component
import enum
import pygame

class ColliderType(enum.Enum):
    Circle = enum.auto()
    Rect = enum.auto()
    
    def Encode(self):
        return self.name

class CollisionInfo:
    def __init__(self, collisionPoint, otherCollisionPoint, collisionNormal, otherNormal, objectA, objectB, collisionType, collisionResponseTag):
        '''
        collisionType: "vertEdge","edge"
        '''
        self.collisionPoint = collisionPoint #Point where touch
        self.otherCollisionPoint = otherCollisionPoint #Point where touch if "edge"
        self.collisionNormal = collisionNormal #One Normal from touch
        self.otherNormal = otherNormal #opposing to collisionNormal
        self.objectA = objectA #self.parent
        self.objectB = objectB #collider.parent
        self.collisionType = collisionType #best "vertEdge"
        self.collisionResponseTag = collisionResponseTag #tells the physics engine whether the collision requires a response. if either collider has a NoCollisionResponse in its list of tags, no collision response will happen
        
    def __str__(self):
        return ("Object A: %s, Object B: %s, Collision Type: %s, Collision Point: %s, Other Collision Point: %s, Collision Normal: %s, Other Normal: %s, Collision Response: %s"%(self.objectA.GetID(),self.objectB.GetID(),self.collisionType,self.collisionPoint,self.otherCollisionPoint,self.collisionNormal,self.otherNormal,self.collisionResponseTag))

class Collider(Component.Component):
    def __init__(self, localPosition=Vec2(0,0),localRotation=0,localScale=1):
        self.name = Component.Components.Collider
        self.parent = None
        self.colliderType = None
        self.tags = []
                
        self.collisions = []
        self._safetyMargin = 10
        self._edgeAlignmentMargin = 0.01
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
            self.parent.UpdateOnCollision(collider.objectB.GetComponent(Components.Collider))
    
    def Encode(self,obj):
        outDict = super(Collider,self).Encode(obj)
        if obj.localPosition != Vec2(0,0):
            outDict["localPosition"] = obj.localPosition
        if obj.localRotation != 0:
            outDict["localRotation"] = obj.localRotation
        if obj.localScale != 1:
            outDict["localScale"] = obj.localScale
        if obj.colliderType is not None:
            outDict["colliderType"] = obj.colliderType.Encode()
        return outDict
    
class ColliderCircle(Collider):
    def __init__(self, radius=50, localPosition=Vec2(0, 0), localRotation=0, localScale=1):
        super(ColliderCircle,self).__init__(localPosition, localRotation, localScale)
        self.colliderType = ColliderType.Circle
        self.radius = 50
        self.sqRadius = radius**2
        
    def Update(self,deltaTime,colliders):
        self.collisions = []
        self.CheckCollision(colliders)
        self._UpdateOnCollision()
    
    def CheckCollision(self, colliders):
        transform = self.parent.GetComponent(Components.Transform)
        center = transform.position
        for collider in colliders:
            self.CheckCollisionCircle(collider,center)
    
    def CheckCollisionCircle(self,collider, center):
        collisionResponseTag = False if self.tags.__contains__("NoCollisionResponse") or collider.tags.__contains__("NoCollisionResponse") else True
        if not collider.parent.GetID() == self.parent.GetID():
            if collider.colliderType == ColliderType.Circle:
                collTransform = collider.parent.GetComponent(Components.Transform)
                collCenter = collTransform.position
                deltaLocalPosition = center - collCenter
                if (collider.radius + self.radius)**2 >= deltaLocalPosition.SqMag():
                    p2p = collCenter-center
                    collisionPoint = center+p2p.Normalize()*self.radius
                    self.collisions.append(CollisionInfo(collisionPoint=collisionPoint, collisionNormal=(center - collisionPoint).Normalized(), otherNormal=None, objectA=self.parent, objectB=collider.parent, collisionType="vertEdge", collisionResponseTag=collisionResponseTag))
        return
    
    def DisplayCollider(self):
        transform = self.parent.GetComponent(Components.Transform)
        center = transform.position
        pygame.draw.circle(GlobalVars.screen,(20,220,20),(center.x,center.y),self.radius*transform.scale)
        
    def Encode(self,obj):
        outDict = super(ColliderCircle,self).Encode(obj)
        outDict["radius"] = obj.radius
        return outDict

class ColliderRect(Collider):
    def __init__(self, lenX = 50, lenY = 50, localPosition = Vec2(0,0), localRotation = 0, localScale = 1):
        super(ColliderRect,self).__init__(localPosition, localRotation, localScale)
        self.colliderType = ColliderType.Rect
        self.lenX = lenX
        self.lenY = lenY
        self.sqRadius = Vec2(lenX/2.0,lenY/2.0).SqMag()
        
    def Start(self):
        self.Recalculate(temp=False)
    
    def Update(self,deltaTime,colliders):
        self.collisions = []
        self.CheckCollision(colliders)
        self._UpdateOnCollision()
        self.DisplayCollider()
        
    def CheckCollision(self, colliders):
        verts = self.verts
        normals = self.norms
        for collider in colliders:
            if collider.parent.GetID() == self.parent.GetID():
                continue
            #check if the objects are inside each others circumcircles
            posA = self.parent.GetComponent(Components.Transform).position
            posB = collider.parent.GetComponent(Components.Transform).position
            if (posA-posB).SqMag() > self.sqRadius+collider.sqRadius:
                continue
            
            if collider.colliderType == ColliderType.Rect:
                collVerts = collider.verts
                collNorms = collider.norms
                #edges have priority over vertex collisions
                if self.CheckCollisionEdge(collider,verts,normals,collVerts,collNorms):
                    continue
                self.CheckCollisionVertEdge(collider,verts,collVerts)
            elif collider.colliderType == ColliderType.Circle:
                self.CheckCollisionCircle(collider, verts)
        return
    
    def CheckCollisionCircle(self, collider, verts):
        collisionResponseTag = False if self.tags.__contains__("NoCollisionResponse") or collider.tags.__contains__("NoCollisionResponse") else True
        collTransform = collider.parent.GetComponent(Components.Transform)
        collCenter = collTransform.position
        radSq = collider.radius**2
        for i in range(len(verts)):
            A, B = verts[i], verts[(i+1)%len(verts)]
            SqDP, onLine = None, None
            
            SqDP, onLine = self.SqDistancePointSegment(SqDP,onLine,A,B,collCenter)
            if SqDP <= radSq:
                if onLine:
                    AB = B-A
                    AP = collCenter-A
                    collisionPoint = A + AP.ProjectedOn(AB)
                    collNormal = (collCenter - collisionPoint).Normalize()
                    otherNormal = -collNormal
                else:
                    if (collCenter-A).SqMag() <= radSq:
                        collNormal = (collCenter-A).Normalize()
                        otherNormal = None
                        collisionPoint = A
                    else:
                        collNormal = (collCenter-B).Normalize()
                        otherNormal = None
                        collisionPoint = B
                self.collisions.append(CollisionInfo(collisionPoint=collisionPoint, otherCollisionPoint=collisionPoint, collisionNormal=collNormal, otherNormal=otherNormal, objectA=self.parent, objectB=collider.parent, collisionType="vertEdge", collisionResponseTag=collisionResponseTag))
                return
        return
    
    def CheckCollisionEdge(self,collider,verts,normals,collVerts,collNorms):
        collisionResponseTag = False if self.tags.__contains__("NoCollisionResponse") or collider.tags.__contains__("NoCollisionResponse") else True
        SqMinEdgeEdgeDistance = 1000000
        A_, B_, C_, D_ = None,None,None,None
        #check each edge against each other
        for i in range(len(verts)):
            A, B = verts[i], verts[(i+1)%len(verts)]
            normalAB = normals[i]
            for k in range(len(collVerts)):
                C, D = collVerts[k], collVerts[(k+1)%len(collVerts)]
                normalCD = collNorms[k]
                
                #keep going if edge normals are mostly opposed, only one per edge
                if (normalAB.Dot(normalCD) < -1 + self._edgeAlignmentMargin):
                    #get closest vertex of other edge to current own edge
                    closestVertex, onLine, collisionDistance = Vec2(0,0), False, 0.0
                    closestVertex, onLine, collisionDistance = self.ClosesetPointToSegment(closestVertex,onLine,collisionDistance,A,B,C,D)
                    #check if closest point projects onto the actual segment
                    if onLine:
                        #check if the closest point to edge is inside the rectangle
                        if self.IsPointInsideRect(closestVertex,verts):                        
                            if collisionDistance < SqMinEdgeEdgeDistance:
                                SqMinEdgeEdgeDistance = collisionDistance
                                A_,B_,C_,D_ = A,B,C,D
        
        if A_ is not None:
            #recalculate normals
            AB = B_-A_
            CD = D_-C_
            normalAB = AB.Perp().Normalized()
            normalCD = CD.Perp().Normalized()
            
            #project COM on other edge segment
            projectionCOMA = self.ClosestPointOnSegment(C_,D_,self.parent.GetComponent(Components.Transform).position)
            collisionPointA = projectionCOMA
            projectionCOMB = self.ClosestPointOnSegment(A_,B_,collider.parent.GetComponent(Components.Transform).position)
            collisionPointB = projectionCOMB
            self.collisions.append(CollisionInfo(collisionPoint=collisionPointA,otherCollisionPoint=collisionPointB,collisionNormal=normalAB,otherNormal=normalCD,objectA=self.parent,objectB=collider.parent,collisionType="edge",collisionResponseTag=collisionResponseTag))
            return True
        return False

    def CheckCollisionVertEdge(self,collider,verts,collVerts):
        collisionResponseTag = False if self.tags.__contains__("NoCollisionResponse") or collider.tags.__contains__("NoCollisionResponse") else True
        for p in collVerts:
            #check if point is inside rectangle
            if not self.IsPointInsideRect(p,verts):
                continue
            
            closestNormal, vertIndex = Vec2(0,0), 0
            closestNormal, vertIndex = self.ClosestEdgeToPoint(closestNormal,vertIndex,p,verts)
                        
            self.collisions.append(CollisionInfo(collisionPoint=p, otherCollisionPoint=p, collisionNormal=closestNormal, otherNormal=None, objectA=self.parent, objectB=collider.parent, collisionType="vertEdge", collisionResponseTag=collisionResponseTag))
            return
        
    def RaySegmentIntersection(self,hitPoint,hitBool,A,B,P,dir):
        PA = A-P
        AB = B-A
        #lines are parallel up or down
        if (AB.x == 0 and dir.x == 0) or (AB.y == 0 and dir.y == 0):
            return None, False
        elif dir.x == 0.0:
            t = float(-PA.x)/AB.x
            s = PA.y + AB.y*t/dir.y
        elif dir.y == 0.0:
            t = float(-PA.y)/AB.y
            s = PA.x - AB.x*t/dir.x
        else:
            t = float(PA.Cross2D(dir))/dir.Cross2D(AB)
            s = float(A.x-P.x+AB.x*t)/dir.x
        
        if s < 0:
            return None, False
        
        if t < 0:
            hitPoint = A
            hitBool = False
        elif t > 1:
            hitPoint = B
            hitBool = False
        else:
            hitPoint = P + dir * s
            hitBool = True
        return hitPoint,hitBool
                
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
        
    def ClosestEdgeToPoint(self,normal,vertIndex,p,verts):
        minSqDistance = 1000000
        for i in range(len(verts)):
            A, B = verts[i], verts[(i+1)%len(verts)]
            AB = B-A
            AP = p-A
            v = AP.ProjectedOn(AB)
            dist = (v+A-p).SqMag()
            if dist < minSqDistance:
                minSqDistance = dist
                vertIndex = i
        
        A, B = verts[vertIndex], verts[(vertIndex+1)%len(verts)]
        normal = (B-A).Normalized().Perp()
        return normal,vertIndex
    
    def ClosesetPointToSegment(self,Vc,onLine,d,A,B,C,D):
        SqDC, SqDD = 0, 0
        SqDC, onLineC = self.SqDistancePointSegment(SqDC,onLine,A,B,C) #square distance from C to edge
        SqDD, onLineD = self.SqDistancePointSegment(SqDD,onLine,A,B,D) #square distance from D to edge
        if SqDC < SqDD:
            Vc = C
            d = SqDC
            onLine = onLineC
        else:
            Vc = D
            d = SqDD
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
        parentPhysics = self.parent.GetComponent(Components.Physics)
        otherPhysics = collider.parent.GetComponent(Components.Physics)
        relativeVelocity = Vec2(0,0)
            
        #check if objects have a physics component whose velocity we need to consider
        if parentPhysics is not None:
            rAP_   =  -(pointA - self.parent.GetComponent(Components.Transform).position).Perp()
            vAP    =   parentPhysics.velocity + rAP_ * parentPhysics.angularSpeed
            relativeVelocity -= vAP
        if otherPhysics is not None:
            rBP_   =  -(pointB - otherPhysics.parent.GetComponent(Components.Transform).position).Perp()
            vBP    =   otherPhysics.velocity + rBP_ * otherPhysics.angularSpeed
            relativeVelocity += vBP
        if parentPhysics is None and otherPhysics is None:
            return Vec2(0,0)
        
        #if the velocities cancel out perfectly, the velocity of the other object (with vertex inside this one) is chosen
        if relativeVelocity.SqMag() == 0:
            relativeVelocity = otherPhysics.velocity       
        return relativeVelocity
    
    def Recalculate(self, temp):
        self.verts = self.GetVertices(temp)
        self.norms = self.GetNormals(self.verts)
    
    def GetVertices(self, temp=False):#CCW starting top left if not rotated
        physics = self.parent.GetComponent(Components.Physics)
        transf = self.parent.GetComponent(Components.Transform)
        scale = self.localScale*transf.scale
        if temp and physics is not None:
            center = physics.tempNextPos+self.localPosition
            angle = physics.tempNextAngle+self.localRotation
            A = center + Vec2(-self.lenX/2,-self.lenY/2).Rotate(angle)*scale
            B = center + Vec2(-self.lenX/2, self.lenY/2).Rotate(angle)*scale
            C = center + Vec2( self.lenX/2, self.lenY/2).Rotate(angle)*scale
            D = center + Vec2( self.lenX/2,-self.lenY/2).Rotate(angle)*scale
        else:
            center = transf.position+self.localPosition
            angle = transf.rotation+self.localRotation
            A = center + Vec2(-self.lenX/2,-self.lenY/2).Rotate(angle)*scale
            B = center + Vec2(-self.lenX/2, self.lenY/2).Rotate(angle)*scale
            C = center + Vec2( self.lenX/2, self.lenY/2).Rotate(angle)*scale
            D = center + Vec2( self.lenX/2,-self.lenY/2).Rotate(angle)*scale
        return [A,B,C,D]
    
    def GetNormals(self,verts):
        normals = list()
        for i in range(4):
            AB = verts[(i+1)%4]-verts[i]
            normals.append(AB.Perp().Normalize())
        return normals
    
    def DisplayCollider(self):
        verts = self.GetVertices()
        vertices = []
        for v in verts:
            vertices.append((v.x,v.y))
        pygame.draw.polygon(GlobalVars.screen,(20,220,20),vertices,1)

    def Encode(self,obj):
        outDict = super(ColliderRect,self).Encode(obj)
        outDict["lenX"] = obj.lenX
        outDict["lenY"] = obj.lenY
        return outDict
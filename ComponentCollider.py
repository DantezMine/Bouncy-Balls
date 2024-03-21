from Vector import Vec2
import Component
import math

class CollisionInfo:
    def __init__(self, collisionPoint, collisionDistance, collisionNormal, otherNormal, edgeVec, objectA, objectB, collisionType, collisionResponseTag): #collisionType: "vertEdge","edge"
        '''
        collisionType: "vertEdge","edge"
        collisionPoint if "edge": point furthest along the collision edge
        edgeVector points from "edge" collisionPoint to the other point of the edge
        '''
        self.collisionPoint = collisionPoint #Point where touch
        self.collisionDistance = collisionDistance
        self.collisionNormal = collisionNormal #One Normal from touch
        self.otherNormal = otherNormal #opposing to collisionNormal
        self.edgeVector = edgeVec #only edge-edge
        self.objectA = objectA #self.parent
        self.objectB = objectB #collider.parent
        self.collisionType = collisionType #best "vertEdge"
        self.collisionResponseTag = collisionResponseTag #tells the physics engine whether the collision requires a response. if either collider has a NoCollisionResponse in its list of tags, no collision response will happen
        
    def __str__(self):
        return ("Object A: %s, Object B: %s, Collision Type: %s, Collision Point: %s, Collision Distance: %s, Collision Normal: %s, Other Normal: %s, Edge Vector: %s, Collision Response: %s"%(self.objectA.GetID(),self.objectB.GetID(),self.collisionType,self.collisionPoint,self.collisionDistance,self.collisionNormal,self.otherNormal,self.edgeVector, self.collisionResponseTag))

class Collider(Component.Component):
    def __init__(self):
        self.name = "Collider"
        self.parent = None
        
        self.tags = []
                
        self.collisions = []
        self._safetyMargin = 10
        self._edgeAlignmentMargin = 0.05
    
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
        #if furthest vertices aren't in range (within a safety margin), don't bother checking
        # if (self.parent.GetComponent("Transform").position - collider.parent.GetComponent("Transform").position).SqMag() > self.sqRadius + collider.sqRadius + self._safetyMargin:
        #     return False
        collisionResponseTag = False if self.tags.__contains__("NoCollisionResponse") or collider.tags.__contains__("NoCollisionResponse") else True
        #check each edge against each other
        for i in range(len(verts)):
            A, B = verts[i], verts[(i+1)%len(verts)]
            AB = B-A
            normalAB = AB.Perp().Normalize()
            
            for k in range(len(collVerts)):
                C, D = collVerts[k], collVerts[(k+1)%len(collVerts)]
                CD = D-C
                normalCD = CD.Perp().Normalize()
                
                #keep going if edge normals are mostly opposed, should only ever be one possible per current edge
                if normalAB.Dot(normalCD) < -1 + self._edgeAlignmentMargin:
                    #get closest vertex of other edge to current own edge
                    Vc, onLine, collisionDistance = Vec2(0,0), False, 0.0
                    Vc, onLine, collisionDistance = self.ClosesetPointToSegment(Vc,onLine,collisionDistance,A,B,[C,D])
                    
                    #check if closest point to edge is inside the rectangle
                    inside = True
                    for i in range(len(verts)):
                        _AB = verts[(i+1)%4] - verts[i]
                        AVc = Vc - verts[i]
                        normal = Vec2(-_AB.y,_AB.x)
                        if AVc.Dot(normal) >= 0:
                            inside = False
                            break
                    
                                        
                    #edge probably inside if true
                    if inside and (Vc-A).Dot(normalAB) < 0 and onLine:
                        relativeVelocity = self.GetRelativeVelocity(collider,self.parent.GetComponent("Transform").position, collider.parent.GetComponent("Transform").position)
                        print("ObjectA: %s, normal %s, combVel: %s, dot: %s" %(self.parent.GetID(), normalAB, relativeVelocity, normalAB.Dot(relativeVelocity)))
                        #choose edge that faces away from relative velocity
                        if normalAB.Dot(relativeVelocity) < 0:
                            #get closest vertex of current edge to other edge for additional info
                            Pc, onLine_, d_ = Vec2(0,0), False, 0.0
                            Pc, onLine_, d_ = self.ClosesetPointToSegment(Pc,onLine_,d_,C,D,[A,B])
                            edgeVec = (Pc + (Pc - A - B)).Normalize() * -1
                            self.collisions.append(CollisionInfo(Pc,collisionDistance,normalAB,normalCD, edgeVec, self.parent, collider.parent,"edge", collisionResponseTag))
                            return True
        return False
    
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
            
    def ClosesetPointToSegment(self,Vc,onLine,d,A,B,verts):
        SqDC, SqDD = 0, 0
        SqDC, onLine = self.SqDistancePointSegment(SqDC,onLine,A,B,verts[0]) #square distance from C to edge
        SqDD, onLine = self.SqDistancePointSegment(SqDD,onLine,A,B,verts[1]) #square distance from D to edge
        if SqDC < SqDD:
            Vc = verts[0]
            d = math.sqrt(SqDC)
        else:
            Vc = verts[1]
            d = math.sqrt(SqDD)
        return (Vc, onLine, d)

                
    def CheckCollisionVertEdge(self,collider,verts,collVerts):
        #if furthest vertices aren't in range (within a safety margin), don't bother checking
        # if (self.parent.GetComponent("Transform").position - collider.parent.GetComponent("Transform").position).SqMag() > self.sqRadius + collider.sqRadius + self._safetyMargin:
        #     return
        collisionResponseTag = False if self.tags.__contains__("NoCollisionResponse") or collider.tags.__contains__("NoCollisionResponse") else True
        for p in collVerts:
            inside = True
            for i in range(len(verts)):
                AB = verts[(i+1)%4] - verts[i]
                AP = p - verts[i]
                normal = Vec2(-AB.y,AB.x)
                if AP.Dot(normal) >= 0:
                    inside = False
                    break
            if inside:
                relativeVelocity = self.GetRelativeVelocity(collider,p,p)
                minDot = 0 #i think there should always be a normal going the other way and thus at least one or two dot products should be below zero
                minNormal = None
                #find face whose normal most opposes direction of relative velocity, i.e. normal that was most likely hit
                for i in range(len(verts)):
                    ab = verts[(i+1)%4]-verts[i]
                    n = Vec2(-ab.y,ab.x)
                    if relativeVelocity.Dot(n) < minDot:
                        minDot = relativeVelocity.Dot(n)
                        minNormal = n
                        collisionDistance = ((p-verts[i]).ProjectedOn(ab)).Mag()
                self.collisions.append(CollisionInfo(p, collisionDistance, minNormal.Normalized(), None, None, self.parent, collider.parent, "vertEdge", collisionResponseTag))
                return
    
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
            
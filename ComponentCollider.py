from Vector import Vec2
import Component

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
        
    def BoolCollision(self, colliders):
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
                        normal = Vec2(-AB.y,AB.x)
                        AP = p - verts[i]
                        if AP.Dot(normal) >= 0:
                            inside = False
                            break
                    if inside:
                        return True
        return False
    
    def GetVertices(self):#CCW starting top left if not rotated
        transf = self.parent.GetComponent("Transform")
        center = transf.position+self.localPosition
        A = center + Vec2(-self.lenX/2,-self.lenY/2).Rotate(transf.rotation+self.localRotation)
        B = center + Vec2(-self.lenX/2, self.lenY/2).Rotate(transf.rotation+self.localRotation)
        C = center + Vec2( self.lenX/2, self.lenY/2).Rotate(transf.rotation+self.localRotation)
        D = center + Vec2( self.lenX/2,-self.lenY/2).Rotate(transf.rotation+self.localRotation)
        return [A,B,C,D]
import math

class Vec2:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def __add__(self,other):
        return Vec2(self.x+other.x,self.y+other.y)
    
    def __sub__(self,other):
        return Vec2(self.x-other.x,self.y-other.y)
    
    def __mul__(self,scalar): #other must be a scalar
        return Vec2(self.x*scalar,self.y*scalar)
    
    def __div__(self,scalar): #other must be a scalar
        return Vec2(self.x/scalar,self.y/scalar)
    
    def Dot(self,other):
        return self.x*other.x+self.y*other.y
    
    def Mag(self):
        return math.sqrt((self.x**2)+(self.y**2))
    
    def SqMag(self):
        return (self.x**2)+(self.y**2)
    
    def Normalize(self):
        mag = self.Mag()
        self.x /= mag
        self.y /= mag
        return Vec2(self.x,self.y)
    
    def Normalized(self):
        mag = self.Mag()
        return Vec2(self.x/mag,self.y/mag)
    
    def AngleBetween(self,other):
        return math.acos(self.Dot(other)/(self.Mag()*other.Mag()))
    
    def ProjectedOn(self,other):
        return other * (self.Dot(other) / other.SqMag())
    
    def Rotate(self,angle,offset): #in radians, maybe offset should be added instead, testing required
        return Vec2((self.x-offset.x) * math.cos(angle)-(self.y-offset.y) * math.sin(angle),(self.x-offset.x) * math.sin(angle) + (self.y-offset.y) * math.cos(angle))
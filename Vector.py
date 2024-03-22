import math

class Vec2:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return "<%.2f, %.2f>"%(self.x,self.y)
    
    def __add__(self,other):
        return Vec2(self.x+other.x,self.y+other.y)
    
    def __sub__(self,other):
        return Vec2(self.x-other.x,self.y-other.y)
    
    def __mul__(self,scalar):
        return Vec2(self.x * scalar,self.y*scalar)
    
    def __div__(self,scalar):
        return Vec2(self.x/scalar,self.y/scalar)
    
    def __neg__(self):
        return Vec2(-self.x,-self.y)
    
    def Dot(self,other):
        return self.x*other.x+self.y*other.y
    
    def Mag(self):
        return math.sqrt((self.x**2)+(self.y**2))
    
    def SqMag(self):
        return (self.x**2)+(self.y**2)
    
    def Perp(self):
        return Vec2(-self.y,self.x)
    
    def Normalize(self):
        mag = self.Mag()
        if mag == 0:
            return self
        self.x /= mag
        self.y /= mag
        return self
    
    def Normalized(self):
        mag = self.Mag()
        return Vec2(self.x/mag,self.y/mag)
    
    def AngleBetween(self,other): #in radians between 0 and pi
        if self.Dot(other)/(self.Mag()*other.Mag()) > 1:
            return 0.0
        return math.acos(self.Dot(other)/(self.Mag()*other.Mag()))
    
    def ProjectedOn(self,other):
        '''Returns the projection of self (self: Point - Vector begin) onto vector'''
        return other * (self.Dot(other) / other.SqMag())
    
    def Rotate(self,angle): #in radians
        return Vec2(self.x * math.cos(angle)-self.y * math.sin(angle),self.x * math.sin(angle) + self.y * math.cos(angle))
    
    def Slerp(p, q ,t): #spherical lerp
        theta = p.AngleBetween(q)
        w_p = math.sin((1-t)*theta)/math.sin(theta)
        w_q = math.sin(theta * t)/math.sin(theta)
        return p * w_p + q * w_q
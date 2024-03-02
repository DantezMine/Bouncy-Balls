import Component
from Vector import Vec2

class ComponentTransform(Component.Component):
    def __init__(self):
        self.position = Vec2(0,0)
        self.rotation = 0 #in radians
        self.scale = Vec2(1,1)
        self.up = Vec2(0,-1)
        self.forward = Vec2(1,0)
    
    def Rotate(self,angle):
        self.rotation += angle
        self.forward.Rotate(angle)
        self.up.Rotate(angle)
        
    def LookAt(self,gameObj):
        da = self.forward.AngleBetween(gameObj.GetComponent("Transform").position-self.position) #angle between forward and gameObj
        self.Rotate(da)
        
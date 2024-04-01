import json
from Components import Component
from Components.Component import Components
from Vector import Vec2
from lib import GlobalVars

class ComponentTransform(Component.Component):
    def __init__(self):
        self.name = Components.Transform
        self.parent = None
        
        self.position = Vec2(0,0)
        self.rotation = 0 #in radians
        self.scale = 1
        self.up = Vec2(0,-1)
        self.forward = Vec2(1,0)
    
    def Rotate(self,angle):
        self.rotation += angle
        self.forward.Rotate(angle)
        self.up.Rotate(angle)
        
    def LookAt(self,targetPos):
        da = self.forward.AngleBetween(targetPos-self.position) #angle between forward and target
        self.Rotate(da)
        
    def WorldToScreenPos(self,pos,camera):
        width = GlobalVars.screen.get_width()
        height = GlobalVars.screen.get_height()
        xScreen =        (pos.x*camera.scale + 1)*width /2.0
        yScreen = height-(pos.y*camera.scale + 1)*height/2.0
        return Vec2(xScreen,yScreen)
    
    def ScreenToWorldPos(self,pos,camera):
        width = GlobalVars.screen.get_width()
        height = GlobalVars.screen.get_height()
        xWorld = (pos.x*2.0/width - 1)/camera.scale
        yWorld = ((height-pos.y)*2.0/height - 1)/camera.scale
        return Vec2(xWorld,yWorld)
        
    def Encode(self,obj):
        return {
            "name" : obj.name.Encode(),
            "parentID" : obj.parent.GetID(),
            "position" : obj.position.Encode(),
            "rotation" : obj.rotation,
            "scale" : obj.scale,
            "up" : obj.up.Encode(),
            "forward" : obj.forward.Encode()
        }
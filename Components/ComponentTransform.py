import json
from . import Component
from Vector import Vec2
import GlobalVars
from Components.Component import ComponentType

class TransformState:
    def __init__(self, transform):
        self.position = transform.position
        self.rotation = transform.rotation
        self.scale    = transform.scale
        self.up       = transform.up
        self.forward  = transform.forward

class Transform(Component.Component):
    def __init__(self):
        self.name = Component.ComponentType.Transform
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
        
    def WorldToScreenPos(pos,camera):
        width = GlobalVars.screen.get_width()
        height = GlobalVars.screen.get_height()
        camTransf = camera.parent.GetComponent(ComponentType.Transform)
        xScreen =        ((pos.x-camTransf.position.x)*camera.scale + 1)*width /2.0
        yScreen = height-((pos.y-camTransf.position.y)*camera.scale + 1)*height/2.0
        return Vec2(xScreen,yScreen)
    
    def ScreenToWorldPos(pos,camera):
        width = GlobalVars.screen.get_width()
        height = GlobalVars.screen.get_height()
        camTransf = camera.parent.GetComponent(ComponentType.Transform)
        xWorld = (pos.x*2.0/width - 1)/camera.scale + camTransf.position.x
        yWorld = ((height-pos.y)*2.0/height - 1)/camera.scale + camTransf.position.y
        return Vec2(xWorld,yWorld)
    
    def SaveState(self):
        return TransformState(self)
    
    def LoadState(self,state):
        self.position = state.position
        self.rotation = state.rotation
        self.scale    = state.scale
        self.up       = state.up
        self.forward  = state.forward
        
    def Decode(self, obj):
        super().Decode(obj)
        self.position = Vec2.FromList(obj["position"])
        self.rotation = obj["rotation"]
        self.scale = obj["scale"]
        self.up = Vec2.FromList(obj["up"])
        self.forward = Vec2.FromList(obj["forward"])
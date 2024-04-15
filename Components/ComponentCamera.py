from Components import Component
from Vector import Vec2

class Camera(Component.Component):
    def __init__(self, position = Vec2(0,0), scale = 1):
        self.name = Component.ComponentType.Camera
        self.parent = None
        self.initPos = position
        self.scale = scale #factor by which the scene scales, or zoom factor ; greater -> more zoomed in
    
    def Start(self):
        self.transform = self.parent.GetComponent(Component.ComponentType.Transform)
    
    def Decode(self, obj):
        super().Decode(obj)
        self.scale = obj["scale"]
        self.initPos = Vec2.FromList(obj["initPos"])
from Components import Component
from Vector import Vec2
import time
import ComponentBall

class Camera(Component.Component):
    def __init__(self, position = Vec2(0,0), scale = 1, boundLenX, boundLenY):
        self.name = Component.ComponentType.Camera
        self.parent = None
        self.initPos = position
        self.scale = scale #factor by which the scene scales, or zoom factor ; greater -> more zoomed in
        self.boundLenX = boundLenX
        self.boundLenY = boundLenY
    
    # def Start(self):
    #     self.transform = self.parent.GetComponent(Component.ComponentType.Transform)
    
    def Decode(self, obj):
        super().Decode(obj)
        self.scale = obj["scale"]
        self.initPos = Vec2.FromList(obj["initPos"])
        
        
        
    def Follow(self, ComponentBall):
        
        ballTransform = Ball.parent.GetComponent(ComponentType.Transform)
        
        if abs(Vec2.y) < (1/self.scale):
            dy = (1/self.scale) - Vec2.y
        else:
            dy = 0
        targetY = ballTransform.position.y + dy #Vec2.y but from the target (here the ball), where can i get that from?
        
        pass
        
    def Update(self, deltaTime, C, B, t):
        self.C = C
        self.B = B
        self.t = t
        
        C = Vec2.x, Vec2.y
        B = Vec2.x, Vec2.y #but from the target, same question as above
        lerp = C + (C-B)*deltaTime
        pass
    
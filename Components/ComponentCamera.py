from Components import Component
from Components.Component import ComponentType
from Vector import Vec2
import math

class Camera(Component.Component):
    def __init__(self, position = Vec2(0,0), scale = 1, boundLen = Vec2(5,5)):
        self.name = Component.ComponentType.Camera
        self.parent = None
        self.initPos = position
        self.scale = scale #factor by which the scene scales, or zoom factor ; greater -> more zoomed in ; screen length = 2/scale
        self.boundLen = boundLen
        
    def Update(self, deltaTime):
        self.scene = self.parent.GetParentScene()
        balls = self.scene.GetObjectsWithComponent(ComponentType.Ball)
        for ball in balls:
            ballPosition = ball.GetComponent(ComponentType.Transform).position
        self.MoveCamera(ballPosition)
        
    def EnforceBounds(self):
        def sign(x):
            if x == 0:
                return 0
            return -1 if x < 0 else 1
         
        transform = self.parent.GetComponent(ComponentType.Transform)
        signedDist = Vec2(1,1)/self.scale - self.boundLen/2.0 + abs(transform.position)
        signedDist.x = max(0,signedDist.x) * sign(transform.position.x)
        signedDist.y = max(0,signedDist.y) * sign(transform.position.y)
        transform.position -= signedDist
        
    def MoveCamera(self, position):
        self.parent.GetComponent(ComponentType.Transform).position = position
        self.EnforceBounds()
        
    def ScaleCamera(self, scale):
        self.scale = scale
        self.EnforceBounds()
        
    def Decode(self, obj):
        super().Decode(obj)
        self.scale = obj["scale"]
        self.initPos = Vec2.FromList(obj["initPos"])
from Components import Component
from Components.Component import ComponentType
from Components.Component import ComponentType
from Vector import Vec2
import math
import math

class Camera(Component.Component):
    def __init__(self, position = Vec2(0,0), scale = 1, boundLen = None, free = False):
        self.name = Component.ComponentType.Camera
        self.parent = None
        self.initPos = position
        self.scale = scale #factor by which the scene scales, or zoom factor ; greater -> more zoomed in ; screen length = 2/scale
        self.minimalBound = Vec2(2/scale,2/scale)
        self.boundLen = self.minimalBound if boundLen is None else boundLen
        self.free = free
        
        
    def Start(self):
        self.parent.GetComponent(ComponentType.Transform).position = self.initPos
        
    def Update(self, deltaTime):
        if not self.free:
            if self.boundLen.x >= self.minimalBound.x:
                if self.boundLen.y >= self.minimalBound.y:
                    self.scene = self.parent.GetParentScene()
                    balls = self.scene.GetObjectsWithComponent(ComponentType.Ball)
                    ballPosition = None
                    for ball in balls:
                        ballPosition = ball.GetComponent(ComponentType.Transform).position
                    if ballPosition is not None:
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
        self.boundLen = Vec2.FromList(obj["boundLen"]) if isinstance(obj["boundLen"],list) else obj["boundLen"]
        self.minimalBound = Vec2(2/self.scale,2/self.scale)
        self.boundLen = self.minimalBound if self.boundLen is None else self.boundLen
        self.free = obj["free"]
from Components.Component import ComponentType
from Components import ComponentTransform
from Components import ComponentCollider
from Components import ComponentPhysics
from Components import ComponentSprite
from Components import Component
import GlobalVars
from Vector import Vec2
import GlobalVars
import enum
import pygame
import math

class BallType(enum.Enum):
    Bouncy = enum.auto()
    Heavy = enum.auto()

    def Decode(value):
        members = list(vars(BallType).values())
        members = members[GlobalVars.membersOffset:len(members)-1]
        for member in members:
            if value == member.value:
                return member

class Ball(Component.Component):
    def __init__(self):
        self.name = ComponentType.Ball
        self.parent = None
    
    def Start(self):
        self.radius = 0.2
        circColl = ComponentCollider.ColliderCircle(radius=self.radius)
        self.parent.AddComponent(circColl)
        physics = ComponentPhysics.Physics()
        physics.constraintPosition = True
        physics.constraintRotation = True
        self.parent.AddComponent(physics)
        
    def Update(self, deltaTime):
        if not self.IsInBound():
            self.parent.GetParentScene().GetComponents(ComponentType.Cannon)[0].NextBall()

    def IsInBound(self):
        camera = self.parent.GetParentScene().camera
        boundCenter = camera.parent.GetComponent(ComponentType.Transform).position
        boundLen = camera.boundLen
        transform = self.parent.GetComponent(ComponentType.Transform)
        if transform.position.x + self.radius < boundCenter.x - boundLen.x or transform.position.x - self.radius > boundCenter.x + boundLen.x:
            return False
        if transform.position.y + self.radius < boundCenter.y - boundLen.y or transform.position.y - self.radius > boundCenter.y + boundLen.y:
            return False
        return True

    def ProjectPath(self, steps, impulse):
        path = self.GetPath(steps, impulse)
        camera = self.parent.GetParentScene().camera
        for i in range(steps//5):
            point = ComponentTransform.Transform.WorldToScreenPos(path[i*5], camera)
            pygame.draw.circle(GlobalVars.foreground,(255,255,255),(point.x,point.y),5)
    
    def GetPath(self,steps, impulse):
        physics : ComponentPhysics = self.parent.GetComponent(ComponentType.Physics)
        collider : ComponentCollider = self.parent.GetComponent(ComponentType.Collider)
        transform = self.parent.GetComponent(ComponentType.Transform)
        
        #save state
        transformState = transform.SaveState()
        physicsState = physics.SaveState()
        
        physics.constraintPosition = False
        physics.constraintRotation = False
        physics.AddImpulse(impulse)
        #project next n timesteps, if a collision occurs with a structure, the projection stops
        path = []
        for i in range(steps):
            for k in range(GlobalVars.updateFrequency):
                colliders = self.parent.GetParentScene().GetComponents(ComponentType.Collider)
                collider.Update(None,colliders,False)
                physics.Update(1/60.0,collider.collisions,3)
                path.append(transform.position)
        
        #load state
        physics.LoadState(physicsState)
        transform.LoadState(transformState)
        return path
      
    def OnClick(self):
        pass
    
    def Decode(self, obj):
        super().Decode(obj)
        self.radius = obj["radius"]
        self.ballType = BallType.Decode(obj["ballType"])
    
class BallBouncy(Ball):
    '''type : "Bouncy"'''
    def __init__(self):
        super().__init__()
        self.ballType = BallType.Bouncy
    
    def Start(self):
        self.radius = 0.15
        circColl = ComponentCollider.ColliderCircle(radius=self.radius,tags=["Ball"])
        self.parent.AddComponent(circColl)
        physics = ComponentPhysics.Physics()
        physics.constraintPosition = True
        physics.constraintRotation = True
        physics.mass = 1.8
        physics.restitution = 0.8
        self.parent.AddComponent(physics)
        self.parent.AddComponent(ComponentSprite.Sprite(spritePath="data/TennisBall.PNG", diameter=self.radius*2))

class BallBowling(Ball):
    '''type : "Heavy"'''
    def __init__(self):
        super().__init__()
        self.ballType = BallType.Heavy
    
    def Start(self):
        self.radius = 0.3
        circColl = ComponentCollider.ColliderCircle(radius=self.radius,tags=["Ball"])
        self.parent.AddComponent(circColl)
        physics = ComponentPhysics.Physics()
        physics.constraintPosition = True
        physics.constraintRotation = True
        physics.mass = 1.5
        physics.restitution = 0.1
        self.parent.AddComponent(physics)
        self.parent.AddComponent(ComponentSprite.Sprite(spritePath="data/BowlingBall.PNG", diameter=self.radius*2))
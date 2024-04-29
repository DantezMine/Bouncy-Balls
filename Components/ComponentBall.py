from Components.Component import ComponentType
from Components import ComponentTransform
from Components import ComponentCollider
from Components import ComponentPhysics
from Components import ComponentSprite
from Components import Component
from lib import GlobalVars
from Vector import Vec2
from lib import GlobalVars
import enum
import pygame
import math

class BallType(enum.Enum):
    Bouncy = enum.auto()
    Heavy = enum.auto()
    
    def Decode(value):
        members = list(vars(BallType).values())
        members = members[8:len(members)-1]
        for member in members:
            if value == member.value:
                return member

class Ball(Component.Component):
    def __init__(self, sling = None):
        self.name = ComponentType.Ball
        self.parent = None
        self.state = "Origin"
        self.sling = sling
        self.mousePosStart = None
        GlobalVars.mousePressed = False
        self.mouseLeft = False
        self.slingD = 10
    
    def Start(self):
        self.radius = 0.2
        circColl = ComponentCollider.ColliderCircle(radius=self.radius)
        self.parent.AddComponent(circColl)
        physics = ComponentPhysics.Physics()
        physics.constraintPosition = True
        physics.constraintRotation = True
        self.parent.AddComponent(physics)
        
    def Update(self, deltaTime):
        if self.sling is None:
            self.sling = self.parent.GetParentScene().GameObjectWithID(self.slingID)
        slingTransform = self.sling.GetComponent(ComponentType.Transform)
        transform = self.parent.GetComponent(ComponentType.Transform)
        
        mousePosWorld = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen, self.parent.GetParentScene().camera)
        self.parent.GetComponent(ComponentType.Collider).DisplayCollider()
        if self.state == "Origin":
            transform.position = slingTransform.position
        if GlobalVars.mousePressed:
            if self.state == "Origin" and GlobalVars.mouseLeft:
                self.mousePosStart = mousePosWorld
                self.state = "Dragged"
            if self.state == "Dragged" and mousePosWorld:
                mousePos = mousePosWorld
                deltaVec = slingTransform.position - mousePosWorld
                delta = deltaVec.Mag()
                deltaNorm = deltaVec.Normalized()
                transform.position = slingTransform.position + deltaNorm * 0.25
                impulse = deltaNorm * math.log(1.5*delta + 1) * self.slingD
                self.ProjectPath(40,impulse)
            if self.state == "Released" and self.mouseLeft:
                self.OnClick()
        
        if not GlobalVars.mousePressed:
             if self.state == "Dragged":
                self.state = "Released"
                delta = self.mousePosStart - self.mousePos
                force = delta * self.slingD
                self.parent.GetComponent(Components.Physics).AddForce(force)
                deltaVec = self.mousePosStart - mousePosWorld
                delta = deltaVec.Mag()
                deltaNorm = deltaVec.Normalized()
                impulse = deltaNorm * math.log(1.5*delta + 1) * self.slingD

                physics = self.parent.GetComponent(ComponentType.Physics)
                physics.constraintPosition = False
                physics.constraintRotation = False
                physics.AddImpulse(impulse)
       
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
        transform = self.parent.GetComponent(Components.Transform)
        camera = self.parent.GetParentScene().camera
        for i in range(steps//5):
            point = transform.WorldToScreenPos(path[i*5], camera)
            pygame.draw.circle(GlobalVars.foreground,(255,255,255),(point.x,point.y),5)
        
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
        self.state = obj["state"]
        self.slingID = obj["sling"]
        self.slingD = obj["slingD"]
        self.ballType = BallType.Decode(obj["ballType"])
    
class BallBouncy(Ball):
    '''type : "Bouncy"'''
    def __init__(self, sling = None):
        super().__init__(sling)
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
    def __init__(self, sling = None):
        super().__init__(sling)
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

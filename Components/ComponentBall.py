from Components.Component import Components
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
    
    def Encode(self):
        return self.name

class Ball(Component.Component):
    def __init__(self, sling):
        self.name = Components.Ball
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
        mousePosWorld = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen, self.parent.GetParentScene().camera)
        
        self.parent.GetComponent(Components.Collider).DisplayCollider()
        if self.state == "Origin":
            self.parent.GetComponent(Components.Transform).position = self.sling.GetComponent(Components.Transform).position
        if GlobalVars.mousePressed:
            if self.state == "Origin" and GlobalVars.mouseLeft:
                self.mousePosStart = mousePosWorld
                self.state = "Dragged"
            if self.state == "Dragged" and mousePosWorld:
                deltaVec = self.mousePosStart - mousePosWorld
                delta = deltaVec.Mag()
                deltaNorm = deltaVec.Normalized()
                self.parent.GetComponent(Components.Transform).position = self.sling.GetComponent(Components.Transform).position - deltaNorm * math.log(1.5*delta + 1)
                impulse = deltaNorm * math.log(1.5*delta + 1) * self.slingD
                self.ProjectPath(40,impulse)
            if self.state == "Released" and self.mouseLeft:
                self.OnClick()
        if not GlobalVars.mousePressed:
             if self.state == "Dragged":
                self.state = "Released"
                deltaVec = self.mousePosStart - mousePosWorld
                delta = deltaVec.Mag()
                deltaNorm = deltaVec.Normalized()
                impulse = deltaNorm * math.log(1.5*delta + 1) * self.slingD
                physics = self.parent.GetComponent(Components.Physics)
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
        physics : ComponentPhysics = self.parent.GetComponent(Components.Physics)
        collider : ComponentCollider = self.parent.GetComponent(Components.Collider)
        transform = self.parent.GetComponent(Components.Transform)
        
        #save state
        transformState = transform.SaveState()
        physicsState = physics.SaveState()
        
        physics.constraintPosition = False
        physics.constraintRotation = False
        physics.AddImpulse(impulse)
        #project next n timesteps, if a collision occurs with a structure, the projection stops
        path = []
        for i in range(steps):
            colliders = self.parent.GetParentScene().GetComponents(Components.Collider)
            collider.Update(None,colliders,False)
            physics.Update(1/60.0,collider.collisions,3)
            path.append(transform.position)
        
        #load state
        physics.LoadState(physicsState)
        transform.LoadState(transformState)
        return path
      
    def OnClick(self):
        pass
    
    def Encode(self,obj):
        outDict = super(Ball,self).Encode(obj)
        outDict["radius"] = obj.radius
        outDict["state"] = obj.state
        outDict["sling"] = obj.sling.GetID()
        outDict["slingD"] = obj.slingD
        outDict["ballType"] = obj.ballType.Encode()
    
class BallBouncy(Ball):
    '''type : "Bouncy"'''
    def __init__(self, sling):
        super().__init__(sling)
        self.ballType = BallType.Bouncy
    
    def Start(self):
        self.radius = 0.2
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
    def __init__(self, sling):
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

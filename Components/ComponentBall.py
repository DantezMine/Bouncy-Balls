from Components.Component import Components
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
    Normal = enum.auto()
    
    def Encode(self):
        return self.name

class Ball(Component.Component):
    def __init__(self, sling):
        self.name = Components.Ball
        self.parent = None
        self.state = "Origin"
        self.sling = sling
        self.mousePosStart = None
        self.mousePressed = False
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
        mousePos = pygame.mouse.get_pos()
        mousePos = Vec2(mousePos[0],mousePos[1])
        mousePosWorld = self.parent.GetComponent(Components.Transform).ScreenToWorldPos(mousePos, self.parent.GetParentScene().camera)
        for event in GlobalVars.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mousePressed = True
                if event.button == 1:
                    self.mouseLeft = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mousePressed = False
                self.mouseLeft = False
        
        self.parent.GetComponent(Components.Collider).DisplayCollider()
        if self.state == "Origin":
            self.parent.GetComponent(Components.Transform).position = self.sling.GetComponent(Components.Transform).position
        if self.mousePressed:
            if self.state == "Origin" and self.mouseLeft:
                self.mousePosStart = mousePosWorld
                self.state = "Dragged"
            if self.state == "Dragged" and mousePosWorld:
                mousePos = mousePosWorld
                deltaVec = self.mousePosStart - mousePosWorld
                delta = deltaVec.Mag()
                deltaNorm = deltaVec.Normalized()
                self.parent.GetComponent(Components.Transform).position = self.sling.GetComponent(Components.Transform).position - deltaNorm * math.log(1.5*delta + 1)
                impulse = deltaNorm * math.log(1.5*delta + 1) * self.slingD
                self.ProjectPath(40,impulse)
            if self.state == "Released" and self.mouseLeft:
                self.OnClick()
        if not self.mousePressed:
             if self.state == "Dragged":
                self.state = "Released"
                delta = self.mousePosStart - self.mousePos
                force = delta * self.slingD
                self.parent.GetComponent(Components.Physics).AddForce(force)
       
      
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
        physics.mass = 0.8
        physics.restitution = 0.8
        self.parent.AddComponent(physics)
        self.parent.AddComponent(ComponentSprite.Sprite(spritePath="data/TennisBall.PNG", diameter=self.radius*2))
        self.parent.GetComponent(Components.Collider).tags = ["Ball"]
        

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

class BallSdlyBig(Ball):
    '''type : "Normal"'''
    def __init__(self, sling, scale):
        super().__init__(sling)
        self.ballType = BallType.Normal
        self.scale = scale
    
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
        self.parent.AddComponent(ComponentSprite.Sprite(spritePath="data/TennisBall.PNG", diameter=self.radius*2))
    
    def OnClick(self):
        self.radius = 0.5
        self.parent.AddComponent(ComponentCollider.ColliderCircle(radius=self.radius,tags=["Ball"]))
        self.parent.AddComponent(ComponentSprite.Sprite(spritePath="data/TennisBall.PNG", diameter=self.radius*2))
        
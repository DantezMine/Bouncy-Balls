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
import enum

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
        self.slingD = 40
    
    def Start(self):
        self.radius = 50
        circColl = ComponentCollider.ColliderCircle(radius=self.radius)
        self.parent.AddComponent(circColl)
        self.parent.AddComponent(ComponentPhysics.Physics())
        
    def Update(self, deltaTime):
        mousePressed = False
        mouseLeft = False
        mousePos = Vec2(0,0)
        for event in GlobalVars.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = True
                mousePos = Vec2(event.pos[0],event.pos[1])
                if event.button == pygame.BUTTON_LEFT:
                    mouseLeft = True
        
        self.parent.GetComponent(Components.Collider).DisplayCollider()
        if self.state == "Origin":
            self.parent.GetComponent(Components.Transform).position = self.sling.GetComponent(Components.Transform).position
        if mousePressed:
            if self.state == "Origin" and mouseLeft:
                self.mousePosStart = mousePos
                self.state = "Dragged"
            if self.state == "Dragged" and mouseLeft:
                self.mousePos = mousePos
                delta = self.mousePosStart - self.mousePos
                self.parent.GetComponent(Components.Transform).position = self.sling.GetComponent(Components.Transform).position - delta
            if self.state == "Released" and mouseLeft:
                self.OnClick()
        if not mousePressed:
             if self.state == "Dragged":
                self.state = "Released"
                delta = self.mousePosStart - self.mousePos
                force = delta * self.slingD
                self.parent.GetComponent(Components.Physics).AddForce(force)
       
    def ProjectPath(self, steps):
        path = self.GetPath(steps)
        transform = self.parent.GetComponent(Components.Transform)
        camera = self.parent.GetParentScene().camera
        for i in range(steps//5):
            point = transform.WorldToScreenPos(path[i*5], camera)
            pygame.draw.circle(GlobalVars.foreground,(255,255,255),(point.x,point.y),5)
    
    def GetPath(self,steps):
        physics : ComponentPhysics = self.parent.GetComponent(Components.Physics)
        collider : ComponentCollider = self.parent.GetComponent(Components.Collider)
        transform = self.parent.GetComponent(Components.Transform)
        
        #save state
        transformState = transform.SaveState()
        physicsState = physics.SaveState()
        
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
        self.radius = 0.3
        circColl = ComponentCollider.ColliderCircle(radius=self.radius,tags=["Ball"])
        self.parent.AddComponent(circColl)
        self.parent.AddComponent(ComponentPhysics.Physics())
        self.parent.GetComponent(Components.Physics).restitution = 0.8
        self.parent.GetComponent(Components.Physics).mass = 0.08
        self.parent.AddComponent(ComponentSprite.Sprite(spritePath="data/TennisBall.PNG", diameter=self.radius*2))
        

class BallBowling(Ball):
    '''type : "Heavy"'''
    def __init__(self, sling):
        super().__init__(sling)
        self.ballType = BallType.Heavy
    
    def Start(self):
        self.radius = 0.4
        circColl = ComponentCollider.ColliderCircle(radius=self.radius,tags=["Ball"])
        self.parent.AddComponent(circColl)
        self.parent.AddComponent(ComponentPhysics.Physics())
        self.parent.GetComponent(Components.Physics).restitution = 0.1
        self.parent.GetComponent(Components.Physics).mass = 0.15
        self.parent.AddComponent(ComponentSprite.Sprite(spritePath="data/BowlingBall.PNG", diameter=self.radius*2))

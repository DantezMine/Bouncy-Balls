import ComponentSprite
import ComponentCollider
import ComponentPhysics
import Component
from Vector import Vec2

class Ball(Component.Component):
    def __init__(self):
        self.name = "Ball"
        self.parent = None
        self.state = "Origin"
        self.sling = None
        self.mousePosStart = None
        self.slingD = 40
    

    def Start(self):
        circColl = ComponentCollider.ColliderCircle()
        circColl.SetCollider(50)
        self.parent.AddComponent(circColl)
        self.parent.AddComponent(ComponentPhysics.Physics())
        
        
    def Update(self, deltaTime):
        self.parent.GetComponent("Collider").DisplayCollider()
        if self.state == "Origin":
            self.parent.GetComponent("Transform").position = self.sling.GetComponent("Transform").position
        if mousePressed:
            if self.state == "Origin" and mouseButton == 37:
                self.mousePosStart = Vec2(mouseX, mouseY)
                self.state = "Dragged"
            if self.state == "Dragged" and mouseButton == 37:
                self.mousePos = Vec2(mouseX, mouseY)
                delta = self.mousePosStart - self.mousePos
                self.parent.GetComponent("Transform").position = self.sling.GetComponent("Transform").position - delta
            if self.state == "Released" and mouseButton == 37:
                self.OnClick()
        if not mousePressed:
             if self.state == "Dragged":
                self.state = "Released"
                delta = self.mousePosStart - self.mousePos
                force = delta * self.slingD
                self.parent.GetComponent("Physics").AddForce(force)
        if self.state == "Released":
             self.parent.GetComponent("Physics").AddForce(Vec2(0, 60))
      
    def OnClick(self):
        pass




class BallBouncy(Ball):
    def Start(self):
        circColl = ComponentCollider.ColliderCircle()
        
        self.radius = 30
        circColl.SetCollider(radius=self.radius)
        self.parent.AddComponent(circColl)
        self.parent.AddComponent(ComponentPhysics.Physics())
        self.parent.GetComponent("Physics").restitution = 0.8
        self.parent.GetComponent("Physics").mass = 0.08
        self.parent.AddComponent(ComponentSprite.Sprite(s_spritePath="data/TennisBall.PNG", diameter=self.radius*2))
        

class BallBowling(Ball):
    def Start(self):
        circColl = ComponentCollider.ColliderCircle()
        self.radius = 60
        circColl.SetCollider(radius=self.radius)
        self.parent.AddComponent(circColl)
        self.parent.AddComponent(ComponentPhysics.Physics())
        self.parent.GetComponent("Physics").restitution = 0.1
        self.parent.GetComponent("Physics").mass = 0.15
        self.parent.AddComponent(ComponentSprite.Sprite(s_spritePath="data/BowlingBall.PNG", diameter=self.radius*2))

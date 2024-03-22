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
        self.startVelocity = Vec2(0,0)
        self.gravity = True

    def Start(self):
        circColl = ComponentCollider.ColliderCircle()
        circColl.SetCollider(50)
        self.parent.AddComponent(circColl)
        #self.parent.GetComponent("Physics").gravity = self.gravity
        
    def Update(self, deltaTime):
        self.parent.GetComponent("Collider").DisplayCollider()
        #print(self.parent.GetComponent("Physics").velocity)
        # if self.state == "Origin":
        #     self.parent.GetComponent("Transform").position = self.sling.GetComponent("Transform").position
        # if mousePressed:
        #     if self.state == "Origin" and mouseButton == 37:
        #         self.mousePosStart = Vec2(mouseX, mouseY)
        #         self.mousePos = Vec2(mouseX, mouseY)
        #         self.state = "Dragged"
        #     if self.state == "Dragged" and mouseButton == 37:
        #         self.mousePos = Vec2(mouseX, mouseY)
        #         self.Delta = self.mousePosStart - self.mousePos
        #         self.parent.GetComponent("Transform").position = self.sling.GetComponent("Transform").position - self.Delta
        # if not mousePressed:
        #     if self.state == "Dragged":
        #         self.state = "Released"
        #         self.Delta = self.mousePosStart - self.mousePos
        #         force = self.Delta * self.slingD
        #         self.parent.GetComponent("Physics").AddForce(force)
        # if self.state == "Released":
        #     self.parent.GetComponent("Physics").AddForce(Vec2(0, 60))
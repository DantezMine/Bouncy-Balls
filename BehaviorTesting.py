import ComponentSprite
import Component
from Vector import Vec2

class BehaviorTesting(Component.Component):
    def __init__(self):
        self.name = "BehaviorTesting"
        self.parent = None
    
    def Start(self):
        ballSprite = ComponentSprite.SpriteBallSlime(False, "SlimeBallMC.png")
        self.parent.AddComponent(ballSprite)
    
    def Update(self,deltaTime):
        self.parent.GetComponent("Transform").position = Vec2(mouseX,mouseY)
        self.parent.GetComponent("Transform").Rotate(deltaTime*1)
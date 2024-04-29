from Components import Component
from Components.Component import ComponentType
from Vector import Vec2
from Components import ComponentCollider

class GoalField(Component.Component):
    def __init__(self, position = Vec2(0,0), lenX = 50, lenY = 50, rotation = 0.0):
        self.name = ComponentType.GoalField
        self.parent = None
        self.initPos = position
        self.initRot = rotation
        self.lenX = lenX
        self.lenY = lenY
        self.success = False

    def Start(self):
        transform = self.parent.GetComponent(ComponentType.Transform)
        transform.position = self.initPos
        transform.rotation = self.initRot
               
        self.parent.AddComponent(ComponentCollider.ColliderRect(lenX = self.lenX, lenY = self.lenY))
        self.parent.GetComponent(ComponentType.Collider).tags = ["NoCollisionsResponse","GoalField"]

    def OnCollision(self, collider):
        if collider.tags.__contains__("Ball"):
            self.success = True
            print("True")
    
    def Update(self, deltaTime):
        self.parent.GetComponent(ComponentType.Collider).DisplayCollider()
    
    def Decode(self, obj):
        super().Decode(obj)
        self.lenX = obj["lenX"]
        self.lenY = obj["lenY"]
        self.success = obj["success"]
        self.initPos = Vec2.FromList(obj["initPos"])
        self.initRot = obj["initRot"]

from Components.Component import ComponentType
from Components import ComponentCollider
from Components import ComponentSprite
from Components import Component
from Vector import Vec2

class GoalField(Component.Component):
    def __init__(self, position = None, lenX = 0.5, lenY = 0.5, rotation = None):
        self.name = ComponentType.GoalField
        self.parent = None
        self.initPos = position
        self.initRot = rotation
        self.lenX = lenX
        self.lenY = lenY
        self.success = False

    def Start(self):
        transform = self.parent.GetComponent(ComponentType.Transform)
        transform.position = self.initPos if self.initPos is not None else transform.position
        transform.rotation = self.initRot if self.initRot is not None else transform.rotation
               
        self.parent.AddComponent(ComponentCollider.ColliderRect(lenX = self.lenX, lenY = self.lenY))
        self.parent.GetComponent(ComponentType.Collider).tags = ["NoCollisionsResponse","GoalField"]
        self.parent.AddComponent(ComponentSprite.Sprite(spritePath="data/GoalField.png",lenX=self.lenX,lenY=self.lenY))

    def OnCollision(self, collider):
        if collider.tags.__contains__("GoalStructure"):
            self.success = True
    
    def Update(self, deltaTime):
        self.parent.GetComponent(ComponentType.Collider).DisplayCollider()
    
    def Decode(self, obj):
        super().Decode(obj)
        self.lenX = obj["lenX"]
        self.lenY = obj["lenY"]
        self.success = obj["success"]
        self.initPos = Vec2.FromList(obj["initPos"]) if obj["initPos"] is not None else None
        self.initRot = obj["initRot"]
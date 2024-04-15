from Components import ComponentSprite
from Components import Component
from Components.Component import Components
from Vector import Vec2

class Background(Component.Component):
    def __init__(self, position = Vec2(0,0),lenX=50,lenY=50):
        self.name = Components.Background
        self.parent = None
        
        self.initPos = position
        self.lenX = lenX
        self.lenY = lenY
        
    def Start(self):
        self.parent.GetComponent(Components.Transform).position = self.initPos
        
    def Encode(self, obj):
        outDict = super().Encode(obj)
        outDict["lenX"] = obj.lenX
        outDict["lenY"] = obj.lenY

class BackgroundNature(Background):
    def Start(self):
        super().Start()
        self.parent.AddComponent(ComponentSprite.SpriteBackground("data/BackgroundNature-Sky.png",self.lenX,self.lenY))

class BackgroundSkyline(Background):
    def Start(self):
        super().Start()
        self.parent.AddComponent(ComponentSprite.SpriteBackground("data/BackgroundSkyline-Sky.png",self.lenX,self.lenY))
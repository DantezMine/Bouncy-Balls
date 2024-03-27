import Component

class Sprite(Component.Component):
    def __init__(self, spritePath = None, lenX = 50, lenY = 50, diameter = None): #s_spritePath must be given
        self.name = "Sprite"
        self.spritePath = spritePath
        self.parent = None
        self.lenX = diameter if diameter is not None else lenX
        self.lenY = diameter if diameter is not None else lenY
        
    def Update(self,deltaTime):
        self.DisplayImg()
    
    def DisplayImg(self):
        parentTransform = self.parent.GetComponent("Transform")
        sprite = loadImage(self.spritePath)
        pushMatrix()
        translate(parentTransform.position.x, parentTransform.position.y)
        rotate(parentTransform.rotation)
        image(sprite,-self.lenX*parentTransform.scale/2.0,-self.lenY*parentTransform.scale/2.0,self.lenX*parentTransform.scale,self.lenY*parentTransform.scale)
        popMatrix()
        
    def Encode(self,obj):
        outDict = {
            "name" : obj.name,
            "parentID" : obj.parent.GetID()
        }
        outDict["spritePath"] = obj.spritePath
        outDict["lenX"] = obj.lenX
        outDict["lenY"] = obj.lenY
        return outDict
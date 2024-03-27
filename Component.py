import json

class Component(object):
    def __init__(self):
        self.name = None #needs to be set in each component class individually
        self.parent = None
    
    def Start(self):
        pass
    
    def Update(self,deltaTime):
        pass
    
    def OnCollision(self,collider):
        pass
    
    def ToJSONstr(self):
        return json.dumps(obj=self,default=self.Encode,indent=4)
    
    def Encode(self,obj):
        outDict = {
            "name" : obj.name,
            "parentID" : obj.parent.GetID()
        }
        return outDict
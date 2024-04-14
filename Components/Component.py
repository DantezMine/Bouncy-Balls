import json
import enum

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
            "type" : obj.name.Encode() if type(obj.name) == ComponentType else obj.name,
            "parentID" : obj.parent.GetID()
        }
        return outDict
    
    def Decode(self,obj):
        pass
    
class ComponentType(enum.Enum):
    Transform = enum.auto()
    Physics = enum.auto()
    Sprite = enum.auto()
    Collider = enum.auto()
    Ball = enum.auto()
    Structure = enum.auto()
    Ground = enum.auto()
    Background = enum.auto()
    Camera = enum.auto()
    Cannon = enum.auto()
    GoalField = enum.auto()
    Button = enum.auto()
    Slider = enum.auto()
    
    def Encode(self):
        return self.value
    
    def GetType(compType):
        members = list(vars(ComponentType).values())
        members = members[9:len(members)-1]
        for ctype in members:
            if compType == ctype.value:
                return ctype
import json
import enum
from Vector import Vec2

class Component(object):
    def __init__(self):
        import GameObject
        self.name = None #needs to be set in each component class individually
        self.parent : GameObject.GameObject = None
    
    def Start(self):
        pass
    
    def Update(self,deltaTime):
        pass
    
    def OnCollision(self,collider):
        pass
    
    def ToJSONstr(self):
        return json.dumps(obj=self,default=self.Encode,indent=4)
    
    def Encode(self,obj):
        outDict = dict()
        members = vars(obj)
        for varName in members.keys():
            outDict[varName] = self.EncodeVariable(members[varName])
        return outDict
    
    def EncodeVariable(self, varValue):
        import GameObject
        if isinstance(varValue, enum.Enum):
            return varValue.value
        if isinstance(varValue, (int, float, str, bool)):
            return varValue
        if isinstance(varValue, Vec2):
            return varValue.Encode()
        if isinstance(varValue, GameObject.GameObject):
            return varValue.GetID()
    
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
    Base = enum.auto()
    Editor = enum.auto()
    
    def GetType(compType):
        members = list(vars(ComponentType).values())
        members = members[8:len(members)-1]
        for ctype in members:
            if compType == ctype.value:
                return ctype
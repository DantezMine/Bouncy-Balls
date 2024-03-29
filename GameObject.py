import json
import ComponentTransform
from Component import Components

class GameObject(object):
    def __init__(self, parentScene):
        self.__id = parentScene.CreateID()
        self.__components = {key: value for key, value in []} #initialize an empty dictionary using dictionary comprehension
        self.__parentScene = parentScene
        self.__isBackground = False
        
        self.AddComponent(ComponentTransform.ComponentTransform())
        
    def AddComponent(self, component):
        if self.__components.__contains__(component.name):
            print("Component already exists in object %d"%self.__id)
            return False
        self.__components[component.name] = component
        self.__components[component.name].parent = self
        component.Start()
        if component.name == Components.Background:
            self.__isBackground = True
        return True
    
    def RemoveComponent(self,componentName):
        if self.__components.__contains__(componentName):
            self.__components.pop(componentName)
            if componentName == Components.Background:
                self.__isBackground = False
            return True
        print("Component doesn't exist in object %d"%self.__id)
        return False
    
    def RemoveFromScene(self):
        self.__parentScene.RemoveGameObject(self)
    
    def GetComponent(self,compName):
        if self.__components.__contains__(compName):
            return self.__components[compName]
        #print("Component doesn't exist in object %d"%self.__id)
        return None
    
    def GetComponentNoPrint(self,compName):
        if self.__components.__contains__(compName):
            return self.__components[compName]
        return None
    
    def HasComponent(self,compName):
        return self.__components.__contains__(compName)
    
    def IsBackground(self):
        return self.__isBackground    
    
    def GetID(self):
        return self.__id
    
    def GetParentScene(self):
        return self.__parentScene
    
    def Start(self):
        pass
        # keysCopy = list(self.__components.keys()).copy()
        # for key in keysCopy:
        #     self.__components[key].Start()
    
    def Update(self,deltaTime):
        keysCopy = self.__components.keys()
        for key in keysCopy:
            if key != Components.Sprite and key != Components.Collider and key != Components.Physics:
                self.__components[key].Update(deltaTime)
    
    def UpdateCollider(self,deltaTime, colliders):
        if self.HasComponent(Components.Collider):
            self.__components[Components.Collider].Update(deltaTime, colliders)
    
    def UpdatePhysics(self,deltaTime,allCollisions,mode):
        if self.__components.__contains__(Components.Physics):
            self.__components[Components.Physics].Update(deltaTime,allCollisions,mode)
            
    def Show(self,deltaTime):
        if self.__components.__contains__(Components.Sprite):
            self.__components[Components.Sprite].Update(deltaTime)
            
    def UpdateOnCollision(self,collider):
        keys = list(self.__components.keys())[:]
        for key in keys:
            if self.__components.__contains__(key):
                self.__components[key].OnCollision(collider)
            
    def ToJSONstr(self):
        outString = json.dumps(obj=self,default=self.Encode,indent=4)
        return outString
    
    def Encode(self,obj):
        joinedDict = dict()
        for component in obj.__components.values():
            joinedDict[str(component.name)] = component.Encode(component)
        return joinedDict
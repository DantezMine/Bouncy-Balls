import json
from Components import ComponentTransform
from Components.Component import ComponentType

class GameObject(object):
    def __init__(self, parentScene, id = None):
        self.__id = parentScene.CreateID()
        self.__id = self.__id if id is None else id
        self.__components = {key: value for key, value in []} #initialize an empty dictionary using dictionary comprehension
        self.__parentScene = parentScene
        self.__isBackground = False
        self.startQueue = list()        
        self.AddComponent(ComponentTransform.Transform())
        
    def AddComponent(self, component):
        self.__components[component.name] = component
        self.__components[component.name].parent = self
        if self.__parentScene.hasStarted:
            component.Start()
        else:
            self.startQueue.append(component)
        if component.name == ComponentType.Background:
            self.__isBackground = True
        return True
    
    def RemoveComponent(self,componentName):
        if self.__components.__contains__(componentName):
            self.__components.pop(componentName)
            if componentName == ComponentType.Background:
                self.__isBackground = False
    
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
    
    def HandleStartQueue(self):
        for component in self.startQueue:
            component.Start()
        self.startQueue = list()
    
    def Start(self):
        self.HandleStartQueue()
        pass
        # keysCopy = list(self.__components.keys()).copy()
        # for key in keysCopy:
        #     self.__components[key].Start()
    
    def Update(self,deltaTime):
        self.HandleStartQueue()
        
        keysCopy = self.__components.keys()
        for key in keysCopy:
            if key != ComponentType.Sprite and key != ComponentType.Collider and key != ComponentType.Physics:
                self.__components[key].Update(deltaTime)
    
    def UpdateCollider(self,deltaTime, colliders):
        if self.HasComponent(ComponentType.Collider):
            self.__components[ComponentType.Collider].Update(deltaTime, colliders)
    
    def UpdatePhysics(self,deltaTime,allCollisions,mode):
        if self.__components.__contains__(ComponentType.Physics):
            self.__components[ComponentType.Physics].Update(deltaTime,allCollisions,mode)
            
    def Show(self,deltaTime):
        if self.__components.__contains__(ComponentType.Sprite):
            self.__components[ComponentType.Sprite].Update(deltaTime)
            
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
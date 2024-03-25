import ComponentTransform

class GameObject:
    def __init__(self, parentScene):
        self.__id = parentScene.CreateID()
        self.__components = {key: value for key, value in []} #initialize an empty dictionary using dictionary comprehension
        self.__parentScene = parentScene
        
        self.AddComponent(ComponentTransform.ComponentTransform())
        
    def AddComponent(self, component):
        if self.__components.__contains__(component.name):
            print("Component already exists in object %d"%self.__id)
            return False
        self.__components[component.name] = component
        self.__components[component.name].parent = self
        return True
    
    def RemoveComponent(self,component):
        if self.__components.__contains__(component.name):
            self.__components.pop(component.name)
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
        
    def GetID(self):
        return self.__id
    
    def GetParentScene(self):
        return self.__parentScene
    
    def Start(self):
        for key in self.__components.keys():
            self.__components[key].Start()
    
    def Update(self,deltaTime):
        for key in self.__components.keys():
            if key != "Sprite" and key != "Collider" and key != "Physics":
                self.__components[key].Update(deltaTime)
    
    def UpdateCollider(self,deltaTime, colliders):
        if self.__components.__contains__("Collider"):
            self.__components["Collider"].Update(deltaTime, colliders)
    
    def UpdatePhysics(self,deltaTime,allCollisions,mode):
        if self.__components.__contains__("Physics"):
            self.__components["Physics"].Update(deltaTime,allCollisions,mode)
            
    def Show(self,deltaTime):
        if self.__components.__contains__("Sprite"):
            self.__components["Sprite"].Update(deltaTime)
            
    def UpdateOnCollision(self,collider):
        for component in self.__components.values():
            component.OnCollision(collider)
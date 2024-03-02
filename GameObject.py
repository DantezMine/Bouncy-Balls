class GameObject:
    def __init__(self, parentScene):
        self.__id = parentScene.CreateID()
        self.__components = {key: value for key, value in []} #initialize an empty dictionary using dictionary comprehension
        
    def AddComponent(self, component):
        if self.__components.__contains__(component.name):
            print("Component already exists in object %d"%self.__id)
            return False
        self.__components[component.name] = component
        return True
    
    def RemoveComponent(self,component):
        if self.__components.__contains__(component.name):
            self.__components.pop(component.name)
            return True
        print("Component doesn't exist in object %d"%self.__id)
        return False
    
    def GetID(self):
        return self.__i_id
    
    def Update(self,deltaTime):
        pass
    
    def Show(self,deltaTime):
        if self.__components.__contains__("Sprite"):
            self.__components["Sprite"].Update()
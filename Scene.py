import GameObject

class Scene:
    ID = 0
    def __init__(self):
        self.__GameObjects = list()
        
    def AddGameObject(self,gameObject):
        self.__GameObjects.append(gameObject)
        return True
    
    def RemoveGameObject(self,gameObject):
        self.__GameObjects.remove(gameObject)
        
    def CreateID(self):
        Scene.ID += 1
        return Scene.ID
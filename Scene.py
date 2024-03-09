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
    
    def GetObjectsWithComponent(self,compName):
        outList = list()
        for gameObj in self.__GameObjects:
            comp = gameObj.GetComponentNoPrint(compName)
            if comp is not None:
                outList.append(comp.parent)
        return outList
    
    def GetComponents(self,compName):
        outList = list()
        for gameObj in self.__GameObjects:
            comp = gameObj.GetComponentNoPrint(compName)
            if comp is not None:
                outList.append(comp)
        return outList
    
    def UpdateScene(self,deltaTime):
        for go in self.__GameObjects:
            go.Update(deltaTime)
            go.Show(deltaTime)
        for go in self.__GameObjects:
            go.UpdateCollider(deltaTime, self.GetComponents("Collider"))
        for go in self.__GameObjects:
            go.UpdatePhysics(deltaTime)
    

    def StartScene(self):
        for go in self.__GameObjects:
            go.Start()
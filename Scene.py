class Scene:
    ID = 0
    def __init__(self):
        self.__gameObjects = list()
        
    def AddGameObject(self,gameObject):
        if self.__gameObjects.__contains__(gameObject):
            return False
        self.__gameObjects.append(gameObject)
        return True
    
    def RemoveGameObject(self,gameObject):
        if self.__gameObjects.__contains__(gameObject):
            self.__gameObjects.remove(gameObject)
            return True
        return False
        
    def CreateID(self):
        Scene.ID += 1
        return Scene.ID
    
    def GetObjectsWithComponent(self,compName):
        outList = list()
        for gameObj in self.__gameObjects:
            comp = gameObj.GetComponentNoPrint(compName)
            if comp is not None:
                outList.append(comp.parent)
        return outList
    
    def GetComponents(self,compName):
        outList = list()
        for gameObj in self.__gameObjects:
            comp = gameObj.GetComponentNoPrint(compName)
            if comp is not None:
                outList.append(comp)
        return outList
    
    def UpdateScene(self,deltaTime, updateFrequency):
        for go in self.__gameObjects:
            go.Update(deltaTime)
        for i in range(updateFrequency):
            dt = float(deltaTime)/updateFrequency
            collisions = []
            for go in self.__gameObjects:
                go.UpdatePhysics(dt,None,0)
            for go in self.__gameObjects:
                go.UpdateCollider(dt, self.GetComponents("Collider"))
                collisions += go.GetComponent("Collider").collisions
            for go in self.__gameObjects:
                go.UpdatePhysics(dt,collisions,1)
            for go in self.__gameObjects:
                go.UpdatePhysics(dt,None,2)
        for go in self.__gameObjects:
            go.Show(deltaTime)
    

    def StartScene(self):
        for go in self.__gameObjects:
            go.Start()
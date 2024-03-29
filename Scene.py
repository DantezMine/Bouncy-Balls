import json
from Component import Components

class Scene:
    ID = 0
    def __init__(self, name):
        self.__gameObjects = dict()
        self.name = name
        
    def AddGameObject(self,gameObject):
        if self.__gameObjects.__contains__(gameObject):
            return False
        self.__gameObjects[gameObject.GetID()] = gameObject
        return True
    
    def RemoveGameObject(self,gameObject):
        if self.__gameObjects.__contains__(gameObject):
            self.__gameObjects.pop(gameObject.GetID())
            return True
        return False
        
    def CreateID(self):
        Scene.ID += 1
        return Scene.ID
    
    def GameObjectWithID(self,id):
        return self.__gameObjects[id]
    
    def GetObjectsWithComponent(self,compName):
        outList = list()
        for gameObj in self.__gameObjects.values():
            comp = gameObj.GetComponentNoPrint(compName)
            if comp is not None:
                outList.append(comp.parent)
        return outList
    
    def GetComponents(self,compName):
        outList = list()
        for gameObj in self.__gameObjects.values():
            comp = gameObj.GetComponentNoPrint(compName)
            if comp is not None:
                outList.append(comp)
        return outList
    
    def UpdateScene(self,deltaTime, updateFrequency):
        for go in self.__gameObjects.values():
            go.Update(deltaTime)
        for i in range(updateFrequency):
            dt = float(deltaTime)/updateFrequency
            collisions = []
            for go in self.__gameObjects.values():
                go.UpdatePhysics(dt,None,0)
            for go in self.__gameObjects.values():
                go.UpdateCollider(dt, self.GetComponents(Components.Collider))
                collider = go.GetComponent(Components.Collider)
                if  collider is not None:
                    collisions += collider.collisions
            for go in self.__gameObjects.values():
                go.UpdatePhysics(dt,collisions,1)
            for go in self.__gameObjects.values():
                go.UpdatePhysics(dt,None,2)
        for go in self.__gameObjects.values():
            if go.IsBackground():
                go.Show(deltaTime)
        for go in self.__gameObjects.values():
            if not go.IsBackground():
                go.Show(deltaTime)
    

    def StartScene(self):
        for go in self.__gameObjects.values():
            go.Start()
        print(self.ToJSONstr())
            
    def ToJSONstr(self):
        outString = json.dumps(obj=self,default=self.Encode,indent=4)
        return outString
    
    def Encode(self,obj):
        joinedDict = dict()
        for gameObject in obj.__gameObjects.values():
            joinedDict[gameObject.GetID()] = gameObject.Encode(gameObject)
        return joinedDict
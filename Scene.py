import json
from Components.Component import ComponentType
import GameObject
from Components import ComponentBackground
from Components import ComponentBall
from Components import ComponentButton
from Components import ComponentCamera
from Components import ComponentCannon
from Components import ComponentCollider
from Components import ComponentGoalField
from Components import ComponentGround
from Components import ComponentPhysics
from Components import ComponentSlider
from Components import ComponentSprite
from Components import ComponentStructure
from Components import ComponentTransform
from Components import ComponentEditor

class Scene:
    def __init__(self, name = ""):
        self.ID = 0
        self.__gameObjects = dict()
        self.name = name
        self.world = None
        self.removeQueue = list()
        self.addQueue = list()
        self.hasStarted = False
        
    def AddGameObject(self,gameObject):
        self.addQueue.append(gameObject)
    
    def RemoveGameObject(self,gameObject):
        self.removeQueue.append(gameObject)
        
    def RemoveGameObjectID(self, id):
        if self.__gameObjects.__contains__(int(id)):
            self.removeQueue.append(self.__gameObjects[int(id)])
        
    def CreateID(self):
        self.ID += 1
        return self.ID
    
    def GameObjectWithID(self,id):
        if self.__gameObjects.__contains__(int(id)):
            return self.__gameObjects[int(id)]
        return None
    
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
        self.HandleAddQueue()
        self.HandleRemoveQueue()

        self.UpdateComponents(deltaTime)
        self.UpdatePhysicsScene(deltaTime, updateFrequency)
        self.ShowScene(deltaTime)
        
    def UpdateComponents(self, deltaTime):
        for go in self.__gameObjects.values():
            go.Update(deltaTime)
            
    def UpdatePhysicsScene(self, deltaTime, updateFrequency):
        for i in range(updateFrequency):
            dt = float(deltaTime)/updateFrequency
            collisions = []
            for go in self.__gameObjects.values():
                go.UpdatePhysics(dt,None,0)
            for go in self.__gameObjects.values():
                collider = go.GetComponent(ComponentType.Collider)
                if  collider is not None:
                    go.UpdateCollider(dt, self.GetComponents(ComponentType.Collider))
                    collisions += collider.collisions
            for go in self.__gameObjects.values():
                go.UpdatePhysics(dt,collisions,1)
            for go in self.__gameObjects.values():
                go.UpdatePhysics(dt,None,2)
                
    def ShowScene(self,deltaTime):
        for go in self.__gameObjects.values():
            go.Show(deltaTime)

    def HandleAddQueue(self):
        for gameObject in self.addQueue:
            if self.__gameObjects.__contains__(gameObject):
                continue
            if gameObject.HasComponent(ComponentType.Camera):
                self.camera = gameObject.GetComponent(ComponentType.Camera)
            self.__gameObjects[gameObject.GetID()] = gameObject
        self.addQueue = list()
            
    def HandleRemoveQueue(self):
        for go in self.removeQueue:
            if self.__gameObjects.__contains__(go.GetID()):
                self.__gameObjects.pop(go.GetID())
        self.removeQueue = list()

    def StartScene(self):
        self.HandleAddQueue()
        self.HandleRemoveQueue()
        self.hasStarted = True
        for go in self.__gameObjects.values():
            go.Start()
            
    def ToJSONstr(self):
        outString = json.dumps(obj=self,default=self.Encode,indent=4)
        return outString
    
    def WriteJSON(self, fp):
        out = json.dump(obj=self, fp=fp, default=self.Encode,indent=4)
        return out
    
    def FromJSON(self, scenePath):
        with open("Bouncy-Balls/"+scenePath, 'r') as fp:
            self.Decode(json.load(fp=fp))
    
    def Encode(self,obj):
        joinedDict = dict()
        for gameObject in obj.__gameObjects.values():
            joinedDict[gameObject.GetID()] = gameObject.Encode(gameObject)
        return {
            "name" : self.name,
            "__gameObjects" : joinedDict
        }
    
    def Decode(self,obj):
        self.IDQueue = dict()
        self.IDmap = dict()
        self.name = obj["name"]
        gameObjects = obj["__gameObjects"]
        for gameObjectID in gameObjects.keys():
            gameObjectID = int(gameObjectID)
            gameObject = GameObject.GameObject(self, gameObjectID)
            for componentObj in gameObjects[str(gameObjectID)].values():
                componentConstr = self.GetComponent(componentObj)
                if componentConstr is None:
                    pass
                component = componentConstr()
                component.Decode(componentObj)
                gameObject.AddComponent(component)
            self.AddGameObject(gameObject)
            self.IDmap[gameObjectID] = str(gameObject.GetID())
        return self
    
    def GetComponent(self, component):
        ctype = component["name"]
        
        if ctype == ComponentType.Transform.value:
            return ComponentTransform.Transform
        if ctype == ComponentType.Background.value:
            backgroundType = component["backgroundType"]
            if backgroundType  == ComponentBackground.BackgroundType.Background.value:
                return ComponentBackground.Background
            if backgroundType == ComponentBackground.BackgroundType.Nature.value:
                return ComponentBackground.BackgroundNature
            if backgroundType == ComponentBackground.BackgroundType.Skyline.value:
                return ComponentBackground.BackgroundSkyline
        if ctype == ComponentType.Ball.value:
            ballType = component["ballType"]
            if ballType == ComponentBall.BallType.Heavy.value:
                return ComponentBall.BallBowling
            if ballType == ComponentBall.BallType.Bouncy.value:
                return ComponentBall.BallBouncy
        if ctype == ComponentType.Button.value:
            buttonType = component["buttonType"]
            if buttonType == ComponentButton.ButtonType.Button.value:
                return ComponentButton.Button
            if buttonType == ComponentButton.ButtonType.Scene.value:
                return ComponentButton.ButtonScene
            if buttonType == ComponentButton.ButtonType.Selectable.value:
                return ComponentButton.ButtonSelectable
        if ctype == ComponentType.Camera.value:
            return ComponentCamera.Camera
        if ctype == ComponentType.Cannon.value:
            return ComponentCannon.Cannon
        if ctype == ComponentType.Base.value:
            return ComponentCannon.Base
        if ctype == ComponentType.Collider.value:
            colliderType = component["colliderType"]
            if colliderType == ComponentCollider.ColliderType.Circle.value:
                return ComponentCollider.ColliderCircle
            if colliderType == ComponentCollider.ColliderType.Rect.value:
                return ComponentCollider.ColliderRect
        if ctype == ComponentType.GoalField.value:
            return ComponentGoalField.GoalField
        if ctype == ComponentType.Ground.value:
            groundType = component["groundType"]
            if groundType == ComponentGround.GroundType.Dirt.value:
                return ComponentGround.GroundDirt
        if ctype == ComponentType.Physics.value:
            return ComponentPhysics.Physics
        if ctype == ComponentType.Slider.value:
            return ComponentSlider.Slider
        if ctype == ComponentType.Sprite.value:
            spriteType = component["spriteType"]
            if spriteType == ComponentSprite.SpriteType.Sprite.value:
                return ComponentSprite.Sprite
            elif spriteType == ComponentSprite.SpriteType.Background.value:
                return ComponentSprite.SpriteBackground
            elif spriteType == ComponentSprite.SpriteType.UI.value:
                return ComponentSprite.SpriteUI
        if ctype == ComponentType.Structure.value:
            structureType = component["structureType"]
            if structureType == ComponentStructure.StructureType.Metal.value:
                return ComponentStructure.StructureMetal
            elif structureType == ComponentStructure.StructureType.Wood.value:
                return ComponentStructure.StructureWood
        if ctype == ComponentType.Editor.value:
            return ComponentEditor.Editor
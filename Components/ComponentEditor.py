from Vector import Vec2
from lib import GlobalVars
from Components.Component import ComponentType
from Components import ComponentTransform
from Components import ComponentStructure
from Components import ComponentButton
from Components import ComponentCamera
from Components import Component
import GameObject
import Scene

class Editor(Component.Component):
    def __init__(self):
        self.name = ComponentType.Editor
        self.parent = None
        
    def Start(self):
        self.CreateSelectables()
        self.workingScene = Scene.Scene("untitled scene")
        camera = GameObject.GameObject(self.workingScene)
        camera.AddComponent(ComponentCamera.Camera(position=Vec2(0,0),scale=1/1.0))
        self.workingScene.AddGameObject(camera)
        self.workingObject = None
        
    def Update(self, deltaTime):
        camera = self.parent.GetParentScene().camera
        if self.workingObject is not None:
            objTransform = self.workingObject.GetComponent(ComponentType.Transform)
            objTransform.position = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen, camera)
        self.workingScene.UpdateScene(deltaTime=deltaTime,updateFrequency=10)
        
    def CreateSelectables(self):
        parentScene = self.parent.GetParentScene()
        buttonWood = GameObject.GameObject(parentScene)
        buttonWood.AddComponent(ComponentButton.ButtonSelectable(nPoly=4, lenX=0.2, lenY=0.2, position=Vec2(-0.8,0.8),spritePath="data/WoodStructure.png",editor=self,componentInit=ComponentStructure.StructureWood))
        parentScene.AddGameObject(buttonWood)
    
    def SelectType(self, componentInit):
        self.workingObject = GameObject.GameObject(self.workingScene)
        self.workingObject.AddComponent(componentInit())
        self.workingScene.AddGameObject(self.workingObject)
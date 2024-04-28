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
import enum
import math

class EditorState(enum.Enum):
    Free = enum.auto()
    Placing = enum.auto()
    EditingObject = enum.auto()

class Editor(Component.Component):
    def __init__(self):
        self.name = ComponentType.Editor
        self.parent = None
        
        self.state = EditorState.Free
        self.minZoom = 1.0/15
        self.maxZoom = 1.0
        self.startDrag = None
        
    def Start(self):
        self.CreateSelectables()
        self.workingScene = Scene.Scene("untitled scene")
        camera = GameObject.GameObject(self.workingScene)
        camera.AddComponent(ComponentCamera.Camera(position=Vec2(0,0),scale=1/1.0))
        self.workingScene.AddGameObject(camera)
        self.workingObject = None
        
    def Update(self, deltaTime):
        camera = None
        try:
            camera = self.workingScene.camera
        except:
            pass
        if self.workingObject is not None and camera is not None:
            objTransform = self.workingObject.GetComponent(ComponentType.Transform)
            objTransform.position = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen, camera)
        self.workingScene.HandleAddQueue()
        self.workingScene.HandleRemoveQueue()
        self.workingScene.ShowScene(deltaTime)
        self.CheckMouse()
        
    def CreateSelectables(self):
        parentScene = self.parent.GetParentScene()
        size = 0.3
        
        buttonWood = GameObject.GameObject(parentScene)
        buttonWood.AddComponent(ComponentButton.ButtonSelectable(nPoly=4, lenX=size, lenY=size, position=Vec2(-0.8,0.8),spritePath="data/WoodStructure.png",editor=self,componentInit=ComponentStructure.StructureWood))
        parentScene.AddGameObject(buttonWood)
        
        buttonMetal = GameObject.GameObject(parentScene)
        buttonMetal.AddComponent(ComponentButton.ButtonSelectable(nPoly=4, lenX=size, lenY=size, position=Vec2(-0.45,0.8),spritePath="data/StructureMetal.png",editor=self,componentInit=ComponentStructure.StructureMetal))
        parentScene.AddGameObject(buttonMetal)
    
    def SelectType(self, componentInit):
        self.workingObject = GameObject.GameObject(self.workingScene)
        self.workingObject.AddComponent(componentInit())
        self.workingScene.AddGameObject(self.workingObject)
        self.state = EditorState.Placing
        
    def PlaceObject(self):
        self.workingObject = None
        self.state = EditorState.Free
        
    def CheckMouse(self):
        if GlobalVars.mouseLeft:
            self.OnLeftClick()
        if GlobalVars.mouseMid:
            if self.startDrag is None:
                self.startDrag = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen, self.workingScene.camera)
                self.camStartPos = self.workingScene.camera.parent.GetComponent(ComponentType.Transform).position
            self.MoveCamera()
        else:
            self.startDrag = None
        if GlobalVars.scrollEvent is not None:
            self.ScrollCamera()
            
    def OnLeftClick(self):
        if self.state == EditorState.Free:
            pass
        if self.state == EditorState.Placing:
            self.PlaceObject()
            
    def MoveCamera(self): #function jiggles aroung the more zoomed out it is, probably because camera moves but is also used for screen to world transform
        drag = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen, self.workingScene.camera) - self.startDrag
        self.workingScene.camera.parent.GetComponent(ComponentType.Transform).position = self.camStartPos - drag #change to camera's internal move function
    
    def ScrollCamera(self):
        scroll = GlobalVars.scrollEvent.y
        camera = self.workingScene.camera
        camera.scale += scroll * (math.log(1.0/camera.scale)/30 + 0.1) / 5
        camera.scale = self.maxZoom if camera.scale > self.maxZoom else camera.scale
        camera.scale = self.minZoom if camera.scale < self.minZoom else camera.scale
from Vector import Vec2
import GlobalVars
from Components.Component import ComponentType
from Components import ComponentTransform
from Components import ComponentStructure
from Components import ComponentButton
from Components import ComponentCamera
from Components import ComponentGround
from Components import ComponentSprite
from Components import Component
import GameObject
import Scene
import enum
import math

class EditorState(enum.Enum):
    Free = enum.auto()
    Selected = enum.auto()
    Move = enum.auto()
    ScaleX = enum.auto()
    ScaleY = enum.auto()
    Rotate = enum.auto()
    EditingObject = enum.auto()

class Editor(Component.Component):
    def __init__(self):
        self.name = ComponentType.Editor
        self.parent = None
        
        self.state = EditorState.Free
        self.minZoom = 1.0/15
        self.maxZoom = 1.0
        self.startDrag = None
        self.objectIDs = list()
                
    def Start(self):
        self.CreateSelectables()
        self.workingScene = Scene.Scene("untitled scene")
        camera = GameObject.GameObject(self.workingScene)
        camera.AddComponent(ComponentCamera.Camera(position=Vec2(0,0),scale=1/1.0))
        self.workingScene.AddGameObject(camera)
        self.workingObject = None
        gizmoObject = GameObject.GameObject(self.workingScene)
        gizmoObject.AddComponent(ComponentSprite.SpriteGizmo(lenX=0.3,lenY=0.3,targetID=None))
        self.workingScene.AddGameObject(gizmoObject)
        self.gizmoObjectID = gizmoObject.GetID()
        
    def Update(self, deltaTime):
        camera = None
        try:
            camera = self.workingScene.camera
        except:
            pass
        if self.state == EditorState.Selected:
            objTransform = self.workingObject.GetComponent(ComponentType.Transform)
            # objTransform.position = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen, camera)
        
        self.workingScene.HandleAddQueue()
        self.workingScene.HandleRemoveQueue()
        self.workingScene.ShowScene(deltaTime)
        self.CheckMouse()
        
        
    def CreateSelectables(self):
        parentScene = self.parent.GetParentScene()
        size = 0.2
        
        selectables = (
            ("data/WoodStructure.png", ComponentStructure.StructureWood),
            ("data/StructureMetal.png", ComponentStructure.StructureMetal),
            ("data/GroundDirt.png", ComponentGround.GroundDirt)
        )
        
        for i in range(len(selectables)):
            button = GameObject.GameObject(parentScene)
            button.AddComponent(ComponentButton.ButtonSelectable(nPoly=4, lenX=size, lenY=size, position=Vec2(-1 + size * (2.0/3 + i * 7.0/6), 1 - size * 2.0/3), spritePath=selectables[i][0], editor=self, componentInit=selectables[i][1]))
            parentScene.AddGameObject(button)
    
    def SelectType(self, componentInit):
        self.workingObject = GameObject.GameObject(self.workingScene)
        self.workingObject.AddComponent(componentInit())
        self.workingObject.GetComponent(ComponentType.Transform).position = ComponentTransform.Transform.ScreenToWorldPos(Vec2(GlobalVars.foreground.get_width()/2.0,GlobalVars.foreground.get_height()/2.0),self.workingScene.camera)
        self.workingScene.AddGameObject(self.workingObject)
        self.objectIDs.append(self.workingObject.GetID())
        self.state = EditorState.Selected
        
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
        if GlobalVars.mouseChanged:
            if self.state == EditorState.Free:
                self.SelectObject()
            elif self.state == EditorState.Selected:
                if self.SelectGizmo():
                    return
                self.PlaceObject()
            
    def MoveCamera(self): #function jiggles aroung the more zoomed out it is, probably because camera moves but is also used for screen to world transform
        drag = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen, self.workingScene.camera) - self.startDrag
        self.workingScene.camera.MoveCamera(self.camStartPos - drag) #change to camera's internal move function
    
    def ScrollCamera(self):
        scroll = GlobalVars.scrollEvent.y
        camera = self.workingScene.camera
        self.minZoom = 2.0/(camera.boundLen.y)
        scale = camera.scale + scroll * (math.log(1.0/camera.scale)/30 + 0.1) / 5
        scale = min(self.maxZoom, max(self.minZoom, scale))
        camera.ScaleCamera(scale)
        
    def SelectObject(self):
        mousePosWorld = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen,self.workingScene.camera)
        intersection = False
        ID = None
        for id in self.objectIDs:
            obj = self.workingScene.GameObjectWithID(id)
            if obj.HasComponent(ComponentType.Structure):
                if self.CheckIntersection(mousePosWorld, obj.GetComponent(ComponentType.Structure)):
                    intersection = True
                    ID = id
                    break
            if obj.HasComponent(ComponentType.Ground):
                if self.CheckIntersection(mousePosWorld, obj.GetComponent(ComponentType.Ground)):
                    intersection = True
                    ID = id
                    break
        
        if intersection:
            self.workingObject = self.workingScene.GameObjectWithID(ID)
            gizmoSprite = self.workingScene.GameObjectWithID(self.gizmoObjectID).GetComponent(ComponentType.Sprite)
            gizmoSprite.targetID = self.gizmoObjectID
            gizmoSprite.gizmoVal = 0
            self.state = EditorState.Selected
            
    def SelectGizmo(self):
        pass
        gizmoSprite = self.workingScene.GameObjectWithID(self.gizmoObjectID).GetComponent(ComponentType.Sprite)
        gizmoSprite.gizmoVal = 0
    
    def CheckIntersection(self, point, comp):
        verts = list()
        deltaPhi = math.pi/2
        for i in range(4):
            verts.append(comp.parent.GetComponent(ComponentType.Transform).position + Vec2(math.cos(deltaPhi*i+deltaPhi/2.0)*comp.lenX/2.0, math.sin(deltaPhi*i+deltaPhi/2.0)*comp.lenY/2.0))
        return self.PointInPolygon(point, verts)
            
    def PointInPolygon(self,point,verts):
        inside = True
        for i in range(4):
            A = verts[i]
            B = verts[(i+1)%4]
            normal = (B-A).Perp()
            AP = point-A
            if normal.Dot(AP) < 0:
                inside = False
        return inside
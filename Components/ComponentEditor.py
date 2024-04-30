import pygame
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
        self.gizmoSize = 0.3
        self.mouseStart = None
                
    def Start(self):
        self.CreateSelectables()
        self.workingScene = Scene.Scene("untitled scene")
        camera = GameObject.GameObject(self.workingScene)
        camera.AddComponent(ComponentCamera.Camera(position=Vec2(0,0),scale=1/1.0))
        self.workingScene.AddGameObject(camera)
        self.workingObject = None
        gizmoObject = GameObject.GameObject(self.workingScene)
        gizmoObject.AddComponent(ComponentSprite.SpriteGizmo(diameter=self.gizmoSize*math.sqrt(2),targetID=None))
        self.workingScene.AddGameObject(gizmoObject)
        self.gizmoObjectID = gizmoObject.GetID()
        
    def Update(self, deltaTime):
        self.HandleGizmo()
        
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
        gizmoSprite = self.workingScene.GameObjectWithID(self.gizmoObjectID).GetComponent(ComponentType.Sprite)
        self.gizmoObjectID = self.workingObject.GetID()
        gizmoSprite.targetID = self.gizmoObjectID
        gizmoSprite.gizmoVal = 0
        self.state = EditorState.Selected
        
    def PlaceObject(self):
        self.workingObject = None
        self.state = EditorState.Free
        
    def CheckMouse(self):
        if GlobalVars.mouseLeft:
            self.OnLeftClick()
        else:
            self.workingScene.GameObjectWithID(self.gizmoObjectID).GetComponent(ComponentType.Sprite).gizmoVal = 0
            if self.state == EditorState.Move or self.state == EditorState.Rotate or self.state == EditorState.ScaleX or self.state == EditorState.ScaleY:
                self.state = EditorState.Selected
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
            self.gizmoObjectID = self.workingObject.GetID()
            gizmoSprite.targetID = self.gizmoObjectID
            gizmoSprite.gizmoVal = 0
            self.state = EditorState.Selected
            
    def SelectGizmo(self):
        gizmoSprite = self.workingScene.GameObjectWithID(self.gizmoObjectID).GetComponent(ComponentType.Sprite)
        targetTransform = self.workingObject.GetComponent(ComponentType.Transform)
        sceneCam = self.workingScene.camera
        
        #World Space
        topLeft = (Vec2(gizmoSprite.lenX,-gizmoSprite.lenY)/(sceneCam.scale*2.0)).Rotate(targetTransform.rotation)
        botLeft = (Vec2(gizmoSprite.lenX, gizmoSprite.lenY)/(sceneCam.scale*2.0)).Rotate(targetTransform.rotation)
        #get extremes of AABB
        dx = max(abs(topLeft.x),abs(botLeft.x))
        dy = max(abs(topLeft.y),abs(botLeft.y))
        
        s = dx/4.0
        vertsSquare = [] * 4
        deltaPhi = math.pi/2
        for i in range(4):
            vertsSquare.append(targetTransform.position + Vec2(math.cos(deltaPhi*i+deltaPhi/2.0)*s, math.sin(deltaPhi*i+deltaPhi/2.0)*s))
        
        sX = s * 4/5.0
        sY = s * 2
        vertsArrowY = [] * 4
        deltaPhi = math.pi/2
        for i in range(4):
            vertsArrowY.append(targetTransform.position + Vec2(0,23/10.0)*s + Vec2(math.cos(deltaPhi*i+deltaPhi/2.0)*sX, math.sin(deltaPhi*i+deltaPhi/2.0)*sY))

        vertsArrowX = [] * 4
        deltaPhi = math.pi/2
        for i in range(4):
            vertsArrowX.append(targetTransform.position + Vec2(23/10.0,0)*s + Vec2(math.cos(deltaPhi*i+deltaPhi/2.0)*sY, math.sin(deltaPhi*i+deltaPhi/2.0)*sX))
            
        dO = dx
        dI = dx*0.9
        
        mousePosWorld = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen,self.workingScene.camera)
        self.mouseStart = mousePosWorld
        if self.PointInPolygon(mousePosWorld,vertsSquare):
            gizmoSprite.gizmoVal = 1
            self.state = EditorState.Move
            return True
        if (mousePosWorld-targetTransform.position).SqMag() < dO**2 and (mousePosWorld-targetTransform.position).SqMag() > dI**2:
            gizmoSprite.gizmoVal = 2
            self.state = EditorState.Rotate
            return True
        if self.PointInPolygon(mousePosWorld,vertsArrowX):
            gizmoSprite.gizmoVal = 3
            self.state = EditorState.ScaleX
            return True
        if self.PointInPolygon(mousePosWorld,vertsArrowY):
            gizmoSprite.gizmoVal = 4
            self.state = EditorState.ScaleY
            return True
        self.mouseStart = None
        return False
    
    def HandleGizmo(self):
        if self.state == EditorState.Move:
            camera = self.workingScene.camera
            objTransform = self.workingObject.GetComponent(ComponentType.Transform)
            objTransform.position = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen, camera)
    
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
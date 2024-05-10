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
from Components import ComponentBackground
from Components import ComponentCannon
from Components import ComponentBall
from Components import ComponentManager
from Components import ComponentGoalField
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
    Saving = enum.auto()

class Editor(Component.Component):
    def __init__(self):
        self.name = ComponentType.Editor
        self.parent = None
        
        self.state = EditorState.Free
        self.startDrag = None
        self.objectIDs = list()
        self.gizmoSize = 0.3
        self.mouseStart = None
        
        self.ballData = {
            ComponentBall.BallType.Bouncy : 0,
            ComponentBall.BallType.Heavy : 0
        }
        
        self.ballNumbers = {}
                
    def Start(self):
        self.CreateSelectables()
        self.CreateBallSelections()
        self.workingScene = Scene.Scene("untitled scene")
        camera = GameObject.GameObject(self.workingScene)
        camera.AddComponent(ComponentCamera.Camera(position=Vec2(0,0),scale=1/1.0,boundLen=Vec2(30,20)))
        self.workingScene.AddGameObject(camera)
        
        background = GameObject.GameObject(self.workingScene)
        background.AddComponent(ComponentBackground.BackgroundNature(position=Vec2(0,0),lenX=2,lenY=2))
        self.workingScene.AddGameObject(background)
        self.objectIDs.append(background.GetID())
        
        manager = GameObject.GameObject(self.workingScene)
        manager.AddComponent(ComponentManager.Manager(inEditor=True))
        self.workingScene.AddGameObject(manager)
        
        self.workingObject = None
        self.workingComp = None
        
        gizmoObject = GameObject.GameObject(self.workingScene)
        gizmoObject.AddComponent(ComponentSprite.SpriteGizmo(diameter=self.gizmoSize*math.sqrt(2),targetID=None))
        self.workingScene.AddGameObject(gizmoObject)
        self.gizmoObjectID = gizmoObject.GetID()
        
        saveButton = GameObject.GameObject(self.parent.GetParentScene())
        saveButton.AddComponent(ComponentButton.Button(nPoly=4,lenX=0.2,lenY=0.2,position=Vec2(-0.87,-0.87),function=self.SaveScene, spritePath="data/Save.png"))
        self.parent.GetParentScene().AddGameObject(saveButton)
        
        cannon = GameObject.GameObject(self.workingScene)
        cannon.AddComponent(ComponentCannon.Cannon())
        self.workingScene.AddGameObject(cannon)
        self.objectIDs.append(cannon.GetID())
        
        goalField = GameObject.GameObject(self.workingScene)
        goalField.AddComponent(ComponentGoalField.GoalField())
        # goalField.GetComponent(ComponentType.Transform).position = Vec2(0.5,0.5)
        self.workingScene.AddGameObject(goalField)
        self.objectIDs.append(goalField.GetID())
        
        self.workingScene.StartScene()
        
    def Update(self, deltaTime):
        if self.state == EditorState.Saving and self.workingScene.GameObjectWithID(self.gizmoObjectID) is None:
            import SceneSetup
            sceneName = self.workingScene.name
            cannons = self.workingScene.GetObjectsWithComponent(ComponentType.Cannon)
            
            levelSelectButton = GameObject.GameObject(self.workingScene)
            levelSelectButton.AddComponent(ComponentButton.ButtonScene(lenX=0.2,lenY=0.2,setupFunc=SceneSetup.SetupLevelSelect, sceneName="levelSelect", spritePath="data/Return.png", position=Vec2(0.9,0.9)))
            self.workingScene.AddGameObject(levelSelectButton)
            
            self.workingScene.camera.free = False
            if len(cannons) > 0:
                cannons[0].ballData = self.ballData
            with open("Bouncy-Balls/Levels/scene%s.json"%sceneName,"w") as fp:
                self.workingScene.WriteJSON(fp)
            self.workingScene.camera.free = True
                
            gizmoObject = GameObject.GameObject(self.workingScene)
            gizmoObject.AddComponent(ComponentSprite.SpriteGizmo(diameter=self.gizmoSize*math.sqrt(2),targetID=None))
            self.workingScene.AddGameObject(gizmoObject)
            self.gizmoObjectID = gizmoObject.GetID()
            
            self.state = EditorState.Free
            
            
        self.HandleGizmo()
        
        self.workingScene.HandleAddQueue()
        self.workingScene.HandleRemoveQueue()
        self.workingScene.ShowScene(deltaTime)
        self.CheckMouse()
        self.workingScene.StartScene()
        
        baseList = self.workingScene.GetComponents(ComponentType.Base)
        if len(baseList) > 0:
            baseList[0].UpdatePosition()
        
    def CreateSelectables(self):
        parentScene = self.parent.GetParentScene()
        self.size = 0.2
        
        selectables = (
            ("data/WoodStructure.png", ComponentStructure.StructureWood),
            ("data/StructureMetal.png", ComponentStructure.StructureMetal),
            ("data/StructureGoal.png", ComponentStructure.StructureGoal),
            ("data/GroundDirt.png", ComponentGround.GroundDirt),
            ("data/BackgroundSkyline-Sky.png", ComponentBackground.BackgroundSkyline),
            ("data/BackgroundNature-Sky.png", ComponentBackground.BackgroundNature)
        )
        
        for i in range(len(selectables)):
            button = GameObject.GameObject(parentScene)
            button.AddComponent(ComponentButton.ButtonSelectable(nPoly=4, lenX=self.size, lenY=self.size, position=Vec2(-1 + self.size * (2.0/3 + i * 7.0/6), 1 - self.size * 2.0/3), spritePath=selectables[i][0], editor=self, componentInit=selectables[i][1]))
            parentScene.AddGameObject(button)
    
    def CreateBallSelections(self):
        parentScene = self.parent.GetParentScene()
        size = 0.15
        balls = (
            ("data/BowlingBall.PNG",ComponentBall.BallType.Heavy),
            ("data/TennisBall.png", ComponentBall.BallType.Bouncy)
        )
        
        for i in range(len(balls)):
            display = GameObject.GameObject(parentScene)
            display.AddComponent(ComponentSprite.SpriteUI(spritePath=balls[i][0],lenX=size,lenY=size))
            display.GetComponent(ComponentType.Transform).position = Vec2(-1 + size * 2.0/3, 0.7 - size * (2.0/3 + i * 8/6))
            parentScene.AddGameObject(display)
            
            arrowUp = GameObject.GameObject(parentScene)
            arrowUp.AddComponent(ComponentButton.ButtonBallArrow(lenX=size/3,lenY=size/2,position=Vec2(-0.7 + size * 2.0/3, 0.7 - size * (2.0/3 - 0.3 + i * 8/6)),function=self.ButtonArrow,ballType=balls[i][1],weight=1))
            parentScene.AddGameObject(arrowUp)
            arrowDown = GameObject.GameObject(parentScene)
            arrowDown.AddComponent(ComponentButton.ButtonBallArrow(lenX=size/3,lenY=size/2,position=Vec2(-0.7 + size * 2.0/3, 0.7 - size * (2.0/3 + 0.3 + i * 8/6)),function=self.ButtonArrow,ballType=balls[i][1],weight=-1))
            parentScene.AddGameObject(arrowDown)
            
            number = GameObject.GameObject(parentScene)
            number.AddComponent(ComponentSprite.SpriteUI(spritePath="data/WoodStructure.png",lenX=size,lenY=size,number=0))
            number.GetComponent(ComponentType.Transform).position = Vec2(-0.83 + size * 2.0/3, 0.7 - size * (2.0/3 + i * 8/6))
            parentScene.AddGameObject(number)
            
            self.ballNumbers[balls[i][1]] = number.GetComponent(ComponentType.Sprite)
                        
    def ButtonArrow(self, ballType, weight):
        self.ballData[ballType] += weight if self.ballData[ballType] + weight >= -1 and self.ballData[ballType] + weight <= 9 else 0
        self.ballNumbers[ballType].number += weight if self.ballData[ballType] + weight >= -1 and self.ballData[ballType] + weight <= 9 else 0
    
    def SelectType(self, componentInit):
        self.workingObject = GameObject.GameObject(self.workingScene)
        self.workingObject.AddComponent(componentInit())
        self.workingObject.GetComponent(ComponentType.Transform).position = ComponentTransform.Transform.ScreenToWorldPos(Vec2(GlobalVars.foreground.get_width()/2.0,GlobalVars.foreground.get_height()/2.0),self.workingScene.camera)
        self.workingScene.AddGameObject(self.workingObject)
        
        if self.workingObject.HasComponent(ComponentType.Background):
            backgroundList = self.workingScene.GetObjectsWithComponent(ComponentType.Background)
            if len(backgroundList) > 0:
                self.workingScene.RemoveGameObject(backgroundList[0])
                self.objectIDs.remove(backgroundList[0].GetID())
        
        self.CreateDeleteButton()
        self.workingComp = self.GetWorkingComponent()
        self.objectIDs.append(self.workingObject.GetID())
        gizmoSprite = self.workingScene.GameObjectWithID(self.gizmoObjectID).GetComponent(ComponentType.Sprite)
        gizmoSprite.targetID = self.workingObject.GetID()
        gizmoSprite.gizmoVal = 0
        self.state = EditorState.Selected
        
    def CreateDeleteButton(self):
        deleteButton = GameObject.GameObject(self.parent.GetParentScene())
        deleteButton.AddComponent(ComponentButton.Button(nPoly=4,lenX=0.2,lenY=0.2,position=Vec2(0,-0.77),function=self.DeleteObject, spritePath="data/Delete.png"))
        self.parent.GetParentScene().AddGameObject(deleteButton)
        self.deleteButtonID = deleteButton.GetID()
        
    def PlaceObject(self):
        self.workingScene.GameObjectWithID(self.gizmoObjectID).GetComponent(ComponentType.Sprite).targetID = None
        self.parent.GetParentScene().RemoveGameObjectID(self.deleteButtonID)
        self.deleteButtonID = None
        self.prevObjID = self.workingObject.GetID()
        self.workingObject = None
        self.workingComp = None
        self.state = EditorState.Free
        
    def CheckMouse(self):
        if self.state == EditorState.Saving:
            return
        if GlobalVars.mouseLeft:
            self.OnLeftClick()
        else:
            if self.state == EditorState.Move or self.state == EditorState.Rotate or self.state == EditorState.ScaleX or self.state == EditorState.ScaleY:
                self.state = EditorState.Selected
        #     self.workingScene.GameObjectWithID(self.gizmoObjectID).GetComponent(ComponentType.Sprite).gizmoVal = 0
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
            if self.workingObject is not None:
                if self.SelectGizmo():
                    return
                self.PlaceObject()
            if self.SelectObject():
                self.CreateDeleteButton()
                return
            
    def MoveCamera(self): #function jiggles aroung the more zoomed out it is, probably because camera moves but is also used for screen to world transform
        drag = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen, self.workingScene.camera) - self.startDrag
        self.workingScene.camera.MoveCamera(self.camStartPos - drag)
    
    def ScrollCamera(self):
        scroll = GlobalVars.scrollEvent.y
        camera = self.workingScene.camera
        scale = camera.scale + scroll * (math.log(1.0/camera.scale)/30 + 0.1) / 5
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
            if obj.HasComponent(ComponentType.Cannon):
                if self.CheckIntersection(mousePosWorld, obj.GetComponent(ComponentType.Cannon)):
                    intersection = True
                    ID = id
                    break
            if obj.HasComponent(ComponentType.GoalField):
                if self.CheckIntersection(mousePosWorld, obj.GetComponent(ComponentType.GoalField)):
                    intersection = True
                    ID = id
                    break
        
        if intersection:
            self.workingObject = self.workingScene.GameObjectWithID(ID)
            self.workingComp = self.GetWorkingComponent()
            gizmoSprite = self.workingScene.GameObjectWithID(self.gizmoObjectID).GetComponent(ComponentType.Sprite)
            gizmoSprite.targetID = self.workingObject.GetID()
            gizmoSprite.gizmoVal = 0
            self.state = EditorState.Selected
            return True
        return False
    
    def DeleteObject(self):
        if self.state == EditorState.Free:
            if self.workingScene.GameObjectWithID(self.prevObjID).HasComponent(ComponentType.Cannon):
                self.workingScene.RemoveGameObject(self.workingScene.GetObjectsWithComponent(ComponentType.Base)[0])
            self.workingScene.RemoveGameObjectID(self.prevObjID)
            self.objectIDs.remove(self.prevObjID)
                
        
    def SaveScene(self):
        self.workingScene.RemoveGameObjectID(self.gizmoObjectID)
        
        self.state = EditorState.Saving
                    
    def SelectGizmo(self):
        gizmoSprite = self.workingScene.GameObjectWithID(self.gizmoObjectID).GetComponent(ComponentType.Sprite)
        targetTransform = self.workingObject.GetComponent(ComponentType.Transform)
        sceneCam = self.workingScene.camera
        
        #World Space
        topLeft = (Vec2(gizmoSprite.lenX,-gizmoSprite.lenY)/(sceneCam.scale*2.0))
        botLeft = (Vec2(gizmoSprite.lenX, gizmoSprite.lenY)/(sceneCam.scale*2.0))
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
        
        #distanceOuter and distanceInner for outside circle intersection
        dO = dx
        dI = dx*0.9
        
        mousePosWorld = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen,self.workingScene.camera)
        self.mouseStart = mousePosWorld
        self.rotStart = None
        if self.PointInPolygon(mousePosWorld,vertsSquare):
            gizmoSprite.gizmoVal = 1
            self.state = EditorState.Move
            return True
        if (mousePosWorld-targetTransform.position).SqMag() < dO**2 and (mousePosWorld-targetTransform.position).SqMag() > dI**2:
            gizmoSprite.gizmoVal = 2
            self.state = EditorState.Rotate
            self.rotStart = targetTransform.rotation
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
        try:
            camera = self.workingScene.camera
            mousePosWorld = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen, camera)
            objTransform = self.workingObject.GetComponent(ComponentType.Transform)
        except:
            pass
        if self.state == EditorState.Move:
            objTransform.position = mousePosWorld
        if self.state == EditorState.ScaleX:
            deltaMouse = mousePosWorld-self.mouseStart
            objTransform.scale.x += (math.log(max(1,deltaMouse.x+0.98)) - math.log(-min(-1,deltaMouse.x-0.98))) * math.log(objTransform.scale.x+0.6,10)/20
        if self.state == EditorState.ScaleY:
            deltaMouse = mousePosWorld-self.mouseStart
            objTransform.scale.y += (math.log(max(1,deltaMouse.y+0.98)) - math.log(-min(-1,deltaMouse.y-0.98))) * math.log(objTransform.scale.y+0.6,10)/20
        if self.state == EditorState.Rotate:
            deltaM = self.mouseStart-objTransform.position
            deltaA = mousePosWorld-objTransform.position
            mouseStartAngle = math.atan(deltaM.y/deltaM.x) if deltaM.x != 0 else math.pi/2
            mouseAngle = math.atan(deltaA.y/deltaA.x) if deltaA.x != 0 else math.pi/2
            mouseStartAngle += math.pi if deltaM.x > 0 else 0
            mouseAngle += math.pi if deltaA.x > 0 else 0
            deltaAngle = mouseAngle-mouseStartAngle
            deltaAngle = deltaAngle - (deltaAngle % (math.pi/12))
            objTransform.Rotate(deltaAngle-objTransform.rotation)
            
    
    def CheckIntersection(self, point, comp):
        verts = list()
        deltaPhi = math.pi/2
        compTransform = comp.parent.GetComponent(ComponentType.Transform)
        for i in range(4):
            verts.append(compTransform.position + Vec2(math.cos(deltaPhi*i+deltaPhi/2.0)*compTransform.scale.x*comp.lenX/2.0, math.sin(deltaPhi*i+deltaPhi/2.0)*compTransform.scale.y*comp.lenY/2.0))
        return self.PointInPolygon(point, verts)
    
    def GetWorkingComponent(self):
        if self.workingObject.HasComponent(ComponentType.Structure):
            return self.workingObject.GetComponent(ComponentType.Structure)
        if self.workingObject.HasComponent(ComponentType.Ground):
            return self.workingObject.GetComponent(ComponentType.Ground)
            
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
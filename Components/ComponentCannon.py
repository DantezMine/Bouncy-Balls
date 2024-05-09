from Components.Component import ComponentType
from Components import ComponentTransform
from Components import ComponentSprite
from Components import ComponentBall
from Components import Component
from Components import ComponentButton
from Components import ComponentBall
import GameObject
from Vector import Vec2
import GlobalVars
import pygame
import math

class Cannon(Component.Component):
    def __init__(self, position = None, rotation = None, gameStart = True):
        self.name = ComponentType.Cannon
        self.parent = None
        self.initPos = position
        self.rotation = rotation
        self.mousePressed = False
        self.mouseLeft = False
        self.cannonScale = 2
        self.lenX = self.cannonScale*0.580
        self.lenY = self.cannonScale*0.402
        self.buttonSize = 0.2
        self.ballType = ComponentBall.BallType.Bouncy
        self.state = "Selecting"
        self.slingD = 10
        self.gameStart = gameStart
        
        self.ballData = {
            ComponentBall.BallType.Bouncy : 0,
            ComponentBall.BallType.Heavy : 0
        }
        
        self.ballConstructors = {
            ComponentBall.BallType.Bouncy : ComponentBall.BallBouncy,
            ComponentBall.BallType.Heavy : ComponentBall.BallBowling
        }
        
    def Start(self):
        transform = self.parent.GetComponent(ComponentType.Transform)
        transform.position = self.initPos if self.initPos is not None else transform.position
        self.parent.AddComponent(ComponentSprite.Sprite("data/Barrel.png", self.cannonScale*0.580, self.cannonScale*0.402))
        # self.parent.AddComponent(Base(self.initPos + self.baseOffset))
        
        scene = self.parent.GetParentScene()
        #only create base if it doesn't exist in the scene yet
        if len(scene.GetComponents(ComponentType.Base)) == 0:
            cannonBase = GameObject.GameObject(scene)
            cannonBase.AddComponent(Base(Vec2(-0.4,-0.3)))
            scene.AddGameObject(cannonBase)
        
        if self.gameStart:
            ballBouncyButton = GameObject.GameObject(scene)
            ballBouncyButton.AddComponent(ComponentButton.ButtonBall(nPoly=4,lenX=self.buttonSize,lenY=self.buttonSize,position= Vec2(-1 + self.buttonSize * 2.0/3, 1 - self.buttonSize * (2.0/3 + 0 * 7.0/6)),spritePath="data/TennisBall.png", ballType = ComponentBall.BallType.Bouncy))
            scene.AddGameObject(ballBouncyButton)
            
            ballHeavyButton = GameObject.GameObject(scene)
            ballHeavyButton.AddComponent(ComponentButton.ButtonBall(nPoly=4,lenX=self.buttonSize,lenY=self.buttonSize,position= Vec2(-1 + self.buttonSize * 2.0/3, 1 - self.buttonSize * (2.0/3 + 1 * 7.0/6)),spritePath="data/BowlingBall.png", ballType = ComponentBall.BallType.Heavy))
            scene.AddGameObject(ballHeavyButton)
            
            loadCannonButton = GameObject.GameObject(scene)
            loadCannonButton.AddComponent(ComponentButton.Button(lenX=self.buttonSize,lenY=self.buttonSize,position=Vec2(-1 + self.buttonSize * 2.0/3, -1 + self.buttonSize * 2.0/3),function=self.LoadBall,atStart=False))
            scene.AddGameObject(loadCannonButton)
            
            for key in self.ballData.keys():
                if self.ballData[key] > 0:
                    self.ballType = key
            
            ball = GameObject.GameObject(scene)
            ball.AddComponent(self.ballConstructors[self.ballType]())
            scene.AddGameObject(ball)
            self.ballID = ball.GetID()     
    
    def Update(self, deltaTime):
        transform = self.parent.GetComponent(ComponentType.Transform)
        mousePos = pygame.mouse.get_pos()
        mousePos = Vec2(mousePos[0],mousePos[1])
        mousePosWorld = ComponentTransform.Transform.ScreenToWorldPos(mousePos, self.parent.GetParentScene().camera)
                
        ball = self.parent.GetParentScene().GameObjectWithID(self.ballID)
        transform = self.parent.GetComponent(ComponentType.Transform)
        ballTransform = ball.GetComponent(ComponentType.Transform)
        
        if self.state == "Selecting" or self.state == "Loaded":
            ballTransform.position = transform.position
        
        if GlobalVars.mousePressed and GlobalVars.mouseLeft:
            if self.state == "Loaded" :
                self.state = "Dragged"
            
            if self.state == "Dragged" and mousePosWorld:
                #push ball to front of barrel and project path
                deltaVec = transform.position - mousePosWorld
                delta = deltaVec.Mag()
                deltaNorm = deltaVec.Normalized()
                ballTransform.position = transform.position + deltaNorm * 0.25
                impulse = deltaNorm * math.log(1.5*delta + 1) * self.slingD
                ball.GetComponent(ComponentType.Ball).ProjectPath(40,impulse)
                
                #set cannon barrel rotation
                delta = mousePosWorld - transform.position
                if delta.x != 0:
                    self.rotation = math.atan(float(delta.y)/float(delta.x)) - 0.35
                else:
                    delta.x = 0.00001
                if delta.x > 0:
                    self.rotation += math.pi
                transform.rotation = self.rotation
                
            if self.state == "Released" and self.mouseLeft:
                self.OnClick()
        
        if not GlobalVars.mousePressed:
             if self.state == "Dragged":
                self.state = "Released"
                deltaVec = transform.position - mousePosWorld
                delta = deltaVec.Mag()
                deltaNorm = deltaVec.Normalized()
                impulse = deltaNorm * math.log(1.5*delta + 1) * self.slingD
                physics = ball.GetComponent(ComponentType.Physics)
                physics.constraintPosition = False
                physics.constraintRotation = False
                physics.AddImpulse(impulse)
                
    def LoadBall(self):
        self.state = "Loaded"
        
    def NextBall(self):
        self.state = "Selecting"
        ballType = ComponentBall.BallType.Bouncy
        for key in self.ballData.keys():
            if self.ballData[key] > 0:
                ballType = key
        self.SelectBall(ballType)
                
    def SelectBall(self, ballType):
        self.ballData[self.ballType] -= 1
        self.ballType = ballType
        self.ballData[self.ballType] += 1
        ball = self.parent.GetParentScene().GetObjectsWithComponent(ComponentType.Ball)
        ball[0].AddComponent(self.ballConstructors[self.ballType]())
        
    def Decode(self, obj):
        super().Decode(obj)
        self.mousePressed = obj["mousePressed"]
        self.mouseLeft = obj["mouseLeft"]
        self.cannonScale = obj["cannonScale"]
        self.rotation = obj["rotation"]
        self.initPos = Vec2.FromList(obj["initPos"])
    
class Base(Component.Component):
    def __init__(self, position=Vec2(0, 0), baseScale=1):
        self.name = ComponentType.Base
        self.parent = None
        self.initPos = position
        self.baseScale = 2
        
    def Start(self):
        # self.initPos += Vec2(self.baseScale*-0.1, self.baseScale*-0.15)
        # transform = self.parent.GetComponent(ComponentType.Transform)
        # transform.position = self.initPos
        self.parent.AddComponent(ComponentSprite.Sprite("data/Base.png", self.baseScale*0.615, self.baseScale*0.345))
        
    def Update(self, deltaTime):
        self.UpdatePosition()    
    
    def UpdatePosition(self):
        self.parent.GetComponent(ComponentType.Transform).position = self.parent.GetParentScene().GetObjectsWithComponent(ComponentType.Cannon)[0].GetComponent(ComponentType.Transform).position + Vec2(-0.4,-0.3)
        
    def Decode(self, obj):
        super().Decode(obj)
        self.baseScale = obj["baseScale"]
        self.initPos = Vec2.FromList(obj["initPos"])
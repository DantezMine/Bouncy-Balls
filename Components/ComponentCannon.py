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
    def __init__(self, position = None, cannonScale = 1, rotation = None):
        self.name = ComponentType.Cannon
        self.parent = None
        self.initPos = position
        self.rotation = rotation
        self.mousePressed = False
        self.mouseLeft = False
        self.cannonScale = 2
        self.lenX = self.cannonScale*0.580
        self.lenY = self.cannonScale*0.402
        self.size = 0.4
        self.ballType = ComponentBall.BallType.Bouncy
        
        self.ballData = {
            ComponentBall.BallType.Bouncy : 0,
            ComponentBall.BallType.Heavy : 0
        }
        
        self.ballConstructors = {
            ComponentBall.BallType.Bouncy : ComponentBall.BallBouncy,
            ComponentBall.BallType.Heavy : ComponentBall.BallBowling
        }
        
        self.ballData = {
            ComponentBall.BallType.Bouncy : 0,
            ComponentBall.BallType.Heavy : 0
        }
        
    def Start(self):
        transform = self.parent.GetComponent(ComponentType.Transform)
        transform.position = self.initPos if self.initPos is not None else transform.position
        self.parent.AddComponent(ComponentSprite.Sprite("data/Barrel.png", self.cannonScale*0.580, self.cannonScale*0.402))
        # self.parent.AddComponent(Base(self.initPos + self.baseOffset))
        
        ballBouncyButton = GameObject.GameObject(self.parent.GetParentScene())
        ballBouncyButton.AddComponent(ComponentButton.ButtonBall(nPoly=4,lenX=self.size,lenY=self.size,position= Vec2(-1 + self.size * 2.0/3, 1 - self.size * (2.0/3 + 0 * 7.0/6)),spritePath="data/TennisBall.png", ballType = ComponentBall.BallType.Bouncy))
        self.parent.GetParentScene().AddGameObject(ballBouncyButton)
        
        ballHeavyButton = GameObject.GameObject(self.parent.GetParentScene())
        ballHeavyButton.AddComponent(ComponentButton.ButtonBall(nPoly=4,lenX=self.size,lenY=self.size,position= Vec2(-1 + self.size * 2.0/3, 1 - self.size * (2.0/3 + 1 * 7.0/6)),spritePath="data/BowlingBall.png", ballType = ComponentBall.BallType.Heavy))
        self.parent.GetParentScene().AddGameObject(ballHeavyButton)
        
        if self.ballData[ComponentBall.BallType.Bouncy] == 0:
            self.ballType = ComponentBall.BallType.Heavy
        else:
            self.ballType = ComponentBall.BallType.Bouncy
        
        ball = GameObject.GameObject(self.parent.GetParentScene())
        ball.AddComponent(self.ballConstructors[self.ballType](self.parent))
        self.parent.GetParentScene().AddGameObject(ball)
        
        scene = self.parent.GetParentScene()
        #only create base if it doesn't exist in the scene yet
        if len(scene.GetComponents(ComponentType.Base)) == 0:
            cannonBase = GameObject.GameObject(scene)
            cannonBase.AddComponent(Base(Vec2(-0.4,-0.3)))
            scene.AddGameObject(cannonBase)
    
    def Update(self, deltaTime):
        transform = self.parent.GetComponent(ComponentType.Transform)
        mousePos = pygame.mouse.get_pos()
        mousePos = Vec2(mousePos[0],mousePos[1])
        mousePosWorld = ComponentTransform.Transform.ScreenToWorldPos(mousePos, self.parent.GetParentScene().camera)
        self.mousePressed = GlobalVars.mousePressed
                    
        if self.mousePressed:
            if self.mouseLeft:
                delta = mousePosWorld - transform.position
                if delta.x != 0 and delta.y != 0:
                    self.rotation = math.atan(float(delta.y)/float(delta.x)) - 0.35
                else:
                    print("congrats, you crashed the game")
                    GlobalVars.running = False
                if delta.x > 0:
                    self.rotation += math.pi
                transform.rotation = self.rotation
                
    def SelectBall(self, ballType):
        self.ballData[self.ballType] -= 1
        self.ballType = ballType
        self.ballData[self.ballType] += 1
        ball = self.parent.GetParentScene().GetObjectsWithComponent(ComponentType.Ball)
        ball[0].AddComponent(self.ballConstructors[self.ballType](self.parent))
        
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
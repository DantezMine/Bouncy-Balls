from Components.Component import ComponentType
from Components import ComponentSprite
from Components import Component
from Vector import Vec2
import GameObject
import enum

class GameState(enum.Enum):
    Start = enum.auto()
    Playing = enum.auto()
    Success = enum.auto()
    Fail = enum.auto()

class Manager(Component.Component):
    def __init__(self, inEditor = False):
        self.name = ComponentType.Manager
        self.parent = None
        
        self.inEditor = inEditor
        self.score = 0
        self.state = GameState.Start
        
    def Start(self):
        if self.inEditor:
            return
        self.cannon = self.parent.GetParentScene().GetComponents(ComponentType.Cannon)[0]
        self.goalField = self.parent.GetParentScene().GetComponents(ComponentType.GoalField)[0]
        self.CreateScoreDisplay()
    
    def Update(self, deltaTime):
        if self.state == GameState.Start:
            self.cannon.StartGame()
            self.state = GameState.Playing
        if self.state == GameState.Playing:
            if self.goalField.success:
                self.state = GameState.Success
                
    def AddScore(self, score):
        self.score += score
        
        for i in range(self.digits):
            number = self.score % (10**(i+1))
            self.displays[i].number = number
                
    def CreateScoreDisplay(self):
        scene = self.parent.GetParentScene()
        size = 0.2
        self.digits = 4
        self.displays = [None] * self.digits
        for i in range(self.digits):
            display = GameObject.GameObject(scene)
            display.AddComponent(ComponentSprite.SpriteUI(spritePath="data/WoodStructure.png",lenX=size,lenY=size,number=0))
            display.GetComponent(ComponentType.Transform).position = Vec2((i+1-self.digits/2.0) * size * 4.0/3,1- size * 2.0/3)
            scene.AddGameObject(display)
            self.displays[i] = display.GetComponent(ComponentType.Sprite)
            
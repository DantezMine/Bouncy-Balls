from Components.Component import ComponentType
from Components import ComponentSprite
from Components import Component
from Vector import Vec2
import GameObject
import enum
import time

class GameState(enum.Enum):
    Start = enum.auto()
    Touring = enum.auto()
    Playing = enum.auto()
    Success = enum.auto()
    Fail = enum.auto()

class Manager(Component.Component):
    def __init__(self, inEditor = False):
        self.name = ComponentType.Manager
        self.parent = None
        
        self.inEditor = inEditor
        self.score = 0
        self.tourDuration = 7
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
            self.tourStart = time.time()
            self.state = GameState.Touring
            
        if self.state == GameState.Touring:
            t = (time.time()-self.tourStart)/self.tourDuration
            if t >= 1:
                self.state = GameState.Playing
            else:
                self.TourFunction(t)
            
        if self.state == GameState.Playing:
            if self.goalField.success:
                self.state = GameState.Success
            
            if self.cannon.state == "Released":
                ball = self.parent.GetParentScene().GameObjectWithID(self.cannon.ballID)
                if ball is not None:
                    if ball.GetComponent(ComponentType.Physics).velocity.SqMag() < 0.01:
                        self.cannon.NextBall()
        
        if self.state == GameState.Fail:
            scene = self.FailScene()
            self.parent.GetParentScene().world.AddScene(scene)
            self.parent.GetParentScene().world.SetActiveScene(scene.name)
        if self.state == GameState.Success:
            scene = self.SuccessScene()
            self.parent.GetParentScene().world.AddScene(scene)
            self.parent.GetParentScene().world.SetActiveScene(scene.name)
            
    def TourFunction(self, t):
        def lerp(A, B, t):
            return A + (B-A) * t
        
        cannonTransf = self.cannon.parent.GetComponent(ComponentType.Transform)
        cameraTransf = self.parent.GetParentScene().camera.parent.GetComponent(ComponentType.Transform)
        goalTransf = self.goalField.parent.GetComponent(ComponentType.Transform)
        waitTime = 0.4
        if t < waitTime:
            cameraTransf.position = goalTransf.position
        else:
            cameraTransf.position = lerp(goalTransf.position,cannonTransf.position, t)
        
    def FailScene(self):
        import Scene
        from Components import ComponentBackground
        from Components import ComponentButton
        from Components import ComponentCamera
        import SceneSetup
        
        size = 0.2
        scene = Scene.Scene("failure")
        
        screen = GameObject.GameObject(scene)
        screen.AddComponent(ComponentBackground.Background(lenX=1,lenY=1,spritePath="data/BackgroundFailure.png"))
        scene.AddGameObject(screen)
        
        camera = GameObject.GameObject(scene)
        camera.AddComponent(ComponentCamera.Camera())
        scene.AddGameObject(camera)
        
        levelSelectButton = GameObject.GameObject(scene)
        levelSelectButton.AddComponent(ComponentButton.ButtonScene(lenX=size,lenY=size,setupFunc=SceneSetup.SetupLevelSelect, spritePath="data/Return.png", sceneName="levelSelect", position=Vec2(0,-0.6)))
        scene.AddGameObject(levelSelectButton)
        
        size = 0.178
        self.digits = 4
        displays = [None] * self.digits
        for i in range(self.digits):
            display = GameObject.GameObject(scene)
            display.AddComponent(ComponentSprite.SpriteUI(spritePath="data/GizmoSquare.png",lenX=size,lenY=size,number=0))
            display.GetComponent(ComponentType.Transform).position = Vec2((i-(self.digits-1)/2.0) * size * 3.2/3, -0.11-size/3.0)
            scene.AddGameObject(display)
            displays[i] = display.GetComponent(ComponentType.Sprite)
            
        intermediate = self.score
        for i in range(self.digits,0,-1):
            number = intermediate // (10**(i))
            intermediate -= number * 10**(i)
            displays[i-1].number = number
        
        return scene
    
    def SuccessScene(self):
        import Scene
        from Components import ComponentBackground
        from Components import ComponentButton
        from Components import ComponentCamera
        import SceneSetup
        
        size = 0.2
        scene = Scene.Scene("success")
        
        screen = GameObject.GameObject(scene)
        screen.AddComponent(ComponentBackground.Background(lenX=1,lenY=1,spritePath="data/BackgroundSuccess.png"))
        scene.AddGameObject(screen)
        
        camera = GameObject.GameObject(scene)
        camera.AddComponent(ComponentCamera.Camera())
        scene.AddGameObject(camera)
        
        levelSelectButton = GameObject.GameObject(scene)
        levelSelectButton.AddComponent(ComponentButton.ButtonScene(lenX=size,lenY=size,setupFunc=SceneSetup.SetupLevelSelect, spritePath="data/Return.png", position=Vec2(0,-0.6)))
        levelSelectButton.GetComponent(ComponentType.Button).sceneName = "levelSelect"
        scene.AddGameObject(levelSelectButton)
        
        size = 0.178
        self.digits = 4
        displays = [None] * self.digits
        for i in range(self.digits):
            display = GameObject.GameObject(scene)
            display.AddComponent(ComponentSprite.SpriteUI(spritePath="data/GizmoSquare.png",lenX=size,lenY=size,number=0))
            display.GetComponent(ComponentType.Transform).position = Vec2((i-(self.digits-1)/2.0) * size * 3.2/3, -0.11-size/3.0)
            scene.AddGameObject(display)
            displays[i] = display.GetComponent(ComponentType.Sprite)
            
        intermediate = self.score
        for i in range(self.digits,0,-1):
            number = intermediate // (10**(i))
            intermediate -= number * 10**(i)
            displays[i-1].number = number
        
        return scene
                
    def AddScore(self, score):
        self.score += score
        
        intermediate = self.score
        for i in range(self.digits-1,-1,-1):
            number = intermediate // (10**i)
            intermediate -= number * 10**i
            self.displays[i].number = number
                
    def CreateScoreDisplay(self):
        scene = self.parent.GetParentScene()
        size = 0.2
        self.digits = 4
        self.displays = [None] * self.digits
        for i in range(self.digits):
            display = GameObject.GameObject(scene)
            display.AddComponent(ComponentSprite.SpriteUI(spritePath="data/WoodStructure.png",lenX=size,lenY=size,number=0))
            display.GetComponent(ComponentType.Transform).position = Vec2((self.digits-i-self.digits/2.0) * size * 4.0/3,1- size * 2.0/3)
            scene.AddGameObject(display)
            self.displays[i] = display.GetComponent(ComponentType.Sprite)
            
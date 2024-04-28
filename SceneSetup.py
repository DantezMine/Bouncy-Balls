import Scene
import GameObject
from Vector import Vec2
import GlobalVars
from Components import ComponentStructure
from Components import ComponentSlider
from Components import ComponentBall
from Components import ComponentCamera
from Components import ComponentGround
from Components import ComponentBackground
from Components import ComponentCannon
from Components import ComponentButton
from Components import ComponentGoalField
from Components import ComponentEditor

def SetupScene1(world):
    scene = Scene.Scene("scene")
    world.AddScene(scene)
    
    width, height = GlobalVars.screen.get_width(), GlobalVars.screen.get_height()
    
    background = GameObject.GameObject(scene)
    background.AddComponent(ComponentBackground.BackgroundNature(Vec2(0,0),width,height))
    scene.AddGameObject(background)
    
    camera = GameObject.GameObject(scene)
    camera.AddComponent(ComponentCamera.Camera(Vec2(0,0),1.0/3.0))
    scene.AddGameObject(camera)
    
    struct1 = GameObject.GameObject(scene)
    struct1.AddComponent(ComponentStructure.StructureWood(Vec2(0.5,1),0.25,1.0))
    scene.AddGameObject(struct1)
    
    struct3 = GameObject.GameObject(scene)
    struct3.AddComponent(ComponentStructure.StructureWood(Vec2(0,0),0.25,1.0,1.57075))
    scene.AddGameObject(struct3)
    
    struct4 = GameObject.GameObject(scene)
    struct4.AddComponent(ComponentStructure.StructureWood(Vec2(-1,1),0.25,1.0,0.3))
    # scene.AddGameObject(struct4)
    
    ground1 = GameObject.GameObject(scene)
    ground1.AddComponent(ComponentGround.GroundDirt(Vec2(0,-2.5),6.0,1.0))
    scene.AddGameObject(ground1)
    
    cannon = GameObject.GameObject(scene)
    cannon.AddComponent(ComponentCannon.Cannon(Vec2(-1,-1)))
    scene.AddGameObject(cannon)
    
    ball = GameObject.GameObject(scene)
    ball.AddComponent(ComponentBall.BallBouncy(cannon))
    scene.AddGameObject(ball)
    
    button1 = GameObject.GameObject(scene)
    button1.AddComponent(ComponentButton.Button(nPoly=4,radius=0.8,position=Vec2(0,0)))
    #scene.AddGameObject(button1)
    
    goalField = GameObject.GameObject(scene)
    goalField.AddComponent(ComponentGoalField.GoalField(Vec2(2,0),1,0.5))
    #scene.AddGameObject(goalField)
    
    slider1 = GameObject.GameObject(scene)
    slider1.AddComponent(ComponentSlider.Slider(Vec2(-1,0),Vec2(1,0),0,5,0.1))
    #scene.AddGameObject(slider1)
    
    lvlSelectButton1 = GameObject.GameObject(scene)
    lvlSelectButton1.AddComponent(ComponentButton.ButtonLevel(nPoly=4,radius=0.5,position=Vec2(-2.5,2.5),scenePath="Levels/levelSelect.json"))
    scene.AddGameObject(lvlSelectButton1)
    
def SetupLevelSelect(world):
    scene = Scene.Scene("levelSelect")
    world.AddScene(scene)
    
    background = GameObject.GameObject(scene)
    background.AddComponent(ComponentBackground.BackgroundNature(position=Vec2(0,0),lenX=1,lenY=1))
    scene.AddGameObject(background)
    
    camera = GameObject.GameObject(scene)
    camera.AddComponent(ComponentCamera.Camera(position=Vec2(0,0),scale=1))
    scene.AddGameObject(camera)
    
    lvlButton1 = GameObject.GameObject(scene)
    lvlButton1.AddComponent(ComponentButton.ButtonLevel(nPoly=4,radius=0.2,position=Vec2(-0.7,0.7),scenePath="Levels/levelTest.json"))
    scene.AddGameObject(lvlButton1)
    

def SetupMainMenu(world):
    scene = Scene.Scene("mainMenu")
    world.AddScene(scene)
    
    background = GameObject.GameObject(scene)
    background.AddComponent(ComponentBackground.BackgroundNature(position=Vec2(0,0),lenX=1,lenY=1))
    scene.AddGameObject(background)
    
    camera = GameObject.GameObject(scene)
    camera.AddComponent(ComponentCamera.Camera(position=Vec2(0,0),scale=1))
    scene.AddGameObject(camera)
    
    levelSelectButton = GameObject.GameObject(scene)
    levelSelectButton.AddComponent(ComponentButton.ButtonLevel(nPoly=4,lenX=0.5, lenY=0.15, position=Vec2(0,0.1), scenePath="Levels/levelSelect.json", spritePath="data/ButtonStart.png"))
    scene.AddGameObject(levelSelectButton)
    
    levelEditorButton = GameObject.GameObject(scene)
    levelEditorButton.AddComponent(ComponentButton.ButtonLevel(nPoly=4,lenX=0.5, lenY=0.15, position=Vec2(0,-0.1), setupFunc=SetupEditor, sceneName="editor", spritePath="data/ButtonEditor.png"))
    scene.AddGameObject(levelEditorButton)
    
def SetupEditor(world):
    scene = Scene.Scene("editor")
    world.AddScene(scene)
    
    background = GameObject.GameObject(scene)
    background.AddComponent(ComponentBackground.BackgroundNature(position=Vec2(0,0),lenX=1,lenY=1))
    scene.AddGameObject(background)
    
    camera = GameObject.GameObject(scene)
    camera.AddComponent(ComponentCamera.Camera(position=Vec2(0,0),scale=1,boundLen=Vec2(10,10)))
    scene.AddGameObject(camera)
    
    editor = GameObject.GameObject(scene)
    editor.AddComponent(ComponentEditor.Editor())
    scene.AddGameObject(editor)
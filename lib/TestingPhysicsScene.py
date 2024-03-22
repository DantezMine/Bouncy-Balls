import Scene
import GameObject
import BehaviorTesting
import ComponentCollider
import ComponentPhysics
import ComponentSprite
import ballscript
from Vector import Vec2

from lib import MovingCollision

def SetupScene1(world):
    scene = Scene.Scene()
    world.AddScene("scene",scene)

    rect1 = GameObject.GameObject(scene)
    rect1.AddComponent(MovingCollision.MovingCollision())
    rect1.GetComponent("Transform").position = Vec2(360,150)
    # rect1.GetComponent("Transform").rotation = 0.035
    rect1.AddComponent(ComponentPhysics.Physics())
    
    rect2 = GameObject.GameObject(scene)
    rect2.AddComponent(MovingCollision.MovingCollision())
    rect2.GetComponent("Transform").position = Vec2(400,250)
    rect2.AddComponent(ComponentPhysics.Physics())
    rect2.GetComponent("Transform").rotation = 0.035
    rect2.GetComponent("Physics").constraintPosition = True
    rect2.GetComponent("Physics").constraintRotation = True
        
    scene.AddGameObject(rect1)
    scene.AddGameObject(rect2)
    
def SetupScene2(world):
    scene = Scene.Scene()
    world.AddScene("scene",scene)
    ball = GameObject.GameObject(scene)
    behaviourTesting = BehaviorTesting.BehaviorTesting()
    ball.AddComponent(behaviourTesting)
    scene.AddGameObject(ball)
    
def SetupScene3(world):
    scene = Scene.Scene()
    world.AddScene("scene",scene)
    slingshot = GameObject.GameObject(scene)
    ball = GameObject.GameObject(scene)
    ball.AddComponent(ComponentSprite.Sprite(b_proc=False, s_spritePath="data/SlimeBallMC.png"))
    slingshot.GetComponent("Transform").position = Vec2(200,400)
    ball.AddComponent(ballscript.Ball())
    ball.GetComponent("Ball").sling = slingshot
    ball.GetComponent("Transform").scale = Vec2(.2,.2)
    scene.AddGameObject(ball)
    scene.AddGameObject(slingshot)
    
def SetupScene4(world):
    scene = Scene.Scene()
    world.AddScene("scene",scene)
    ball1 = GameObject.GameObject(scene)
    ball1.AddComponent(ballscript.Ball())
    ball1.AddComponent(ComponentPhysics.Physics())
    ball1.GetComponent("Transform").position = Vec2(180,200)
    ball1.GetComponent("Physics").gravity = True
    ball2 = GameObject.GameObject(scene)
    ball2.AddComponent(ballscript.Ball())
    ball2.AddComponent(ComponentPhysics.Physics())
    ball2.GetComponent("Transform").position = Vec2(200,400)
    ball2.GetComponent("Physics").constraintPosition = True
    
    scene.AddGameObject(ball1)
    scene.AddGameObject(ball2)

def SetupScene5(world):
    scene = Scene.Scene()
    world.AddScene("scene",scene)
    ball = GameObject.GameObject(scene)
    ball.AddComponent(ballscript.Ball())
    ball.AddComponent(ComponentPhysics.Physics())
    ball.GetComponent("Physics").gravity = True
    ball.GetComponent("Transform").position = Vec2(280,200)
    
    rect = GameObject.GameObject(scene)
    rect.AddComponent(MovingCollision.MovingCollision())
    rect.GetComponent("Transform").position = Vec2(200,400)
    rect.AddComponent(ComponentPhysics.Physics())
    rect.GetComponent("Physics").constraintPosition = True
    rect.GetComponent("Physics").constraintRotation = True
    
    scene.AddGameObject(ball)
    scene.AddGameObject(rect)
    
    #example for what adding a structure should look like. minimal clutter, only add one component
    # block1 = GameObject.GameObject(scene)
    # block1.AddComponent(Structure("Wood",posX=300,posY=350,lenX=20,lenY=100))
    # scene.AddGameObject(block1)
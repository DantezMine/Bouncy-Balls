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
    rect1.GetComponent("Transform").position = Vec2(399,150)
    rect1.AddComponent(ComponentPhysics.Physics())
    rect1.GetComponent("Physics").velocity = Vec2(0,100)
    rect1.GetComponent("Physics").constraintRotation = False
    
    rect2 = GameObject.GameObject(scene)
    rect2.AddComponent(MovingCollision.MovingCollision())
    rect2.GetComponent("Transform").position = Vec2(400,250)
    rect2.AddComponent(ComponentPhysics.Physics())
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
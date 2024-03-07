import Scene
import GameObject
import Scene
import GameObject
import BehaviorTesting
import ComponentCollider
import ComponentPhysics
from Vector import Vec2

from lib import MovingCollision

def SetupScene1(world):
    scene = Scene.Scene()
    world.AddScene("scene",scene)

    rect1 = GameObject.GameObject(scene)
    rect1.AddComponent(MovingCollision.MovingCollision())
    rect1.GetComponent("MovingCollision").controllable = True
    rect1.GetComponent("Transform").position = Vec2(350,150)
    rect1.AddComponent(ComponentPhysics.Physics())
    
    rect2 = GameObject.GameObject(scene)
    rect2.AddComponent(MovingCollision.MovingCollision())
    rect1.GetComponent("MovingCollision").velocity = Vec2(0,1)
    rect2.GetComponent("Transform").position = Vec2(400,450)
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
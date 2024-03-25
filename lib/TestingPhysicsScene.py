import Scene
import GameObject
import ComponentPhysics
from Vector import Vec2
import ComponentBall

from lib import MovingCollision

def SetupScene1(world):
    scene = Scene.Scene()
    world.AddScene("scene",scene)

    rect1 = GameObject.GameObject(scene)
    rect1.AddComponent(MovingCollision.MovingCollision())
    rect1.GetComponent("Transform").position = Vec2(310,150)
    rect1.AddComponent(ComponentPhysics.Physics())
    
    rect2 = GameObject.GameObject(scene)
    rect2.AddComponent(MovingCollision.MovingCollision())
    rect2.GetComponent("Transform").position = Vec2(320,250)
    rect2.AddComponent(ComponentPhysics.Physics())
    rect2.GetComponent("Transform").rotation = 0.785
    rect2.GetComponent("Physics").constraintPosition = True
    rect2.GetComponent("Physics").constraintRotation = True
        
    scene.AddGameObject(rect1)
    scene.AddGameObject(rect2)
    
    #example for what adding a structure should look like. minimal clutter, only add one component
    # block1 = GameObject.GameObject(scene)
    # block1.AddComponent(Structure("Wood",posX=300,posY=350,lenX=20,lenY=100))
    # scene.AddGameObject(block1)
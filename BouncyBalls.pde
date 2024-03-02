import World
import Scene
import GameObject
import BehaviorTesting

world = World.World()
scene = Scene.Scene()
ball = GameObject.GameObject(scene)
behaviourTesting = BehaviorTesting.BehaviorTesting()
ball.AddComponent(behaviourTesting)
scene.AddGameObject(ball)
world.AddScene("scene",scene)

def setup():
    size(400,400)
    world.StartActiveScene()

def draw():
    background(255)
    world.UpdateActiveScene()
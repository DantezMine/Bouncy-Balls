import World
from lib import TestingPhysicsScene

world = World.World()
change = 0

def setup():
    size(600,600)
    TestingPhysicsScene.SetupScene3(world)
    world.StartActiveScene()

def draw():
    background(255)
    world.UpdateActiveScene()
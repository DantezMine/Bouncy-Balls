import World
from lib import TestingPhysicsScene

world = World.World()
change = 0

def setup():
    size(600,600)
    TestingPhysicsScene.SetupScene1(world)
    world.StartActiveScene()

def draw():
    background(255)
    world.UpdateActiveScene()
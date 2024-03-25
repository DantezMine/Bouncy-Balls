import World
from lib import TestingPhysicsScene
from lib import GlobalVars

world = World.World()
GlobalVars.debug = False

def setup():
    size(600,600)
    TestingPhysicsScene.SetupScene1(world)
    world.StartActiveScene()
    GlobalVars.frameCount = 0

def draw():
    if not GlobalVars.debug:
        background(255)
        world.UpdateActiveScene(1/60.0, 10)
        GlobalVars.frameCount += 1

    else:
        if GlobalVars.update or GlobalVars.step:
            GlobalVars.step = False
            GlobalVars.frameCount += 1
            print("Frame #%s"%GlobalVars.frameCount)
            background(255)
            world.UpdateActiveScene(1/60.0, 10)
        if keyPressed and GlobalVars.keyReleased:
            if key == " ":
                GlobalVars.step = True
                GlobalVars.keyReleased = False
            if key == "k":
                GlobalVars.update = False if GlobalVars.update else True
                GlobalVars.keyReleased = False
        if not keyPressed:
            GlobalVars.keyReleased = True
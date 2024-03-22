import World
from lib import TestingPhysicsScene
from lib import GlobalVars

world = World.World()
change = 1
 
def setup():
    size(600,600)
    TestingPhysicsScene.SetupScene5(world)
    world.StartActiveScene()

def draw():
    background(255)
    world.UpdateActiveScene(1/60.0)
    # if GlobalVars.update or GlobalVars.step:
    #     GlobalVars.step = False
    #     background(255)
    #     world.UpdateActiveScene(1/60.0)
    # if keyPressed and GlobalVars.keyReleased:
    #     if key == " ":
    #         GlobalVars.step = True
    #         GlobalVars.keyReleased = False
    #     if key == "k":
    #         GlobalVars.update = False if GlobalVars.update else True
    #         GlobalVars.keyReleased = False
    # if not keyPressed:
    #     GlobalVars.keyReleased = True

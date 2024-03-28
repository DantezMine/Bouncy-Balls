import pygame
import World
from lib import TestingPhysicsScene
from lib import GlobalVars

world = World.World()
GlobalVars.debug = False

'''pygame setup'''
pygame.init()
GlobalVars.screen = pygame.display.set_mode((600,600))
GlobalVars.clock = pygame.time.Clock()
GlobalVars.running = True
TestingPhysicsScene.SetupScene1(world)
world.StartActiveScene()
GlobalVars.frameCount = 0

'''pygame loop'''
while GlobalVars.running:
    if not GlobalVars.debug:
        GlobalVars.screen.fill((255,255,255))
        world.UpdateActiveScene(updateFrequency=10)
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

    GlobalVars.clock.tick(60)
    pygame.display.flip()
    
pygame.quit
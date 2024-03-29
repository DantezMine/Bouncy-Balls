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
GlobalVars.frameCount = 0
world.StartActiveScene()

'''pygame loop'''
while GlobalVars.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GlobalVars.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                GlobalVars.running = False
            if event.key == pygame.K_k and GlobalVars.keyReleased:
                GlobalVars.update = False if GlobalVars.update else True
                GlobalVars.keyReleased = False
            if event.key == pygame.K_SPACE and GlobalVars.keyReleased:
                GlobalVars.step = True
                GlobalVars.keyReleased = False
        else:
            GlobalVars.keyReleased = True
    
    if not GlobalVars.debug:
        GlobalVars.screen.fill((255,255,255))
        world.UpdateActiveScene(deltaTime=1.0/60.0,updateFrequency=10)
        GlobalVars.frameCount += 1

    else:
        if GlobalVars.update or GlobalVars.step:
            GlobalVars.step = False
            GlobalVars.frameCount += 1
            print("Frame #%s"%GlobalVars.frameCount)
            GlobalVars.screen.fill((255,255,255))
            world.UpdateActiveScene(deltaTime=1/60.0, updateFrequency=10)

    GlobalVars.clock.tick(60)
    pygame.display.flip()
    
pygame.quit
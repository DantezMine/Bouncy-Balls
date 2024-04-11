import pygame
import World
import time
import json
from lib import TestingPhysicsScene
from lib import GlobalVars
from Vector import Vec2
import Scene

world = World.World()
GlobalVars.debug = False

'''pygame setup'''
pygame.init()
GlobalVars.screen     = pygame.display.set_mode((600,600))
GlobalVars.background = pygame.Surface((600,600))
GlobalVars.foreground = pygame.Surface((600,600), pygame.SRCALPHA, 32)
GlobalVars.foreground = GlobalVars.foreground.convert_alpha()
GlobalVars.UILayer = pygame.Surface((600,600), pygame.SRCALPHA, 32)
GlobalVars.UILayer = GlobalVars.UILayer.convert_alpha()
GlobalVars.clock = pygame.time.Clock()
GlobalVars.running = True

TestingPhysicsScene.SetupScene1(world)
GlobalVars.frameCount = 0

world.StartActiveScene()
with open("levelTest.json","w") as fp:
    world.GetActiveScene().WriteJSON(fp)

with open("levelTest.json","r") as fp:
    world.RemoveScene("scene")
    scene = Scene.Scene("scene")
    scene.Decode(json.load(fp=fp))


'''pygame loop'''
while GlobalVars.running:
    t1 = time.time()
    GlobalVars.events = pygame.event.get()
    GlobalVars.mousePosScreen = Vec2.FromList(pygame.mouse.get_pos())
    for event in GlobalVars.events:
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
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            GlobalVars.mousePressed = True
            if event.button == pygame.BUTTON_LEFT:
                GlobalVars.mouseLeft = True
        elif event.type == pygame.MOUSEBUTTONUP:
            GlobalVars.mousePressed = False
            GlobalVars.mouseLeft = False
            
                
    if not GlobalVars.debug or GlobalVars.update or GlobalVars.step:
        GlobalVars.background.fill((0,0,0,0))
        GlobalVars.foreground.fill((0,0,0,0))
        GlobalVars.UILayer.fill((0,0,0,0))
        GlobalVars.screen.fill((255,255,255))
        deltaTime = 1/60.0 if GlobalVars.debug else None
        world.UpdateActiveScene(deltaTime=1/60.0,updateFrequency=10)
        GlobalVars.screen.blit(GlobalVars.background,(0,0))
        GlobalVars.screen.blit(GlobalVars.foreground,(0,0))
        GlobalVars.screen.blit(GlobalVars.UILayer,(0,0))
        GlobalVars.frameCount += 1
        
        if GlobalVars.debug:
                GlobalVars.step = False
                print("Frame #%s"%GlobalVars.frameCount)

    GlobalVars.clock.tick(120)
    pygame.display.flip()
    #print(1/(time.time()-t1))
pygame.quit
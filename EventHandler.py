from lib import GlobalVars
import pygame
from Vector import Vec2

def HandleEvents():
    GlobalVars.events = pygame.event.get()
    GlobalVars.mousePosScreen = Vec2.FromList(pygame.mouse.get_pos())
    GlobalVars.scrollEvent = None
    
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
            if event.button == pygame.BUTTON_MIDDLE:
                GlobalVars.mouseMid = True
            if event.button == pygame.BUTTON_RIGHT:
                GlobalVars.mouseRight = True
        elif event.type == pygame.MOUSEBUTTONUP:
            GlobalVars.mousePressed = False
            GlobalVars.mouseLeft = False
            GlobalVars.mouseMid = False
            GlobalVars.mouseRight = False
            GlobalVars.scrollEvent = None
        
        if event.type == pygame.MOUSEWHEEL:
            GlobalVars.scrollEvent = event
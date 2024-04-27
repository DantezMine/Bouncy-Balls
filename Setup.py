from lib import TestingPhysicsScene
from lib import GlobalVars
import pygame

def RunSetup(world):
    GlobalVars.debug = False
    GlobalVars.updateFrequency = 10

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

    TestingPhysicsScene.SetupEditor(world)
    GlobalVars.frameCount = 0
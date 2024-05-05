import SceneSetup
import GlobalVars
import pygame

def RunSetup(world):
    GlobalVars.debug = False
    GlobalVars.updateFrequency = 10
    size = (800,800)

    '''pygame setup'''
    pygame.init()
    GlobalVars.screen     = pygame.display.set_mode(size)
    GlobalVars.background = pygame.Surface(size)
    GlobalVars.foreground = pygame.Surface(size, pygame.SRCALPHA, 32)
    GlobalVars.foreground = GlobalVars.foreground.convert_alpha()
    GlobalVars.UILayer = pygame.Surface(size, pygame.SRCALPHA, 32)
    GlobalVars.UILayer = GlobalVars.UILayer.convert_alpha()
    GlobalVars.clock = pygame.time.Clock()
    GlobalVars.running = True

    SceneSetup.SetupMainMenu(world)
    GlobalVars.frameCount = 0
import pygame
import EventHandler
import GlobalVars

def RunGame(world):
    '''pygame loop'''
    while GlobalVars.running:
        EventHandler.HandleEvents()
                    
        if not GlobalVars.debug and GlobalVars.update and GlobalVars.step:
            GlobalVars.background.fill((0,0,0,0))
            GlobalVars.foreground.fill((0,0,0,0))
            GlobalVars.UILayer.fill((0,0,0,0))
            GlobalVars.screen.fill((255,255,255))
            
            deltaTime = 1/60.0 if GlobalVars.debug else None
            world.UpdateActiveScene(deltaTime=1/60.0,updateFrequency=GlobalVars.updateFrequency)
            
            GlobalVars.screen.blit(GlobalVars.background,(0,0))
            GlobalVars.screen.blit(GlobalVars.foreground,(0,0))
            GlobalVars.screen.blit(GlobalVars.UILayer,(0,0))
            GlobalVars.frameCount += 1
            
            if GlobalVars.debug:
                    GlobalVars.step = False
                    print("Frame #%s"%GlobalVars.frameCount)

        GlobalVars.clock.tick(120)
        pygame.display.flip()
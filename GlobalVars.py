import pygame
from Vector import Vec2

membersOffset : int = 8
update : bool = True
step : bool = True
keyReleased : bool = True
frameCount : int = 0
debug : bool = False
screen : pygame.Surface = None
background : pygame.Surface = None
foreground : pygame.Surface = None
UILayer : pygame.Surface = None
clock = None
running : bool = False
updateFrequency : int = 1

mousePosScreen : Vec2 = None
mouseChanged : bool = False
mousePressed : bool = False
mouseLeft : bool = False
mouseMid : bool = False
mouseRight : bool = False
scrollEvent : pygame.event = None
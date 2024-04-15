import pygame
from Vector import Vec2

update : bool = True
step : bool = True
keyReleased : bool = True
frameCount : int = 0
debug : bool= False
screen : pygame.Surface = None
background : pygame.Surface = None
foreground : pygame.Surface = None
UILayer : pygame.Surface = None
clock = None
running : bool = None

mousePosScreen : Vec2 = None
mousePressed : bool = None
mouseLeft : bool = None
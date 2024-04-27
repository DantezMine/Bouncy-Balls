import pygame
import World
import Setup
import GameLoop

if __name__ == "__main__":
    world = World.World()
    Setup.RunSetup(world)
    world.StartActiveScene()
    GameLoop.RunGame(world)
    pygame.quit

# with open("Bouncy-Balls/Levels/levelTest.json","w") as fp:
#     world.GetActiveScene().WriteJSON(fp)

# with open("Bouncy-Balls/Levels/levelSelect.json","w") as fp:
#     world.GetScene("levelSelect").WriteJSON(fp)
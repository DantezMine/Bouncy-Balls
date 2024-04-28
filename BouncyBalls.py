import pygame
import World
import Setup
import GameLoop

if __name__ == "__main__":
    world = World.World()
    Setup.RunSetup(world)
    world.StartActiveScene()
    # with open("Bouncy-Balls/Levels/Editor.json","w") as fp:
    #     world.GetScene("editor").WriteJSON(fp)
    GameLoop.RunGame(world)
    pygame.quit


# with open("Bouncy-Balls/Levels/levelSelect.json","w") as fp:
#     world.GetScene("levelSelect").WriteJSON(fp)
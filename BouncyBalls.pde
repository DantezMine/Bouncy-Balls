import World
import Scene
import GameObject
import ComponentSprite

world = World.World()
scene = Scene.Scene()
ball = GameObject.GameObject(scene)
ballSprite = ComponentSprite.ComponentSpriteBallSlime(False, "SlimeBallMC.png")
ball.AddComponent(ballSprite)
scene.AddGameObject(ball)
world.AddScene("scene",scene)

def setup():
    size(400,400)

def draw():
    background(255)
    world.UpdateActiveScene()
from World import World
from Scene import Scene
from GameObject import GameObject
from ComponentSprite import ComponentSprite

world = World()
scene = Scene()
ball = GameObject(scene)
ballSprite = ComponentSprite.ComponentSpriteBallSlime(b_proc=True)
ball.AddComponent(ballSprite)
scene.AddGameObject(ball)
world.AddScene("scene",scene)

def setup():
    size(400,400)

def draw():
    background(255)
    world.UpdateActiveScene()
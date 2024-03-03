import World
import Scene
import GameObject
import BehaviorTesting

import ComponentCollider
from Vector import Vec2

world = World.World()
scene = Scene.Scene()
ball = GameObject.GameObject(scene)
behaviourTesting = BehaviorTesting.BehaviorTesting()
ball.AddComponent(behaviourTesting)
#scene.AddGameObject(ball)
world.AddScene("scene",scene)

rect1 = GameObject.GameObject(scene)
rectColl1 = ComponentCollider.ColliderRect()
rectColl1.SetCollider(100,50)
rect1.AddComponent(rectColl1)
rect2 = GameObject.GameObject(scene)
rectColl2 = ComponentCollider.ColliderRect()
rectColl2.SetCollider(100,50)
rect2.AddComponent(rectColl2)



def setup():
    size(600,600)
    world.StartActiveScene()
    rect2.GetComponent("Transform").position = Vec2(400,450)

def draw():
    background(255)
    world.UpdateActiveScene()
    rect1.GetComponent("Transform").position = Vec2(mouseX,mouseY)
    rect1.GetComponent("Transform").rotation = 0.3
    fill(0,255,0,10)
    if rect1.GetComponent("Collider").BoolCollision([rect1.GetComponent("Collider"),rect2.GetComponent("Collider")]):
        fill(255,0,0,10)
    stroke(0)
    rectMode(CENTER)
    pushMatrix()
    translate(mouseX,mouseY)
    rotate(rect1.GetComponent("Transform").rotation)
    rect(0,0,rectColl1.lenX,rectColl1.lenY)
    popMatrix()
    rect(rect2.GetComponent("Transform").position.x,rect2.GetComponent("Transform").position.y,rectColl2.lenX,rectColl2.lenY)
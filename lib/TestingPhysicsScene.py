import Scene
import GameObject
from Vector import Vec2
from Components import ComponentStructure
from Components import ComponentBall
from Components import ComponentCamera
from Components import ComponentGround
from Components import ComponentBackground
from Components import ComponentCannon

from lib import GlobalVars

def SetupScene1(world):
    scene = Scene.Scene("scene")
    world.AddScene(scene.name,scene)
    
    width, height = GlobalVars.screen.get_width(), GlobalVars.screen.get_height()
    
    background = GameObject.GameObject(scene)
    background.AddComponent(ComponentBackground.BackgroundNature(Vec2(0,0),width,height))
    scene.AddGameObject(background)
    
    camera = GameObject.GameObject(scene)
    camera.AddComponent(ComponentCamera.Camera(Vec2(0,0),1.0/3.0))
    scene.AddGameObject(camera)
    
    # struct1 = GameObject.GameObject(scene)
    # struct1.AddComponent(ComponentStructure.StructureWood(Vec2(0.5,-1.5),0.25,1.0))
    # scene.AddGameObject(struct1)
    
    # struct4 = GameObject.GameObject(scene)
    # struct4.AddComponent(ComponentStructure.StructureWood(Vec2(-1,1),0.25,1.0,0.3))
    # scene.AddGameObject(struct4)
    
    # struct2 = GameObject.GameObject(scene)
    # struct2.AddComponent(ComponentStructure.StructureWood(Vec2(-0.5,-1.5),0.25,1.0))
    # scene.AddGameObject(struct2)
    
    # struct3 = GameObject.GameObject(scene)
    # struct3.AddComponent(ComponentStructure.StructureWood(Vec2(0,-0.75),0.25,1.0,1.57075))
    # scene.AddGameObject(struct3)
    
    ground1 = GameObject.GameObject(scene)
    ground1.AddComponent(ComponentGround.GroundDirt(Vec2(0,-2.5),6.0,1.0))
    scene.AddGameObject(ground1)
    
    cannon = GameObject.GameObject(scene)
    cannon.AddComponent(ComponentCannon.Cannon(Vec2(-1,-1)))
    scene.AddGameObject(cannon)
    
    cannonBase = GameObject.GameObject(scene)
    cannonBase.AddComponent(ComponentCannon.Base(Vec2(-1,-1)))
    scene.AddGameObject(cannonBase)
    
    # for i in range(10):
        # struct = GameObject.GameObject(scene)
        # struct.AddComponent(ComponentStructure.StructureWood(Vec2(60*i,300),50,100))
        # scene.AddGameObject(struct)
    
    
    
    #example for what adding a structure should look like. minimal clutter, only add one component
    # block1 = GameObject.GameObject(scene)
    # block1.AddComponent(Structure("Wood",posX=300,posY=350,lenX=20,lenY=100))
    # scene.AddGameObject(block1)
    
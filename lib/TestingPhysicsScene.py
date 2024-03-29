import Scene
import GameObject
from Vector import Vec2
import ComponentStructure
import ComponentBall
import ComponentGround
import ComponentBackground
from lib import GlobalVars

def SetupScene1(world):
    scene = Scene.Scene("scene")
    world.AddScene(scene.name,scene)
    
    width, height = GlobalVars.screen.get_width(), GlobalVars.screen.get_height()
    
    background = GameObject.GameObject(scene)
    background.AddComponent(ComponentBackground.BackgroundNature(Vec2(width/2,height/2),width,height))
    scene.AddGameObject(background)
    
    struct1 = GameObject.GameObject(scene)
    struct1.AddComponent(ComponentStructure.StructureWood(Vec2(270,300),25,100))
    scene.AddGameObject(struct1)
    
    struct2 = GameObject.GameObject(scene)
    struct2.AddComponent(ComponentStructure.StructureWood(Vec2(230,300),25,100))
    scene.AddGameObject(struct2)
    
    struct3 = GameObject.GameObject(scene)
    struct3.AddComponent(ComponentStructure.StructureWood(Vec2(270,200),25,100,1.57075))
    scene.AddGameObject(struct3)
    
    ground1 = GameObject.GameObject(scene)
    ground1.AddComponent(ComponentGround.GroundDirt(Vec2(300,525),600,150))
    scene.AddGameObject(ground1)
    
    # for i in range(10):
        # struct = GameObject.GameObject(scene)
        # struct.AddComponent(ComponentStructure.StructureWood(Vec2(60*i,300),50,100))
        # scene.AddGameObject(struct)
    
    
    
    #example for what adding a structure should look like. minimal clutter, only add one component
    # block1 = GameObject.GameObject(scene)
    # block1.AddComponent(Structure("Wood",posX=300,posY=350,lenX=20,lenY=100))
    # scene.AddGameObject(block1)
    
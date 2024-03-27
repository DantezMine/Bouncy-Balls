import Scene
import GameObject
import ComponentStructure
from Vector import Vec2
import ComponentBall

def SetupScene1(world):
    scene = Scene.Scene("scene")
    world.AddScene(scene.name,scene)
    
    struct1 = GameObject.GameObject(scene)
    struct1.AddComponent(ComponentStructure.StructureWood(Vec2(300,300),25,100))
    scene.AddGameObject(struct1)
    
    struct2 = GameObject.GameObject(scene)
    struct2.AddComponent(ComponentStructure.StructureWood(Vec2(200,300),100,200))
    scene.AddGameObject(struct2)
    
    for i in range(10):
        struct = GameObject.GameObject(scene)
        struct.AddComponent(ComponentStructure.StructureWood(Vec2(60*i,300),50,100))
        scene.AddGameObject(struct)
    
    
    
    #example for what adding a structure should look like. minimal clutter, only add one component
    # block1 = GameObject.GameObject(scene)
    # block1.AddComponent(Structure("Wood",posX=300,posY=350,lenX=20,lenY=100))
    # scene.AddGameObject(block1)
    
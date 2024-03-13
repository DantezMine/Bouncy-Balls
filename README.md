# Bouncy-Balls

## The Core Engine

### UML: Core Engine Diagram

<img src = "README-Graphics/Bouncy-Balls/UML-Diagrams/UML-Diagrams.svg">

### The World

The World is a container that stores all the scenes in a dictionary by their name.  
Scenes can be added with world.AddScene(sceneName,scene) and removed with world.RemoveScene(sceneName). There is always one active scene which can be set with the world.SetActiveScene(sceneName) function and is the scene that is displayed and worked on.<br>
The world gives the command for initializing the scene with world.StartActiveScene() and updating it each frame with world.UpdateActiveScene(). The UpdateActiveScene function can take in an optional parameter, deltaTime.<br>
DeltaTime (in mathematical notation: &Delta;t) is the time that passes between one frame and the next. If there are 60 frames per second, the deltaTime each frame will be 1/60, or 16ms. Passing in a fixed deltaTime will ignore the actual time between frames and always work with the given value. This is mostly relevant for the physics engine, where the distance objects move is based on deltaTime, based on numerical methods such as Euler or Verlet Integration.<br>

><font color="lightblue">AddScene(sceneName,scene) </font>: Add a scene along with its name to find it later again<br>
<font color="lightblue">RemoveScene(sceneName) </font>: Removes the scene by its name from the worlds dictionary<br>
<font color="lightblue">SetActiveScene(sceneName) </font>: Sets the scene with the matching name to the active scene.<br>
<font color="lightblue">StartActiveScene() </font>: Tell the scene to initialize all its GameObjects<br>
<font color="lightblue">StartUpdateScene(deltaTime = None) </font>: Tell the scene to update all its GameObjects<br>

### The Scene

The Scene is another container, this time for GameObjects, with some additional functionality compared to the world. Each scene can be thought of as more or less a seperate level of a game, although the start menu or level selector can be their own seperate scenes too.<br>
GameObjects can be added to and removed from the scenes list with the scene.AddGameObject(gameObject) and scene.RemoveGameObject(gameObject) functions. When a GameObject is added to the scene, it receives an ID from the scene, which is just a counter from to the scene class, so GameObjects across different scenes will never have the same ID.<br>
The scene can be queried for GameObjects with components or the components from the GameObjects themselves. This means, for example, if you want to collect every collider in the scene, you can call scene.GetComponents(compName) or scene.GetObjectsWithComponent(compName) to get a list of all the colliders or objects with colliders.<br>
Finally, the scene has a start and update function which get called by the world and never by anything else. The Update function is special in that it first updates all the generic components from all its game objects, then the scenes collider detection, then the scenes physics response and finally draws the objects to the screen. Seperating these steps through the list of GameObjects is important for more accurate and realistic physics.<br>

><font color="lightblue"> AddGameObject(gameObject) </font>: Adds the GameObject to the scenes list<br>
<font color="lightblue">RemoveGameObject(gameObject) </font>: Removes the GameObject from the scenes list<br>
<font color="lightblue">GetComponents(compName) </font>: Returns a list of all the components with the matching component name from the scenes list of GameObjects<br>
<font color="lightblue">GetObjectsWithComponent(compName) </font>: Returns a list of all GameObjects that have a component with the maching component name from the scenes list of GameObjects<br>

### GameObject

GameObjects are the basis of the game engine. Everything that exists in the game is a GameObject, where the individual GameObjects can be modified by using components and their respective variables. A GameObject is once again just a container, this time for Components, with additional functionality. Each GameObject holds a dictionary of its components, by the component.name variable, as well as an individual ID, assigned to it by its parent scene. Only one component of each type can be assigned to a single GameObject at any given time so that there is no risk of conflicting processes.
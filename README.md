# Bouncy-Balls
## uml: sequence diagram
Here I will embed PlantUML markup to generate a sequence diagram.

I can include as many plantuml segments as I want in my Markdown, and the diagrams can be of any type supported by PlantUML.

```plantuml
@startuml
    skinparam backgroundColor #00000000
    class World{
        {field} - scenes : dict
        {field} - activeScene : Scene
        {method} + AddScene(sceneName, scene) : bool
        {method} + RemoveScene(sceneName) : bool
        {method} + SetActiveScene(sceneName) : bool
        {method} + StartActiveScene()
        {method} + UpdateActiveScene(deltaTime=None)
    }

@enduml
```
import Component

class ComponentSpriteClass(Component.Component):
    def __init__(self):
        self.name = "Sprite"
        
    def Update(self):
        fill(0)
        ellipse(mouseX,mouseY,30,30)
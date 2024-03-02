import Component

class ComponentSprite(Component.Component):
    def __init__(self, b_proc):
        self.name = "Sprite"
        self.b_proc = b_proc
        
    def Update(self):
        if self.b_proc:
            self.DisplayProc()
        else:
            self.DisplayImg()
            
    def DisplayProc(self):
        pass
    
    def DisplayImg(self):
        pass
    
class ComponentSpriteBallSlime(ComponentSprite):
    # def __init__(self,b_proc):
    #     super().__init__(b_proc)
    
    def DisplayProc(self):
        fill(51,255,51)
        stroke(20,200,20)
        strokeWeight(2)
        ellipse(mouseX,mouseY,30,30)
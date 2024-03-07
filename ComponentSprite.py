import Component

class Sprite(Component.Component):
    def __init__(self, b_proc, s_spritePath = None): #if b_proc is False, s_spritePath must be given
        self.name = "Sprite"
        self.b_proc = b_proc
        self.spritePath = s_spritePath
        self.parent = None
        
    def Update(self,deltaTime):
        if self.b_proc:
            self.DisplayProc()
        else:
            self.DisplayImg()
            
    def DisplayProc(self):
        pass
    
    def DisplayImg(self):
        pass
    
class SpriteBallSlime(Sprite):
    # def __init__(self,b_proc):
    #     super().__init__(b_proc)
    
    def DisplayProc(self):
        fill(51,255,51)
        stroke(20,200,20)
        strokeWeight(2)
        ellipse(mouseX,mouseY,30,30)
        
    def DisplayImg(self):
        parentTransform = self.parent.GetComponent("Transform")
        sprite = loadImage(self.spritePath)
        pushMatrix()
        translate(parentTransform.position.x, parentTransform.position.y)
        rotate(parentTransform.rotation)
        image(sprite,-sprite.width*parentTransform.scale.x/2,-sprite.height*parentTransform.scale.y/2,sprite.width*parentTransform.scale.x,sprite.height*parentTransform.scale.y)
        popMatrix()
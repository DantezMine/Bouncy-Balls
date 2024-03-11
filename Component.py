class Component:
    def __init__(self):
        self.name = None #needs to be set in each component class individually
        self.parent = None
    
    def Start(self):
        pass
    
    def Update(self,deltaTime):
        pass
    
    def OnCollision(self,collider):
        pass
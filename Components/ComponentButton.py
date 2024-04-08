import pygame
import math
from Components import Component
from Components import ComponentTransform
from Components.Component import Components
from lib import GlobalVars
from Vector import Vec2

class Button(Component.Component):
    def __init__(self, nPoly = 4, radius = 0.2, position = Vec2(0,0)):
        self.name = Components.Button
        self.parent = None
        
        self.nPoly = nPoly
        self.radius = radius
        self.startPosition = position
        
    def Start(self):
        self.transform = self.parent.GetComponent(Components.Transform)
        self.transform.position = self.startPosition
        self.verts = self.GetVertices()
        
    def Update(self, deltaTime):
        self.verts = self.GetVertices()
        mousePosWorld = ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen,self.parent.GetParentScene().camera)
        self.PointInPolygon(mousePosWorld)
        
    def PointInPolygon(self,point):
        inside = True
        for i in range(self.nPoly):
            A = self.verts[i]
            B = self.verts[(i+1)%self.nPoly]
            normal = (B-A).Perp()
            AP = point-A
            if normal.Dot(AP) < 0:
                inside = False
        return inside
    
    def GetVertices(self):
        verts = list()
        deltaPhi = 2*math.pi/self.nPoly
        for i in range(self.nPoly):
            verts.append(self.transform.position + Vec2(math.cos(deltaPhi*i+deltaPhi/2.0),math.sin(deltaPhi*i+deltaPhi/2.0)) * self.radius)
        return verts
    
    def DisplayButtonOutline(self, color):
        vertices = []
        for v in self.verts:
            vertScreen = ComponentTransform.Transform.WorldToScreenPos(v,self.parent.GetParentScene().camera)
            vertices.append((vertScreen.x,vertScreen.y))
        pygame.draw.polygon(GlobalVars.UILayer,color,vertices,1)
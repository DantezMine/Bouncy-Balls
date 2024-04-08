import pygame
from Components import ComponentTransform
from Components import Component
from Components.Component import Components
from lib import GlobalVars
from Vector import Vec2

class Slider(Component.Component):
    def __init__(self, pos1, pos2, minValue, maxValue, step = 1):
        self.name = Components.Slider
        self.parent = None
        
        self.minValue = minValue
        self.maxValue = maxValue
        self.step = max(0.0001,step)
        self.SetPos(pos1,pos2)
        self.Value = minValue
        
    def Update(self, deltaTime):
        if GlobalVars.mousePressed:
            if GlobalVars.mouseLeft:
                self.CirclePos = self.GetClosestPointOnLine(self.pos1, self.pos2, ComponentTransform.Transform.ScreenToWorldPos(GlobalVars.mousePosScreen,self.parent.GetParentScene().camera))
                self.Value = self.GetValue()    #has to be run after GetClosestPointToLine
        self.DisplaySlider()
                
    def DisplaySlider(self):
        camera = self.parent.GetParentScene().camera
        pos1Screen = ComponentTransform.Transform.WorldToScreenPos(self.pos1,camera)
        pos2Screen = ComponentTransform.Transform.WorldToScreenPos(self.pos2,camera)
        circlePosScreen = ComponentTransform.Transform.WorldToScreenPos(self.CirclePos,camera)
        pygame.draw.line(GlobalVars.UILayer,(51,51,51),(pos1Screen.x,pos1Screen.y),(pos2Screen.x,pos2Screen.y))
        pygame.draw.ellipse(GlobalVars.UILayer,(150,20,150),(circlePosScreen.x-5,circlePosScreen.y-5,10,10))
    
    def SetPos(self, pos1,pos2):
        self.pos1 = pos1
        self.pos2 = pos2
        self.CirclePos = self.pos1

    def GetClosestPointOnLine(self,A,B,P):
        AP = A-P                #vector from point to beginning of slider/line
        AB = B-A                #vector from beginning to end of slider
        
        magAB = AB.Mag()                     #length of the slider 
        ab_to_ap_dot = AB.Dot(AP)            #dot product from ab to ap (not sure why, don't understand the math yet)
        distance = -ab_to_ap_dot/magAB        #distance from beginning of slider to the closest point
        if distance < 0:                     #beyond beginning
            ClosestPoint = A                 
        elif distance > magAB:               #beyond end
            ClosestPoint = B
        else:
            stepLength = (self.maxValue-self.minValue)/self.step                    #distance to travel on slider for each step
            distance = int(stepLength * distance / AB.Mag()) * (AB.Mag() / stepLength)  #round to step length
            ClosestPoint =  A + AB.Normalized() * distance                          #multiply normalized slider vector with distance to get closest point 
        if (ClosestPoint-P).SqMag() < 1:                                            #only return closest point if mouse is close enough to slider, else just give the last position of the circle
            print(ClosestPoint, distance)
            return ClosestPoint
        return self.CirclePos
    
    def GetValue(self):
        sliderLength = (self.pos1-self.pos2).Mag()                                  #the length of the slider
        distanceOnSlider = (self.pos1-self.CirclePos).Mag()                         #how far the point is along the slider
        distRatio = max(0,min(distanceOnSlider / sliderLength,1))                   #mapping the previous distance between 0 and 1
        UnalteredValue = self.minValue + (self.maxValue-self.minValue)*distRatio    #lerp between smallest and biggest value of slider with previous value
        Value = int(UnalteredValue/self.step) * self.step                           #divide value by step size, round to int, then multiply by step size ==> rounding to step size
        return Value
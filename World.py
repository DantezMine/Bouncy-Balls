import time

class World:
    def __init__(self):
        self.__scenes = {key: value for key, value in []} #initialize an empty dictionary using dictionary comprehension
        self.__activeSceneKey = None
        self.__activeScene = None
        self.__prevTime = None
        
    def AddScene(self, sceneName, scene):
        if len(self.__scenes) == 0:
            self.__activeSceneKey = sceneName
            self.__activeScene = scene
        if self.__scenes.__contains__(sceneName):
            inp = input("Scene %s already exists. Do you want to replace it? " %sceneName)
            if inp == "yes" or inp == "Yes" or inp == "YES" or inp == "y":
                self.__scenes[sceneName] = scene
                return True
            else:
                return False
        self.__scenes[sceneName] = scene
        return True
    
    def RemoveScene(self, sceneName):
        if self.__scenes.__contains__(sceneName):
            self.__scenes.pop(sceneName)
            return True
        return False
    
    def UpdateActiveScene(self):
        deltaTime = self.CalculateDeltaTime()
        self.__activeScene.UpdateScene(deltaTime)
    
    def StartActiveScene(self):
        self.__activeScene.StartScene()
        
    def SetActiveScene(self,sceneName):
        if self.__scenes.__contains__(sceneName):
            self.__activeScene = self.__scenes[sceneName]
            self.__activeSceneKey = sceneName
            return True
        print("Scene %s doesn't exist"%sceneName)
        return False
        
    def CalculateDeltaTime(self):
        dt = time.time()-self.__prevTime if self.__prevTime is not None else 0
        self.__prevTime = time.time()
        return dt
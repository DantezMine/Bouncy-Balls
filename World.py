import Scene

class World:
    def __init__(self):
        self.__scenes = {key: value for key, value in []} #initialize an empty dictionary using dictionary comprehension
        
    def AddScene(self, sceneName, scene):
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
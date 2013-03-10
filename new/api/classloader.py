import sys
import inspect
class Loader():

    def __init__(self):
        self.modules = {}

    def load(self, modulePath):
        module = __import__(modulePath)
        self.modules[modulePath] = sys.modules[modulePath]
   
    def get(self, modulePath):
        return self.modules[modulePath]

    def isLoaded(self, modulePath):
        return modulePath in self.modules

    def reload(self, modulePath):
        self.unload(modulePath)
        self.load(modulePath)

    def unload(self, modulePath):
        del sys.modules[modulePath]
        del self.modules[modulePath]

    def getClass(self, modulePath):
        '''
        Returns the first defined class of a module.
        '''
        module = self.get(modulePath)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                return obj
        

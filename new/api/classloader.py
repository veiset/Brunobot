import sys
import inspect
class Loader():
    '''
    Class for loading, unloading and reloading python modules.
    '''

    def __init__(self):
        self.modules = {}

    def load(self, modulePath):
        '''
        Loads a module from module path.

        Keyword arguments:
        moduelPath -- module path (e.g: test.mockapi)
        '''
        module = __import__(modulePath)
        self.modules[modulePath] = sys.modules[modulePath]
   
    def get(self, modulePath):
        '''
        Returns the reference to a loaded module.
        
        Keyword arguments:
        moduelPath -- module path (e.g: test.mockapi)
        '''
        return self.modules[modulePath]

    def isLoaded(self, modulePath):
        '''
        Checks whether a module is loaded or not.

        Keyword arguments:
        moduelPath -- module path (e.g: test.mockapi)
        '''
        return modulePath in self.modules

    def reload(self, modulePath):
        '''
        Reloads a given module. 

        Keyword arguments:
        moduelPath -- module path (e.g: test.mockapi)
        '''
        self.unload(modulePath)
        self.load(modulePath)

    def unload(self, modulePath):
        '''
        Unloads a module.

        Keyword arguments:
        moduelPath -- module path (e.g: test.mockapi)
        '''
        del sys.modules[modulePath]
        del self.modules[modulePath]

    def getClass(self, modulePath):
        '''
        Returns the first defined class of a module.

        Keyword arguments:
        moduelPath -- module path (e.g: test.mockapi)
        '''
        module = self.get(modulePath)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                return obj
        

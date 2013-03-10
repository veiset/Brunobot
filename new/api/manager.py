import api.base
import api.classloader

class Manager():

    def __init__(self):
        self.loader = api.classloader.Loader()
        self.api = {}
        self.modules = {}


    def add(self, modulePath, name):
        self.modules[name] = modulePath
        
    def load(self, name):
        if hasModuel(name): 
            modulePath = getModulePath(name)
            loadMoadule(modulePath)
        else:
            raise Exception("Module %s is not added.", name)


    def loadModule(self, modulePath):
        if not self.loader.isLoaded(modulePath):
            self.loader.load(modulePath)

        return self.loader.get(modulePath)

    def hasModule(self, name):
        return name in self.modules

    def getModulePath(self, name):
        return self.modules[name]

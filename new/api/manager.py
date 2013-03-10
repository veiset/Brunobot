import api.base
import api.classloader

class APILoader():
    def __init__(self, manager, name):
        self.manager = manager
        self.name = name

    def load(self):
        return self.manager.getSimpleAPI(self.name)

class Manager():

    def __init__(self, bot):
        self.bot = bot
        self.loader = api.classloader.Loader()
        self.modules = {}
        self.simpleapi = {}


    def add(self, modulePath, name):
        self.modules[name] = modulePath
        
    def load(self, name):
        if self.hasModule(name): 
            self.loader.load(self.getModulePath(name))
            self.makeSimpleAPI(name)
        else:
            raise Exception("Module %s is not added.", name)

    def get(self, name):
        return APILoader(self, name).load

    def getSimpleAPI(self, name):
        return self.simpleapi[name]
        
    def reload(self, name):
        modulePath = self.getModulePath(name)
        self.loader.reload(modulePath)
        self.makeSimpleAPI(name)

    def makeSimpleAPI(self, name):
        modulePath = self.getModulePath(name)
        apiClass = self.loader.getClass(modulePath)
        apiInstance = apiClass(self.bot)
        self.simpleapi[name] = api.base.SimpleAPI(apiInstance)

    def getModulePath(self, name):
        return self.modules[name]

    def hasModule(self, name):
        return name in self.modules


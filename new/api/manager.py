import api.base
import api.classloader

class APILoader():
    '''
    This class is used as a wrapper for the Simple API interface class.

    Using this class allows modules to call the newest version of the
    loaded API. 
    '''
    def __init__(self, manager, name):
        self.manager = manager
        self.name = name

    def load(self):
        '''
        Returns the managers current version of the SimpleAPI representation
        of a Brunobot API module.
        '''
        return self.manager.getSimpleAPI(self.name)

class Manager():
    ''' 
    Class for managing Brunobot API modules.
    '''

    def __init__(self, bot):
        self.bot = bot
        self.loader = api.classloader.Loader()
        self.modules = {}
        self.simpleapi = {}

    def add(self, apiPath, name):
        '''
        Adds a new API module.

        Keyword arguments:
        apiPath -- path of the Burnobot API module (e.g: api.users.users)
        name       -- API name
        '''
        self.modules[name] = apiPath
        self.load(name)
        
    def load(self, name):
        '''
        Loads a module and creates a simple API representation of the 
        Brunobot API module.

        Keyword arguments:
        name -- name of Brunobot API to load
        '''
        if self.hasModule(name): 
            self.loader.load(self.getAPIPath(name))
            self.makeSimpleAPI(name)
        else:
            raise Exception("Module %s is not added." % name)

    def get(self, name):
        '''
        Returns an API loader. The loader is provided so that when reloading a
        Brunobot API module, the newest representation of the api will be
        used by the module using the API loader.

        Keyword arguments:
        name -- name of the Brunobot API
        '''
        return APILoader(self, name).load

    def getSimpleAPI(self, name):
        '''
        Returns the simple API representation of the Brunobot API module.

        Keyword arguments:
        name -- name of the Brunobot API
        '''
        return self.simpleapi[name]
        
    def reload(self, name):
        '''
        Reloads a loaded API module.

        Keyword arguments:
        name -- name of the Brunobot API
        '''
        apiPath = self.getAPIPath(name)
        self.loader.reload(apiPath)
        self.makeSimpleAPI(name)

    def reloadAll(self):
        '''
        Reloads all the loaded modules.
        '''
        for name in self.modules:
            if self.isLoaded(name):
                self.reload(name)

    def makeSimpleAPI(self, name):
        '''
        Loads the class of a Brunobot API module, an creates a simple API module
        of it. This is done by looking up the first class occurance in the
        classloader.

        Keyword arguments:
        name -- name of the Brunobot API
        '''
        apiPath = self.getAPIPath(name)
        apiClass = self.loader.getClass(apiPath)
        apiInstance = apiClass(self.bot)
        self.simpleapi[name] = api.base.SimpleAPI(apiInstance)


    def getAPIPath(self, name):
        return self.modules[name]

    def hasModule(self, name):
        return name in self.modules

    def isLoaded(self, name):
        return name in self.simpleapi


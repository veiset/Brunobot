import config as cfg
import sys
import inspect
class ModuleManager():
    '''
    The ModuleManager manages the core modules
    such as communication and connection, as well
    as the user defined modules located in module/extra.
    
    It contains information about which modules that
    are loaded.
    '''

    def __init__(self):
        '''
        Load the core modules, as well as the user defined
        extra modules defined in the config file (config.py).
        '''

        sys.path.append('module/core')
        self.mcore = {}
        self.mextra = []
        self.mplugin = []
        
        self.loadCore()

        import loadmodule
        self.moduleLoader = loadmodule.ModuleLoader(self)
        self.dynamicLoader = loadmodule.DynamicLoad(self.moduleLoader)

        for module in cfg.modules_extra:
            self.loadModule(module)


    def loadModule(self,name):
        '''
        Load a module using the module loader. 
        '''

        module = self.moduleLoader.load(name)
        if (inspect.ismodule(module)):
            print module
            self.mextra.append(module)
        else:
            print "!!!! Error loading module:" + module


    def loadCore(self):
        '''
        Load the core modules required for the bot,
        and passing referances to the core modules
        required for initializing them. 
        '''

        import communication
        import cparser as parser
        import connection
        import recentdata
        import corecmd
        self.mcore['connection'] = connection.Connection(
                cfg.nick,
                cfg.ident,
                cfg.name)

        self.mcore['communication'] = communication.Communication(self.mcore['connection'])
        self.mcore['recentdata'] = recentdata.Data()
        self.mcore['parser'] = parser.Parser(self)
        self.mcore['corecmd'] = corecmd.CoreCMD(self)


    def listening(self, keyword):
        '''
        Return: a list of modules that listens to
        a given keyword.
        '''

        modules = []
        for module in self.mextra:
            for k in module.listen:
                if (k == keyword):
                    modules.append(module)

        return modules


    def coreModules(self):
        '''
        TODO: Remove this
        '''

        return self.mcore

    def core(self,name):
        ''' 
        Checking for name in core, i.e:
        that a core module with the name 
        'name' is loaded.
        '''

        try: return self.mcore[str(name)]
        except: return None
    
    def extra(self,name):
        ''' 
        Checking for name in extra, i.e:
        that an extra module with the name 
        'name' is loaded.
        '''

        for mod in self.mextra:
            if mod.name == name:
                return mod
        return None

#    
#    def plugin(self,name):
#        try: return self.mplugin[name]
#        except: return None
    

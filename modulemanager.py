__author__  = 'Vegard Veiset'
__email__   = 'veiset@gmail.com'
__license__ = 'GPL'

import config as cfg
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

        self.mcore = {}
        self.mextra = []
        self.mplugin = []

        self.cmdlist = {}
        
        self.loadCore()

        import module.core.loadmodule as loadmodule
        self.moduleLoader = loadmodule.ModuleLoader(self)
        self.dynamicLoader = loadmodule.DynamicLoad(self.moduleLoader)

        for module in cfg.modules_extra:
            self.loadModule(module)


    def loadModule(self,name):
        '''
        Load a module using the module loader. 
        '''

        module, result = self.moduleLoader.load(name)
        if (inspect.ismodule(module)):
            if (self.isCmd(module)):
                for cmd in module.cmd:
                    cmd[self.cmdlist] = module

            print ' .. Loaded module %s %s' % (module.name, module.version) 
            self.mextra.append(module)
        else:
            print " !! could not load module with name: %s" % name

    def loadCore(self):
        '''
        Load the core modules required for the bot,
        and passing referances to the core modules
        required for initializing them. 
        '''

        import module.core.communication as communication
        import module.core.cparser as parser
        import module.core.connection as connection
        import module.core.recentdata as recentdata
        import module.core.corecmd as corecmd
        import module.core.presist as presist
        import module.core.auth as auth

        self.mcore['connection'] = connection.Connection(
                cfg.nick,
                cfg.ident,
                cfg.name)
        
        self.mcore['auth'] = auth.Auth()
        self.mcore['communication'] = communication.Communication(self.mcore['connection'])
        self.mcore['recentdata'] = recentdata.Data()
        self.mcore['parser'] = parser.Parser(self)
        self.mcore['corecmd'] = corecmd.CoreCMD(self)
        self.mcore['presist'] = {}

    def isCmd(self, module, keyword='cmd'):
        if not (inspect.ismodule(module)):
            try: module = self.extra(module)
            except: ''' ++ Warning: isCmd() - no such module '''

        try: 
            for listen in module.listen:
                if listen == keyword:
                    return True
        except:
            print ' ++ isCmd() - no such module '

        return False

    def requires(self, module, keyword):
        if inspect.ismodule(module):
            for req in module.require:
                if (req == keyword):
                    return True

        return False

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


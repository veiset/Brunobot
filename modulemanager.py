import config as cfg
import sys
class ModuleManager():
    
    def __init__(self):
        sys.path.append('module/core')
        #sys.path.append('module/extra')
        #sys.path.append('module/plugin')
        self.mcore = {}
        self.mextra = []
        self.mplugin = []
        
        self.loadCore()

        import loadmodule
        self.moduleLoader = loadmodule.ModuleLoader(self)

        for module in cfg.modules_extra:
            self.loadModule(module)

        #import typofixer
        #typofixer.communication = self.mcore['communication']
        #typofixer.recentdata = self.mcore['recentdata']
        #self.mextra.append(typofixer)

    def loadModule(self,name):
        module = self.moduleLoader.load(name)
        if (type(module) is not str):
            print module
            self.mextra.append(module)
        else:
            print "!!!! Error loading module:" + module

    def loadCore(self):
        import communication
        import cparser as parser
        import connection
        import recentdata
        self.mcore['connection'] = connection.Connection(
                cfg.nick,
                cfg.ident,
                cfg.name)

        self.mcore['communication'] = communication.Communication(self.mcore['connection'])
        self.mcore['recentdata'] = recentdata.Data()
        self.mcore['parser'] = parser.Parser(self)

    def listening(self, keyword):
        modules = []
        for module in self.mextra:
            for k in module.listen:
                if (k == keyword):
                    modules.append(module)

        return modules

    def coreModules(self):
        return self.mcore

    def core(self,name):
        print self.mcore[name]
        try: return self.mcore[name]
        except: return None
    
#    def extra(self,name):
#        try: return self.mextra[name]
#        except: return None
#    
#    def plugin(self,name):
#        try: return self.mplugin[name]
#        except: return None
    


class ModuleLoader():
        

    def __init__(self,modules):
        self.modules = modules
        self.require_modules = modules.mcore.keys() # modules.mcore
        self.listen_actions = ['privmsg','channel','system']
    
    def validateModule(self,name):
        import sys
        sys.path.append('module/extra')
        sys.path.append('module/plugin')

        print type(name),name 
        module = None
        version = None
        require = 0
        listen = 0
    
        author = None # Optional
        url = None # Optional
    
        # loading the module
        try: module = __import__(name)
        except: return 'no such module; "%s".' % name
    
        # checking for module description
        try: version = module.version
        except: return 'no version number found.'
    
        try: name = module.name
        except: return 'no name is defined.'
        
        try:
            for r in module.require:
                for m in self.require_modules:
                    if (r==m): require += 1
            if (require != len(module.require)): 
                return 'could not require modules defined.'
        except: return 'could not find requirements (require).'
    
        try:
            for l in module.listen:
                for a in self.listen_actions:
                    if (l==a): listen += 1
            if (listen != len(module.listen)):
                return 'could not determine actions to listen on.'
        except: return 'could not find actions to listen on (listen).'
    
        # TODO: this should also check for method arguments
        if not (getattr(module,'main')):
            return 'no main method ( def main(...) ).'
    
        return module
    
    def load(self,name):
        module = self.validateModule(name)
        # injecting depcendencies
        if (type(module) is not str):
            for coremodule in module.require:
                vars(module)[coremodule] = self.modules.mcore[coremodule]

        return module

#print validateModule('typofixer')

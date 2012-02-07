import sys
import inspect
import urllib2
import os 

class ModuleLoader():
        

    def __init__(self,modules):
        self.modules = modules
        self.require_modules = modules.mcore.keys() # modules.mcore
        self.listen_actions = ['privmsg','channel','system','cmd']
    
    def validateModule(self,name):
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
        except: return 'no such module "%s", or error with imports in module.' % name
    
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
        if (inspect.ismodule(module)):
            for coremodule in module.require:
                vars(module)[coremodule] = self.modules.mcore[coremodule]

        else:
            try: del sys.modules[name]
            except: ''' do nothing '''
        return module


class DynamicLoad():
    
    def __init__(self, moduleloader):
        self.mloader = moduleloader


    def load(self,name):
        if not (self.mloader.modules.extra(name)):
            module = self.mloader.load(name)

            if (inspect.ismodule(module)):
                self.mloader.modules.mextra.append(module)
                return (True,'Module %s %s loaded.' % (module.name, module.version), module)
            else:
                try: del sys.modules[name]
                except: ''' do nothing '''
                return (False,'Error: %s' % module)
        else:
            return (False,'Error: Module with that name already loaded')


    def unload(self,name):
        mod = self.mloader.modules.extra(name)
        if (mod):
            self.mloader.modules.mextra.remove(mod)
            try: del sys.modules[name]
            except: ''' nothing ''' 
            return (True,'Module %s %s unloaded' % (mod.name, mod.version))
        else:
            return (False,'Error: no such module.')


    def reloadm(self,name):
        u = self.unload(name)
        if (u[0]):
            l = self.load(name)
            if (l[0]):
                return 'Module %s reloaded.' % name
            else:
                return 'Error: %s' % l[1]
        else:
            return 'Error: %s' % u[1]

    

    def download(self,url):
        response = None
        html = None

         
        response = urllib2.urlopen(url)
        html = response.readlines()
        #except: return ('Error: Could not read file from URL')

        f = open('tmpmodule.py','w')
        for line in html:
            f.write(line)
        f.close()

        tmpmod = self.load('tmpmodule')[2]
        name = tmpmod.name
        version = tmpmod.version
        require = ", ".join(tmpmod.require)
        listen = ", ".join(tmpmod.listen)

        extra_info = []
        try: extra_info.append("Author: " + tmpmod.author)
        except: extra_info.append("Author: uknown")
        try: extra_info.append("url: " + tmpmod.url)
        except: extra_info.append("url: unknown")

        extra_info = ", ".join(extra_info)
        
        f = open('module/extra/%s.py' % name,'w')
        for line in html:
            f.write(line)
        f.close()

        os.remove('tmpmodule.py')

        self.load(name)
        return 'Module: %s %s REQUIRE[%s] LISTEN[%s] %s' % (name, version, require, listen, extra_info)

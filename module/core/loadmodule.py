import sys
import inspect
import urllib2
import os 

class ModuleLoader():
    '''
    ModuleLoader.
    Validates a module to check if it contains  all the
    information required for it to be a brunobot plugin.
    It also check if the module to be loaded has a main
    method to be run when the corresponding action is 
    detected by the parser.

    This module is to load module/extra plugins at the
    start of the bot. 
    '''

    def __init__(self,modules):
        '''
        Require the moudle manager and use 
        the modules from it to validate the new
        modules to load.
        '''

        self.modules = modules
        self.require_modules = modules.mcore.keys() # modules.mcore
        self.listen_actions = ['privmsg','channel','system','cmd']
    
    def validateModule(self,name):
        '''
        Validating that the specified module (name)
        can be loaded and used as a Brunobot plugin.

        Checking that source file of the plugin 
        contains all the required fields and the 
        method that is to be run when called (main).
        '''

        sys.path.append('module/extra')
        sys.path.append('module/plugin')

        module = None
        version = None
        require_count = 0
        listen_count = 0
    
        author = None # Optional
        url = None # Optional
    
        # loading the module
        try: module = __import__(name)
        except: return 'no such module "%s", or errors with the code of the module.' % name
    
        # checking for module description
        try: version = module.version
        except: return 'no version number found.'
    
        try: name = module.name
        except: return 'no name is defined.'
        
        try:
            for require in module.require:
                for mod in self.require_modules:
                    if (require==mod): require_count += 1

            if (require_count != len(module.require)): 
                return 'could not require modules defined.'
        except: return 'could not find requirements (require).'
    
        try:
            for listen in module.listen:
                for action in self.listen_actions:
                    if (listen==action): listen_count += 1

            if (listen_count != len(module.listen)):
                return 'could not determine actions to listen on.'
        except: return 'could not find actions to listen on (listen).'
    
        # TODO: this should also check for method arguments
        if not (inspect.isfunction(getattr(module,'main'))):
            return 'no main method ( def main(...) ).'
    
        # TODO: check for CMD list, help and description

        return module
    
    def load(self,name):
        '''
        Tries to validate the module based the name. 
        If the module is a valid module it will be injected
        with the required core modules asked for by the 
        module.
        '''

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
    '''
    Dynamic loader.
    Takes user model name as userinput, and uses the 
    ModuleLoader to load, reload, unload, and validate
    that the model is in fact a brunobot plugin. 
    '''

    def __init__(self, moduleloader):
        '''
        Keeps a referance to the module loader for
        validating the modules that are to be loaded.
        '''

        self.mloader = moduleloader


    def load(self,name):
        '''
        Load a module based on its name. 
        Will validate it using the ModuleLoader.
        
        return (True, module)     if successful
        return (False, errorMSG)  if unsuccessful
        '''

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
        '''
        Unload a module based on its name. 

        return (True, msg)       if successful
        return (True, errorMSG)  if unsuccessful
        '''

        mod = self.mloader.modules.extra(name)
        if (mod):
            self.mloader.modules.mextra.remove(mod)
            try: del sys.modules[name]
            except: ''' nothing ''' 
            return (True,'Module %s %s unloaded' % (mod.name, mod.version))
        else:
            return (False,'Error: no such module.')


    def reloadm(self,name):
        '''
        Reload a module. 
        Uses the methods unload and load.

        Returns a message of how the reload went.
        '''

        unload = self.unload(name)
        if (unload[0]):
            load = self.load(name)
            if (load[0]):
                return 'Module %s reloaded.' % name
            else:
                return 'Error: %s' % load[1]
        else:
            return 'Error: %s' % unload[1]

    

    def download(self,url):
        ''' 
        Downloading a python module from the web and
        loads it using the load method.

        It will try to download the file and write it to disk.
        If the module is valid then it will be loaded. 
        '''

        response = None
        html = None

         
        try: 
            response = urllib2.urlopen(url)
            html = response.readlines()
        except: return ('Error: Could not read file from URL')

        try:
            f = open('tmpmodule.py','w')
            for line in html:
                f.write(line)
            f.close()
        except: return ('Error: Could not write to temp file')

        tmpimport = self.load('tmpmodule')
        if (tmpimport[0]):
            tmpmod = tmpimport[2]
            name = tmpmod.name
            version = tmpmod.version
            require = ", ".join(tmpmod.require)
            listen = ", ".join(tmpmod.listen)
        else:
            return tmpimport[1]

        extra_info = []
        try: extra_info.append("Author: " + tmpmod.author)
        except: extra_info.append("Author: uknown")
        try: extra_info.append("url: " + tmpmod.url)
        except: extra_info.append("url: unknown")

        extra_info = ", ".join(extra_info)
       
        try:
            f = open('module/extra/%s.py' % name,'w')
            for line in html:
                f.write(line)
            f.close()
        except: 
            return "Error: could not write module to module/extra/%s.py" % name

        os.remove('tmpmodule.py')

        self.load(name)
        
        return 'Module: %s %s REQUIRE[%s] LISTEN[%s] %s' % (name, version, require, listen, extra_info)

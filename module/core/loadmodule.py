__author__  = 'Vegard Veiset'
__email__   = 'veiset@gmail.com'
__license__ = 'GPL'

import sys
import inspect
import urllib2
import os 
import presist
import module.test.moduletest as moduletest

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
    
    def validateModule(self,name,verbose=False):
        '''
        Validating that the specified module (name)
        can be loaded and used as a Brunobot plugin.

        Checking that source file of the plugin 
        contains all the required fields and the 
        method that is to be run when called (main).
        '''

        try: 
            module = __import__("module.extra." + name)
            module = sys.modules["module.extra." + name]
        except: 
            errors = [['Loading module',('no such module "%s", or errors syntax errors within the code of the module.' % name)]]

            return (None,(False, (0,0), errors, None, None))
        try:
            reload(sys.modules['module.extra.%s' + name])
        except:
            ''' Do nothing '''

        return (module, moduletest.validateModule(module,verbose))

        

        # TODO: this should also check for method arguments
        if not (inspect.isfunction(getattr(module,'main'))):
            return 'no main method ( def main(...) ).'
    
        # TODO: check for CMD list, help and description

        return module
    
    def load(self,name,verbose=False):
        '''
        Tries to validate the module based the name. 
        If the module is a valid module it will be injected
        with the required core modules asked for by the 
        module.
        '''

        module, result = self.validateModule(name,verbose)
        # injecting depcendencies
        if (inspect.ismodule(module)):
            for coremodule in module.require:
                if coremodule is 'presist':
                    vars(module)['presist'] = presist.Presist(module,module.presist)
                    module.presist.load()
                else:
                    vars(module)[coremodule] = self.modules.mcore[coremodule]

        else:
            try: del sys.modules[name]
            except: ''' do nothing '''

        return module, result


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


    def load(self,name, verbose=False):
        '''
        Load a module based on its name. 
        Will validate it using the ModuleLoader.
        
        return (True, module)     if successful
        return (False, errorMSG)  if unsuccessful
        '''

        if not (self.mloader.modules.extra(name)):
            module, result = self.mloader.load(name, verbose)

            if (inspect.ismodule(module) and result[0]):
                
                if (self.mloader.modules.isCmd(module)):
                    for cmd in module.cmd:
                        self.mloader.modules.cmdlist[cmd] = module

                self.mloader.modules.mextra.append(module)
                return (module,result)
            else:
                try: del sys.modules['module.extra.' + name]
                except: ''' do nothing '''
                return (False,result)
        else:
            errors = [['Loading module','Error: Module with that name already loaded.']]

            return (None,(False, (0,0), errors, None, None))


    def unload(self,name):
        '''
        Unload a module based on its name. 

        return (True, msg)       if successful
        return (True, errorMSG)  if unsuccessful
        '''

        mod = self.mloader.modules.extra(name)
        if (mod):
            self.mloader.modules.mextra.remove(mod)
            try: del sys.modules['module.extra.' + name]
            except: ''' nothing ''' 
            return (True,(True, (1,1), None, None, None))
        else:
            return (None,(False, (0,0), [['Reloading module','Error: no such module.']], None, None))


    def reloadm(self,name):
        '''
        Reload a module. 
        Uses the methods unload and load.

        Returns a message of how the reload went.
        '''

        unload = self.unload(name)
        if (unload[0]):
            loaded, result = self.load(name)
            if (loaded):
                return '%s/%s tests passed. Module %s reloaded.' % (result[1][1][0],result[1][1][1], name)
            else:
                return result
        else:
            status = (0,0)
            errors = [['Loading module','Error no such module "%s".' % name]]

            return (None,(False, status, errors, None, None))
    

    def download(self,url,verbose=False):
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
            f = open('module/extra/tmp_module.py','w')
            for line in html:
                f.write(line)
            f.close()

        except:
            errors = [['Download module','error: could not write to tempfile']]
            return (None,(False, (0,0), errors, None, None))
    
        #def validateModule(self,name):
        tmpimport, result = self.mloader.validateModule('tmp_module',verbose)
        tmpmod = None
        if (inspect.ismodule(tmpimport)):
            tmpmod = tmpimport
            name = tmpmod.name
            version = tmpmod.version
            require = ", ".join(tmpmod.require)
            listen = ", ".join(tmpmod.listen)
        else:
            return None, result


        extra_info = []
        try: extra_info.append("Author: %s" % tmpmod.author)
        except: extra_info.append("Author: uknown")
        try: extra_info.append("url: %s" % tmpmod.url)
        except: extra_info.append("url: unknown")

        extra_info = ", ".join(extra_info)
       
        try:
            f = open('module/extra/%s.py' % name,'w')
            for line in html:
                f.write(line)
            f.close()
        except: 
            status = (0,0)
            errors = [['Downloading module','could not write module to module/extra/%s.py.' % name]]

            return (None,(False, status, errors, None, None))

        os.remove('module/extra/tmp_module.py')

        #self.load(name)
        return tmpmod, result
        

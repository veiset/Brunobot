__author__  = 'Vegard Veiset'
__email__   = 'veiset@gmail.com'
__license__ = 'GPL'

import sys
import inspect
import urllib2
import os 
import presist
import module.test.moduletest as moduletest

def emptyResult():
    result = {'valid'      : False,
              'successful' : 0,
              'tests'      : 0,
              'errors'     : None,
              'failures'   : None,
              'url'        : None}

    return result

class DynamicLoad():
    '''
    Dynamic loader.

    Takes user model name as userinput, and uses the 
    ModuleLoader to load, reload, unload, and validate
    that the model is in fact a brunobot plugin. 

    Validates a module to check if it contains all the
    information required for it to be a brunobot plugin.
    It also check if the module to be loaded has a main
    method to be run when the corresponding action is 
    detected by the parser.

    This module is to load module/extra plugins for the
    brunobot. 
    '''

    def __init__(self, modules):
        '''
        Require the moudle manager and use 
        the modules from it to validate the new
        modules to load.
        '''

        self.modules = modules
        self.require_modules = modules.mcore.keys() # modules.mcore
        self.cfg = modules.mcore['cfg'] 

    def validateModule(self,name,verbose=False):
        '''
        Validating that the specified module (name)
        can be loaded and used as a Brunobot plugin.

        Checking that source file of the plugin 
        contains all the required fields and the 
        method that is to be run when called (main).
        '''

        result = emptyResult()
        module = None
        try: 
            module = __import__("module.extra." + name)
            module = sys.modules["module.extra." + name]
        except Exception as error: 
            result['errors'] = [['Loading module',('%s error [%s]' % (name,str(error)))]]
            return (None, result)

        try:
            reload(sys.modules['module.extra.%s' + name])
        except:
            ''' Do nothing '''

        unittest = moduletest.validateModule(module,verbose) 

        if unittest['valid']:
            return module, unittest
        else:
            return None, unittest
    


    def load(self,name, verbose=False):
        '''
        Load a module based on its name. 
        Will validate it using the ModuleLoader.
        
        Tries to validate the module based the name. 
        If the module is a valid module it will be injected
        with the required core modules asked for by the 
        module.

        return (Module, unittest)   if successful
        return (None,   unittest)   if unsuccessful
        '''

        result = emptyResult()

        if  self.modules.extra(name):
            result['errors'] == [['Load module','module with name "%s" already loaded.' % name]]
            return None, result
    
        
        module, result = self.validateModule(name,verbose)
        # injecting depcendencies
        if (inspect.ismodule(module)) and result['valid']:
 
            if 'cmd' in module.listen:
                for cmd in module.cmd:
                    self.modules.cmdlist[cmd] = module

            for coremodule in module.require:
                if coremodule is 'presist':
                    vars(module)['presist'] = presist.Presist(module,module.presist)
                    module.presist.load()
                else:
                    vars(module)[coremodule] = self.modules.mcore[coremodule]

            self.modules.mextra.append(module)
            self.cfg.set('modules','%s' % module.name)
            print ' .. extra module loaded: %s %s' % (module.name, module.version)

            return (module,result)
        else:
            try:
                del sys.modules['module.extra.' + name]
            except: 
                ''' do nothing '''
            return None, result

    def unload(self,name):
        '''
        Unload a module based on its name. 

        return (True, msg)       if successful
        return (True, errorMSG)  if unsuccessful
        '''

        mod = self.modules.extra(name)
        if (mod):
            self.cfg.rem('modules','%s' % mod.name)
            try: 
                del sys.modules['module.extra.' + name]
            except: 
                return (False, 'Could not unimport "module.extra.%s" module from python runtime.' % name)
            self.modules.mextra.remove(mod)
            print " .. extra module unloaded: %s" % name
            return (True, 'Module "%s" unloaded.' % name)
        
        else:
            return (False, 'Could not find module %s.' % name)


    def reloadm(self,name):
        '''
        Reload a module. 
        Uses the methods unload and load.

        Returns a message of how the reload went.
        '''

        unload = self.unload(name)
        if (unload[0]):
            module, result = self.load(name)
            if inspect.ismodule(module) and result['valid']:
                return module, result
            else:
                return None, result
        else:
            result = emptyResult()
            result['errors'] = [[unload[1]]]

            return None, result 

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
        except: 
            result = emptyResult()
            result['errors'] =  [['Download module','error: could not read file from URL.']]
            return None, result

        try:
            f = open('module/extra/tmp_module.py','w')
            for line in html:
                f.write(line)
            f.close()
        except:
            result = emptyResult()
            result['errors'] =  [['Download module','error: could not write to tempfile']]
            return None, result

        #def validateModule(self,name):
        module, result = self.validateModule('tmp_module',verbose)
        
        if inspect.ismodule(module) and result['valid']:
            try:
                f = open('module/extra/%s.py' % module.name,'w')
                for line in html:
                    f.write(line)
                f.close()
            except: 
                result = emptyResult()
                result['errors'] = [['Download module','error: could not write module to module/extra/%s.py.' % name]]
                return None, result

        else:
            try: 
                del sys.modules['module.extra.tmp_module']
            except:
                print ' ++ Could not clean up tmp_module import'
            return None, result

        print ' .. Module "%s" downloaded from %s' % (module.name, url)
        os.remove('module/extra/tmp_module.py')


        return module, result
        

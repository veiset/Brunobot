__author__  = 'Vegard Veiset'
__email__   = 'veiset@gmail.com'
__license__ = 'GPL'

import os
import sys

        
class CoreCMD():
    '''
    Core commands of the Brunobot.
    
    TODO: Make each command a module with
    documentation and usage.
    '''

    def __init__(self, m):
        sys.path.append('module/core/cmd')
        self.modules = m
        self.communication = m.mcore['communication']
        #self.cmd = ['load','unload','reload','mod','download','help']
        self.auth = m.mcore['auth']
        import cmd_mod
        import cmd_help
        import cmd_load
        import cmd_unload
        import cmd_reload
        import cmd_download
        import cmd_listmod
        import cmd_list
        import cmd_add
        self.cmd = {'mod'      : cmd_mod, 
                    'help'     : cmd_help,
                    'load'     : cmd_load,
                    'reload'   : cmd_reload,
                    'download' : cmd_download,
                    'listmod'  : cmd_listmod,
                    'list'     : cmd_list,
                    'add'      : cmd_add}
                
    def cmd_join(self,argv):
        self.modules.mcore['connection'].irc.send('JOIN %s\r\n' % argv[0])

    def cmd_part(self,argv):
        self.modules.mcore['connection'].irc.send('PART %s\r\n' % argv[0])



    def parse_cmd(self,data):
        '''
        Parsing the command to check if it is a part
        of the core commands. Returns true if, false
        otherwise.
        '''
        cmd = data['cmd']
        if cmd in self.cmd:
            try:
                self.cmd[cmd].main(self.modules, data)
            except:
                print '!!!! Core MODULE FAILED!!!!!!!!!!!!!'

            return True

        return False

        
 

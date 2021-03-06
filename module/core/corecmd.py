__author__  = 'Vegard Veiset'
__email__   = 'veiset@gmail.com'
__license__ = 'GPL'

import os
import sys 
import traceback
import inspect

from module.core.output import out
        
class CoreCMD():
    '''
    Core commands of the Brunobot.
    
    TODO: Make each command a module with
    documentation and usage.
    '''

    def __init__(self, m):
        self.modules = m
        self.communication = m.mcore['communication']
        self.auth = m.mcore['auth']
        self.cfg  = m.mcore['cfg']
        self.cmd = {}
        self.load_cmds()

    def load_cmds(self):
        ''' 
        Method for loading core commands from
        the module/core/cmd/ directory.
        '''
        cmdlist = []
        for m in os.listdir('module/core/cmd'):
            if m[-3:] == '.py' and not m == '__init__.py':
                cmdlist.append(m[:-3])

        for module in self.cmd.keys():
            try:
                del sys.modules["module.core.cmd." + module]
            except:
                ''' Nothing serious '''

        self.cmd = {}
        for mod in cmdlist:
            if not mod == '__init__':
                try:
                    module = __import__("module.core.cmd." + mod)
                    module = sys.modules["module.core.cmd." + mod]
                    reload(module)
                    for cmd_listen in module.cmd:
                        self.cmd[cmd_listen] = module
                except Exception as error:
                    #print '-'*60
                    #traceback.print_exc(file=sys.stdout)
                    #print '-'*60
                    out.error("Module %s failed to run." % mod)
                    out.verbose(error)


    def parse_cmd(self,data):
        '''
        Parsing the command to check if it is a part
        of the core commands. Returns true if, false
        otherwise.
        '''
        cmd = data['cmd']
        if cmd == 'cmd' and data['argv']:
            try:
                info_cmd = self.cmd[data['argv'][0]]
                used     = ", ".join(info_cmd.cmd) 
                info     = "[%s]    usage: %s" % (used, info_cmd.usage)
                descr    = "%sdescription: %s" % (" "*len(used), info_cmd.description)

                self.communication.say(data['channel'],"%s" % info)
                self.communication.say(data['channel'],"%s" % descr)
            except:
                self.communication.say(data['channel'],"Could not find info for %s" % data['argv'][0])

            return True
        elif cmd == 'reloadcmd':
            self.load_cmds()
            self.communication.say(data['channel'], '%d core commands modules reloaded.' % len(self.cmd))
            self.cfg.load()
            out.info("Reloaded core commands and config file.")
            return True

        elif cmd == 'listcmd':
            listofcmd = ", ".join(self.cmd.keys())
            self.communication.say(data['channel'],
                    'Found %d core commands: %s. (+ reloadcmd, cmd, listcmd)' % (len(self.cmd), listofcmd))

        elif cmd in self.cmd:
            try:
                self.cmd[cmd].main(self.modules, data)
            except Exception as error:
                out.error('Module [%s] in corecmd failed.' % cmd)
                out.verbose(error)
                #print '-'*60
                #traceback.print_exc(file=sys.stdout)
                #print '-'*60
            return True

        return False

        
 

        
class CoreCMD():
    '''
    Core commands of the Brunobot.
    '''

    def __init__(self, m):
        self.modules = m
        self.communication = m.mcore['communication']
        #self.commands = {'mod'}

    def cmd_mod(self,channel,argv):
        '''
        Command to display information about loaded modules.
        '''

        if not argv:
            core = self.modules.mcore.keys()
            core = ", ".join(core)
            extra = ""

            for mod in self.modules.mextra:
                extra += "%s %s, " % (mod.name, mod.version)
        
            if (len(extra)>1): 
                extra = extra[:-2]

            self.communication.say(channel,"Modules loaded: CORE[%s] EXTRA[%s]" % (core,extra))
        else:
            core = self.modules.core(argv[0])

            if (core):
                self.communication.say(channel,"Module %s is a part of the CORE modules." % argv[0])
            else:
                extra = self.modules.extra(argv[0])

                if (extra):
                    extra_info = []
                    try: extra_info.append("Author: " + tmpmod.author)
                    except: extra_info.append("Author: uknown")
                    try: extra_info.append("url: " + tmpmod.url)
                    except: extra_info.append("url: unknown")

                    self.communication.say(channel, 
                            "Module (extra): %s %s REQUIRE[%s] LISTEN[%s] %s" % \
                                    (extra.name,
                                     extra.version,
                                     ", ".join(extra.require),
                                     ", ".join(extra.listen),
                                     ", ".join(extra_info)))

                
    def cmd_load(self,channel,argv):
        msg = self.modules.dynamicLoader.load(argv[0])
        self.communication.say(channel,msg[1])
         
    def cmd_unload(self,channel,argv):
        msg = self.modules.dynamicLoader.unload(data['argv'][0])
        self.communication.say(channel,msg[1])

    def cmd_reload(self,channel,argv):
        msg = self.modules.dynamicLoader.reloadm(data['argv'][0])
        self.communication.say(channel,msg)

    def cmd_download(self,channel,argv):
        msg = self.modules.dynamicLoader.download(data['argv'][0])
        self.communication.say(channel,msg)

    
    def parse_cmd(self,channel,cmd,argv):
        '''
        Parsing the command to check if it is a part
        of the core commands. Returns true if, false
        otherwise.
        '''

        if (cmd == 'mod'):
            self.cmd_mod(channel,argv)
            return True

        if argv:
            if cmd == 'load':
                self.cmd_load(channel,argv)
                return True
            elif cmd == 'unload':
                self.cmd_unload(channel,argv)
                return True
            elif cmd == 'reload':
                self.cmd_reload(channel,argv)
                return True
            elif cmd == 'download':
                self.cmd_download(channel,argv)
                return True

        return False

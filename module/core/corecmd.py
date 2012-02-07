        
class CoreCMD():
    '''
    Core commands of the Brunobot.
    '''

    def __init__(self, m):
        self.modules = m
        self.communication = m.mcore['communication']
        self.cmd = ['load','unload','reload','mod','download','help']
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
                    if len(argv) == 1:
                        extra_info = []
                        try: extra_info.append("author: %s" % extra.author)
                        except: extra_info.append("Author: uknown")
                        try: extra_info.append("url: %s" % extra.url)
                        except: extra_info.append("url: unknown")

                        self.communication.say(channel, 
                                "Module (extra): %s %s REQUIRE[%s] LISTEN[%s] %s" % \
                                        (extra.name,
                                         extra.version,
                                         ", ".join(extra.require),
                                         ", ".join(extra.listen),
                                         ", ".join(extra_info)))

                    elif argv[1] == 'description' or argv[1] == 'info':
                        self.communication.say(channel,
                                "%s %s description: %s" % \
                                        (extra.name,
                                         extra.version,
                                         extra.description))
                    
                    elif argv[1] == 'usage' or argv[1] == 'use':
                        self.communication.say(channel,
                                "%s %s usage: %s" % \
                                        (extra.name,
                                         extra.version,
                                         extra.usage))

    def cmd_help(self, channel, argv):
        extra = self.modules.extra(argv[0])

        if (extra):
            
            try:
                author = "(author: %s)" % extra.author
            except:
                author = "(author: unknown)"

            self.communication.say(channel,"[%s %s %s]: " % (extra.name, extra.version, author))
            self.communication.say(channel," Description: %s" % extra.description)
            self.communication.say(channel," Usage:       %s" % extra.usage)
            if (self.modules.isCmd(extra)):
                self.communication.say(channel, " Listens to:  %s." % (", ".join(extra.cmd)))

                
    def cmd_load(self,channel,argv):
        msg = self.modules.dynamicLoader.load(argv[0])
        self.communication.say(channel,msg[1])
         
    def cmd_unload(self,channel,argv):
        msg = self.modules.dynamicLoader.unload(argv[0])
        self.communication.say(channel,msg[1])

    def cmd_reload(self,channel,argv):
        msg = self.modules.dynamicLoader.reloadm(argv[0])
        self.communication.say(channel,msg)

    def cmd_download(self,channel,argv):
        msg = self.modules.dynamicLoader.download(argv[0])
        self.communication.say(channel,msg)

    def cmd_join(self,argv):
        self.modules.mcore['connection'].irc.send('JOIN %s\r\n' % argv[0])

    def cmd_part(self,argv):
        self.modules.mcore['connection'].irc.send('PART %s\r\n' % argv[0])

    
    def parse_cmd(self,channel,cmd,argv):
        '''
        Parsing the command to check if it is a part
        of the core commands. Returns true if, false
        otherwise.
        '''

        if (cmd == 'mod'):
            self.cmd_mod(channel,argv)
            return True
        elif (cmd == 'join'):
            self.cmd_join(argv)
            return True

        elif (cmd == 'part'):
            self.cmd_part(argv)
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
            elif cmd == 'help':
                self.cmd_help(channel,argv)
                return True

        return False

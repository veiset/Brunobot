__author__  = 'Vegard Veiset'
__email__   = 'veiset@gmail.com'
__license__ = 'GPL'

import os

        
class CoreCMD():
    '''
    Core commands of the Brunobot.
    
    TODO: Make each command a module with
    documentation and usage.
    '''

    def __init__(self, m):
        self.modules = m
        self.communication = m.mcore['communication']
        self.cmd = ['load','unload','reload','mod','download','help']
        self.auth = m.mcore['auth']
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

    
    def cmd_listmod(self, channel):
        extra = ""
        unloaded = []
        loaded = []
        
        for mod in self.modules.mextra:
            extra += "%s %s, " % (mod.name, mod.version)
            loaded.append(mod.name)
        
        if (len(extra)>1): 
            extra = extra[:-2]
            self.communication.say(channel,'Loaded: %s' % extra)
        else:
            self.communication.say(channel,'No modules loaded.')

        for m in os.listdir('module/extra'):
            if m[-3:] == '.py':
                unloaded.append(m[:-3])
        
        unloaded = list(set(unloaded).difference(set(loaded)))

        if len(unloaded)>0:
            self.communication.say(channel,'Unloaded: %s' % ", ".join(unloaded))
       

    def cmd_list(self,channel,argv):
        if len(argv) != 1:
            self.communication.say(channel,'Usage: list <level>')
        else:
            users = []
            try: 
                users = self.auth.listLevel(int(argv[0]))
            except:
                if argv[0] == 'owner':
                    users = self.auth.listOwners()
                elif argv[0] == 'admin':
                    users = self.auth.listAdmins()
                elif argv[0] == 'user':
                    users = self.auth.listUsers()

            userlist = []
            if (len(users) > 0):
                for user in users:
                    userlist.append('%s (%s@%s)' % (user.userf(), user.identf(), user.hostf()))

                self.communication.say(channel,", ".join(userlist))
            else:
                self.communication.say(channel,"No users found for that group.")

    def cmd_add(self, channel, argv, user, ident, host):
        self.auth.isLevel(user,ident,host,1)
        if len(argv) != 4:
            self.communication.say(channel,'Usage: add level nick ident host.')
        else:
            lvl = None
            try:
                level = int(argv[0])
            except:
                if argv[0] == 'owner':
                    lvl = 1
                elif argv[0] == 'admin':
                    lvl = 2
                elif argv[0] == 'user':
                    lvl = 3
            if lvl:
                if self.auth.isLevel(user, ident, host, lvl):
                    self.auth.addUser(argv[1],argv[2],argv[3],lvl)
                    self.communication.say(channel,'User added.')
                else:
                    self.communication.say(channel,'You do not have permission to do that')
            else:
                self.communication.say(channel,'Could not determine user level')


    def parse_cmd(self,data):
        '''
        Parsing the command to check if it is a part
        of the core commands. Returns true if, false
        otherwise.
        '''
        cmd     = data['cmd']
        argv    = data['argv']
        channel = data['channel']

        user    = data['nick']
        ident   = data['ident']
        host    = data['host']

        auth = self.auth
        
        if (cmd == 'mod'):
            self.cmd_mod(channel,argv)
            return True

        if (cmd == 'listmod' or cmd == 'modlist'):
            self.cmd_listmod(channel)
        

        if argv:
            if cmd == 'load':
                if auth.isAdmin(None,ident,host):
                    self.cmd_load(channel,argv)
                return True
               
            elif cmd == 'unload':
                if auth.isAdmin(None,ident,host):
                    self.cmd_unload(channel,argv)
                return True
            elif cmd == 'reload':
                if auth.isAdmin(None,ident,host):
                    self.cmd_reload(channel,argv)
                return True
            elif cmd == 'download':
                if auth.isOwner(None,ident,host):
                    self.cmd_download(channel,argv)
                return True
            elif cmd == 'help':
                self.cmd_help(channel,argv)
                return True
            elif (cmd == 'join'):
                if auth.isOwner(None,ident,host):
                    self.cmd_join(argv)
                return True
            elif (cmd == 'part'):
                if auth.isOwner(None,ident,host):
                    self.cmd_part(argv)
                return True

            elif (cmd == 'list'):
                self.cmd_list(channel,argv)
                return True

            elif (cmd == 'add'):
                self.cmd_add(channel,argv,user,ident,host)
                return True

            elif (cmd == 'remove'):
                self.cmd_remove(channel,argv,user,ident,host)
                return True

        return False

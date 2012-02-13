__author__  = 'Vegard Veiset'
__email__   = 'veiset@gmail.com'
__license__ = 'GPL'

import threading
import regex
import re
import time
import config as cfg
import thread

class Parser():
    '''
    The core parser of the brunobot. 

    '''

    def __init__(self, modules):
        '''
        Getting the modules that are needed by the parser
        from the module manager.
        '''

        self.communication = modules.mcore['communication']
        self.recentdata = modules.mcore['recentdata']
        self.modules = modules
        breader = BufferReader(self)
        breader.start()


    def parse(self, line):
        '''
        Parse a line from the buffer, and decide what type
        of action it represents. 
        '''

        print ":::: parse->",line
        privmatch = re.match(regex.MSG, line)

        if privmatch != None:
            if (privmatch.group(5)[0] == cfg.command_prefix \
                    and len(privmatch.group(5)) > 2):
                self.parsecmd(privmatch.group(1), \
                        privmatch.group(2), \
                        privmatch.group(3), \
                        privmatch.group(4), \
                        unicode(privmatch.group(5)[1:],'utf-8'))
            else:
                self.parsepriv(privmatch.group(1), \
                        privmatch.group(2), \
                        privmatch.group(3), \
                        privmatch.group(4), \
                        unicode(privmatch.group(5),'utf-8'))


    def parsecmd(self, nick, ident, host, channel, cmd):
        '''
        Parse a command sent to the bot and decide what to do
        
        Keyword arguments:
        nick    -- nick of sender
        ident   -- ident of sender
        host    -- host of sender
        channel -- channel the message was sent to
        cmd     -- command that was sent
        '''

        command = cmd.split()
        data = {'nick'    :nick,
                'ident'   :ident,
                'host'    :host,
                'channel' :channel,
                'cmd'     :command[0]}
        try: data['argv'] = command[1:]
        except: data['argv'] = None

        coreCmd = self.modules.mcore['corecmd'].parse_cmd(data)

        if not coreCmd:
            cmdModules = self.modules.listening('cmd')
            
            try:
                module = self.modules.cmdlist[data['cmd']]
                try: thread.start_new_thread(module.main, (data, ) )
                except: 
                    try:
                        self.communication(channel,"!!!! module '%s %s' failed." % (module.name,module.version))
                    except:
                        print "!!!! module '%s %s' failed." % (module.name,module.version)

                if self.modules.requires(module,'presist'):
                    module.presist.save()

            except:
                print "!!!! could not find module that listens to %s." % data['cmd']



    def parsepriv(self, nick, ident, host, channel, message):
        '''
        Parse a message sent to the bot and decide what to do
        
        Keyword arguments:
        nick    -- nick of sender
        ident   -- ident of sender
        host    -- host of sender        channel -- channel the message was sent to
        message -- message that was sent
        '''


        privModules = self.modules.listening('privmsg')
        data = {'nick'    :nick,
                'ident'   :ident,
                'host'    :host, 
                'channel' :channel, 
                'msg'     :message}

        # TODO: each should be in a new thread
        for module in privModules:
            try: thread.start_new_thread(module.main, (data, ) )
            except: 
                try:
                    self.communication(channel,"!! module '%s %s' failed." % (module.name,module.version))
                except:
                    print "!! module '%s %s' failed." % (module.name,module.version)
        
            if self.modules.requires(module,'presist'):
                print 'Module presist!'
                module.presist.save()

        self.recentdata.store(nick,ident,host,channel,message)
  

class BufferReader(threading.Thread):
    '''
    BufferReader.
    '''

    def __init__(self, parser):
        self.parser = parser
        self.buffr = self.parser.communication.connection.ircbuffer
        threading.Thread.__init__(self)

    def run(self):
        
        while True:
            while len(self.buffr)>0:
                line = self.buffr.pop()
                self.parser.parse(line)

                print ":::: buffer->", self.buffr

            time.sleep(0.1)
             


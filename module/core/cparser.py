'''
Parser

'''

import threading
import regex
import re
import time
import config as cfg
import thread
class Parser():

    def __init__(self, modules):
        self.communication = modules.mcore['communication']
        self.recentdata = modules.mcore['recentdata']
        self.modules = modules
        breader = BufferReader(self)
        breader.start()


    def parse(self, line):
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
        command = cmd.split()
        data = {'nick'    :nick,
                'ident'   :ident,
                'host'    :host,
                'channel' :channel,
                'cmd'     :command[0]}
        try: data['argv'] = command[1:]
        except: data['argv'] = None

        ''' CORE CMD START '''
        if (data['cmd'] == 'mod'):
            core = self.modules.mcore.keys()
            core = ", ".join(core)
            extra = ""
            for mod in self.modules.mextra:
                extra += "%s %s, " % (mod.name, mod.version)
            
            if (len(extra)>1): extra = extra[:-2]

            self.communication.say(channel,"Modules loaded: CORE[%s] EXTRA[%s]" % (core,extra))
        
        if data['argv']:
            if (data['cmd'] == 'load'):
                msg = self.modules.dynamicLoader.load(data['argv'][0])
                self.communication.say(channel,msg[1])
            elif (data['cmd'] == 'unload'):
                msg = self.modules.dynamicLoader.unload(data['argv'][0])
                print msg
                self.communication.say(channel,msg[1])
            elif (data['cmd'] == 'reload'):
                msg = self.modules.dynamicLoader.reloadm(data['argv'][0])
                self.communication.say(channel,msg)
            elif (data['cmd'] == 'download'):
                msg = self.modules.dynamicLoader.download(data['argv'][0])
                self.communication.say(channel,msg)

        ''' CORE CMD END '''

        cmdModules = self.modules.listening('cmd')

        for module in cmdModules:
            try: thread.start_new_thread(module.main, (data, ) )
            except: print "!!!! module '%s %s' failed." % (module.name,module.version)



    def parsepriv(self, nick, ident, host, channel, message):
        privModules = self.modules.listening('privmsg')
        data = {'nick'    :nick,
                'ident'   :ident,
                'host'    :host, 
                'channel' :channel, 
                'msg'     :message}

        # TODO: each should be in a new thread
        for module in privModules:
            try: thread.start_new_thread(module.main, (data, ) )
            except: print "!!!! module '%s %s' failed." % (module.name,module.version)

        self.recentdata.store(nick,ident,host,channel,message)
        '''
        Parse a message sent to the bot and decide what to do
        
        Keyword arguments:
        nick    -- nick of sender
        ident   -- ident of sender
        host    -- host of sender
        channel -- channel the message was sent to
        message -- message that was sent
        '''
        #print 'nick    =',nick
        #print 'ident   =',ident
        #print 'host    =',host
        #print 'channel =',channel
        #print 'message =',message
        #print 'message is of length', len(message)


class BufferReader(threading.Thread):

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
             


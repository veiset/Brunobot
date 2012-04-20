__author__  = 'Vegard Veiset'
__email__   = 'veiset@gmail.com'
__license__ = 'GPL'

import threading
import regex
import re
import time

from module.core.output import out

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
        self.cfg = modules.mcore['cfg']
        self.modules = modules
        self.breader = BufferReader(self)
        self.breader.start()
        self.threadmanager = modules.mcore['threadmanager']
        self.threadmanager.start()


    def parse(self, line):
        '''
        Parse a line from the buffer, and decide what type
        of action it represents. 
        '''
        
        out.verbose("%s" % line)
        #print ":::: parse->",line
        privmatch = re.match(regex.MSG, line)

        if privmatch != None:
            text = privmatch.group(5)
            if text is not unicode:
                try:
                    text = text.encode('utf-8', 'ignore')
                except:
                    pass

            if (privmatch.group(5)[0] == self.cfg.get('module','prefix') \
                    and len(privmatch.group(5)) > 2):
                self.parsecmd(privmatch.group(1), \
                        privmatch.group(2), \
                        privmatch.group(3), \
                        privmatch.group(4), \
                        text[1:])
            else:
                self.parsepriv(privmatch.group(1), \
                        privmatch.group(2), \
                        privmatch.group(3), \
                        privmatch.group(4), \
                        text)


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
        data = {'type'    :'cmd',
                'nick'    :nick,
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
                out.info("running: %s" % module)
                if module:
                    try: 
                        self.threadmanager.runModule(module, data)
                        #thread.start_new_thread(module.main, (data, ) )
                    except Exception as error:
                        out.verbose(error)
                        out.error("Module '%s %s' failed to run." % (module.name, module.version))

                    if self.modules.requires(module,'presist'):
                        module.presist.save()

            except:
                out.warn("could not find module that listens to %s." % data['cmd'])



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
        data = {'type'    :'privmsg',
                'nick'    :nick,
                'ident'   :ident,
                'host'    :host, 
                'channel' :channel, 
                'msg'     :message}

        for module in privModules:
            try: 
                self.threadmanager.runModule(module, data)
                #thread.start_new_thread(module.main, (data, ) )
            except: 
                out.error("Module '%s %s' failed to run correctly." % (module.name,module.version))
        
            if self.modules.requires(module,'presist'):
                module.presist.save()

        self.recentdata.store(nick,ident,host,channel,message)
  

class BufferReader(threading.Thread):
    '''
    BufferReader.
    '''
    running = True

    def __init__(self, parser):
        self.parser = parser
        self.buffr = self.parser.communication.connection.ircbuffer
        threading.Thread.__init__(self)

    def run(self):
        
        while self.running:

            while len(self.buffr)>0:
                line = self.buffr.pop()
                self.parser.parse(line)

            time.sleep(0.1)
             
        out.info("Core Parser cparser.BufferReader().run(self) terminated.")


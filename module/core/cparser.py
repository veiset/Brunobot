'''
Parser

'''

import threading
import regex
import re
import time
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
            self.parsepriv(privmatch.group(1), \
                    privmatch.group(2), \
                    privmatch.group(3), \
                    privmatch.group(4), \
                    unicode(privmatch.group(5),'utf-8'))


    def parsepriv(self, nick, ident, host, channel, message):
        privModules = self.modules.listening('privmsg')
        data = [nick, ident, host, channel, message]
        for module in privModules:
            try: module.main(data)
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
        print 'nick    =',nick
        print 'ident   =',ident
        print 'host    =',host
        print 'channel =',channel
        print 'message =',message
        print 'message is of length', len(message)


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

            time.sleep(0.5)
             


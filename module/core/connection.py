# This Python file uses the following encoding: utf-8
'''
brunobot v5

'''
__author__  = 'Andreas Halle, Vegard Veiset'
__email__   = 'veiset@gmail.com'
__license__ = 'GPL'

import re
import socket
import string
import threading
import time
import regex

from module.core.output import out

class Connection():
    '''
    Represents a connection on an IRC network.
    '''
    
    
    def __init__(self, nick, ident, name, server, port, channels, ipaddr=None):
        '''
        Construct a connection ready to connect to an IRC server.
        
        Keyword arguments:
        nick     -- the bot's nickname
        ident    -- the bot's ident
        name     -- the bot's real name
        server   -- irc server to connect to
        port     -- irc server port
        channels -- a list of channels to join on connect
        ipaddr   -- ipaddress to bind a host against (vhost)

        '''
        self.nick = nick
        self.ident = ident
        self.name = name
        self.server = server
        self.port = port
        self.channels = channels
        self.ipaddr = ipaddr 

        self.irc = None

        # Incomming message buffer
        self.ircbuffer = []
       
        self.connected = False 
    
    def quit(self,message=None):
        self.connected = False
        try:
            self.irc.send(u'QUIT \n')
        except:
            out.warning('Could not communicate with IRC socket')
        try:
            self.irc.close()
        except:
            out.warning('Could not close the IRC socket. (Might already be closed)')

   
    def connect(self):
        
        self.irc = socket.socket()

        # Trying to bind vhost
        if self.ipaddr:
            try: 
                self.irc.bind((self.ipaddr, self.port))
                out.info("bound IP-address: %s " % self.ipaddr)
            except: 
                out.warn("could not bind IP-address: %s " % self.ipaddr)


        self.irc.connect((self.server, self.port))
        self.irc.send(u'NICK %s\n' % (self.nick))
        self.irc.send(u'USER %s %s bla :%s\n' % (self.ident, self.server, self.name))

        for channel in self.channels:
            self.irc.send(u'JOIN #%s\n' % channel)

        out.info("Connected to %s" % self.server)
        out.newline()

        self.connected = True
        stayawake = self.StayAwake(self)
        stayawake.start()
        
    
   
    
    class StayAwake(threading.Thread):
        '''
        Make sure that the bot stays alive by answering to PINGs
        as well as parsing messages sent by the IRC server.
        '''
        def __init__(self, parent):
            '''
            Construct a thread to run in the background to keep the bot alive.
            
            Keyword arguments:
            parent -- an instantiated Connection object
            '''
            threading.Thread.__init__(self)
            self.parent = parent
            self.ircbuffer = parent.ircbuffer 
        
        
        def run(self):
            '''
            run() -> None
            
            Run a loop forever in the background and
            replies to PING requests from the IRC server.
            '''
            buffr = ''

            while self.parent.connected:
                buffr += self.parent.irc.recv(1024)
                temp = string.split(buffr, '\n')
                buffr = temp.pop()
               
                for line in temp:
                    line = string.rstrip(line)
                    
                    pingmatch = re.match('^PING :(.*)$', line)
                    
                    # Answer to PINGs from the IRC server.
                    if pingmatch != None:
                        self.parent.irc.send('PONG %s\r\n' % \
                                             (pingmatch.group(1)))

                    self.ircbuffer.append(line)


            out.info("Connection connection.StayAwake().run(self) terminated.")

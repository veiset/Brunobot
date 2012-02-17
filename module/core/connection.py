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
import config as cfg


class Connection():
    '''
    Represents a connection on an IRC network.
    '''
    
    
    def __init__(self, nick, ident, name):
        '''
        Construct a connection ready to connect to an IRC server.
        
        Keyword arguments:
        nick  -- the bot's nickname
        ident -- the bot's ident
        name  -- the bot's real name
        '''
        self.nick = nick
        self.ident = ident
        self.name = name
        
        self.irc = None
        self.server = ""
        self.port = 0

        # Incomming message buffer
        self.ircbuffer = []
        
        self.connected = False
        
    
    
    def connect(self, server, port):
        self.server = server
        self.port = port
        
        self.irc = socket.socket()
        self.irc.connect((server, port))
        self.irc.send(u'NICK %s\n' % (self.nick))
        self.irc.send(u'USER %s %s bla :%s\n' % (self.ident, server, self.name))
        self.irc.send(u'JOIN %s\n' % cfg.channel)
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
            
            while True:
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
                    else:
                        self.ircbuffer.append(line)

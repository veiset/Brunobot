""" Communicaton """
__author__  = 'Vegard Veiset'
__email__   = 'veiset@gmail.com'
__license__ = 'GPL'

import time
from module.core.output import out

class Communication():

    def __init__(self, connection):
        self.connection = connection

    def say(self, target, message):
        '''
        say() -> None
        
        Send a message to a target on the connected IRC server.
        
        Keyword arguments:
        target  -- recipient of given message
        message -- message to send
        '''
        if type(message) is not unicode:
            message = unicode(message,'utf-8')
            
        '''
        From RFC 1459:
        
        IRC messages are always lines of characters terminated with a CR-LF
        (Carriage Return - Line Feed) pair, and these messages shall not
        exceed 512 characters in length, counting all characters including
        the trailing CR-LF. Thus, there are 510 characters maximum allowed
        for the command and its parameters.
        '''
            
        '''
        :nick!ident@host PRIVMSG chan :text
        
        TODO: 80 is just a temporary size. Should be the length of the
        bot's host. TODO: Check length before unicode.
        '''
        noise = 16 + len(self.connection.nick) + len(target) + len(self.connection.ident) + 30
        
        lines = message.split('\n')
        for line in lines:
            # PRIVMSG chan :text\r\n
            cmdlen = noise + len(line)
            if cmdlen <= 512:
                self.connection.irc.send('PRIVMSG %s :%s\n' % (target, line))
            else:
                splits = Connection.lensplit(line, 512 - noise)
                for a in splits: self.say(target, a)
   

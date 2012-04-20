__author__  = 'Vegard Veiset'
__email__   = 'veiset@gmail.com'
__license__ = 'GPL'

import time
class UserData():

    def __init__(self,nick,ident,host):
        self.nick = nick
        self.ident = ident
        self.host = host
        self.recent = []
        self.log = {}

    def msg(self,channel,message):
        # should limit the size of recent and log to avoid to use
        # too much memory when the bot is running for a long duration
        t = time.time()
        self.recent.append({'time' : t, 'channel': channel, 'msg': message})

        if not channel in self.log:
            self.log[channel] = []
        self.log[channel].append([t, message])

    def lastMsg(self):
        return self.recent[-1]

    def mostRecent(self):
        return self.recent[-2]
   
    def channel(self, channel):
        if channel in self.log:
            return self.log[channel]
        return None

class Data(): 
   

    def __init__(self):
        self.users = {}
        self.userhost = lambda a,b,c: a+"!"+b+"@"+c

    def store(self,nick,ident,host,channel,message):

        if (self.userhost(nick,ident,host) not in self.users):
            self.users[self.userhost(nick,ident,host)] = UserData(nick,ident,host)

        self.users[self.userhost(nick,ident,host)].msg(channel,message)

    def user(self,nick,ident,host):
        return self.users[self.userhost(nick,ident,host)]


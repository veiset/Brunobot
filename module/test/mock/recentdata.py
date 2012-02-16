'''
Interface for the Recent Data module.
'''
class UserData():

    def __init__(self, nick, ident, host):
        return (nick, ident, host)

    def msg(self, channel, message):
        return (channel, message)

    def mostRecent(self):
        return True
    
    def lastMsg(self):
        return True

class Data():

    def __init__(self):
        ''' Do nothing '''

    def store(self, nick, ident, host, channel, message):
        return (nick, ident, host, channel, message)

    def user(self, nick, ident, host):
        return (nick, ident, host)


class Users:
    
    REGULAR    = 0
    OP         = 1
    VOICE      = 2

    def __init__(self, bot):
        self.bot = bot
        self.channels = {} #{'#informatikk': [('vz','@').('andern':'+')]}
        self.users = {}
        self.bot.irc.addListener("join", self.joinEvent)
        self.bot.irc.addListener("part", self.partEvent)
        self.bot.irc.addListener("mode", self.modeEvent)
        self.bot.irc.addListener("names", self.namesEvent)

    def namesEvent(self, event):
        ''' '''
        print(event.get('users'))
        

    def joinEvent(self, event):
        ''' 
        Adds the user joining a channel to the channel list as a regular user
        
        Keyword arguments:
        event -- pyric JOIN event
        '''
        channel = event.get('channel') 
        nick, ident, host = event.get('user')

        if not self.existsChannel(channel):
            self.addChannel(channel)
 
        if not self.existsUser(nick):
            self.addUser(nick, ident, host)
        
        self.addUserToChannel(channel, nick, self.REGULAR)


    def partEvent(self, event):
        ''' 
        Removes a parting user from the channel list
        
        Keyword arguments:
        event -- pyric PART event
        '''
        channel = event.get('channel')
        nick, ident, host = event.get('user')

        if self.existsChannel(channel) and self.channelHasUser(channel, nick):
            self.removeUserFromChannel(channel, nick)


        
    def modeEvent(self, event):
        ''' '''
        channel = event.get('channel')
        nick, ident, host = event.get('user')

        modes = self.getModesFromEvent(event.get('msg'))
        for mode in modes: 
            if self.channelHasUser(channel, nick):
                self.changeMode(channel, mode)


    def changeMode(self, channel, mode):
        ''' '''
        add, mode, nick = mode
        if add:
            if not self.userHasMode(channel, nick, mode):
                self.addUserMode(channel, nick, mode)
        else:
            if self.userHasMode(channel, nick, mode):
                self.removeUserMode(channel, nick, mode)


    def user(self, channel="*"):
        ''' '''
        if channel == "*":
            return "something" 

    def getUserModes(self, channel, nick):
        if channel in self.channels:
            if nick in self.channels[channel]:
                return self.channels[channel][nick]
                
        return None

    def getModesFromEvent(self, eventMsg):
        ''' Parsing modes '''
        modes, users = eventMsg.split(' ', 1)
        users = users.split(' ')
        users.reverse()

        userModes = []

        for token in modes:
            if token == '+': add = True
            elif token == '-': add = False
            else:
                mode = self.getModeTypeFromLetter(token)
                if add: 
                    userModes.append((True, mode, users.pop()))
                if not add: 
                    userModes.append((False, mode, users.pop()))

        return userModes

    def getModeTypeFromLetter(self, letter):
        if letter == 'o': return self.OP
        if letter == 'v': return self.VOICE

    def addUserMode(self, channel, nick, mode):
        self.channels[channel][nick].append(mode)

    def removeUserMode(self, channel, nick, mode):
        self.channels[channel][nick].remove(mode)

    def userHasMode(self, channel, nick, mode):
        return mode in self.channels[channel][nick]
    
    def channelHasUser(self, channel, nick):
        return nick in self.channels[channel]

    def removeUserFromChannel(self, channel, nick):
        del self.channels[channel][nick]

    def addUserToChannel(self, channel, nick, mode):
        self.channels[channel][nick] = [mode]
    
    def addUser(self, nick, ident, host):
        self.users[nick] = (ident, host)

    def addChannel(self, channel):
        self.channels[channel] = {}
    
    def existsUser(self, nick):
        return nick in self.users

    def existsChannel(self, channel):
        return channel in self.channels


class Users:
    REGULAR    = 0
    VOICE      = 1
    HALFOP     = 2
    OP         = 3
    ADMIN      = 4
    OWNER      = 5

    def __init__(self, bot):

        self.bot = bot
        self.channels = {} # {'#informatikk': [('vz','OP').('andern':'VOICE')]}
        self.users = {}    # {'vz' : ('~vz', 'veiset.org) ...}

        self.bot.irc.addListener("join", self.joinEvent)
        self.bot.irc.addListener("part", self.partEvent)
        self.bot.irc.addListener("mode", self.modeEvent)
        self.bot.irc.addListener('353', self.namesEvent)

    def namesEvent(self, event):
        ''' '''
        channel = event.get('channel')
        names = event.get('msg')

        if not self.existsChannel(channel):
            self.addChannel(channel)

        statuslist = Users.getStatuslistFromNames(names)
        for status, nick in statuslist: 
            if not self.channelHasUser(channel, nick):
                self.addUserToChannel(channel, nick, self.REGULAR)
            
            if not self.userHasStatus(channel, nick, status):
                self.addUserStatus(channel, nick, status)
            
        

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

        modes = Users.getModesFromEvent(event.get('msg'))
        for mode in modes: 
            if self.channelHasUser(channel, nick):
                self.changeStatus(channel, mode)


    def changeStatus(self, channel, mode):
        ''' '''
        add, status, nick = mode 
        if add:
            if not self.userHasStatus(channel, nick, status):
                self.addUserStatus(channel, nick, status)
        else:
            if self.userHasStatus(channel, nick, status):
                self.removeUserStatus(channel, nick, status)


    def getUserStatus(self, channel, nick):
        if channel in self.channels:
            if nick in self.channels[channel]:
                return self.channels[channel][nick]
                
        return None


    def addUserStatus(self, channel, nick, status):
        self.channels[channel][nick].append(status)

    def removeUserStatus(self, channel, nick, status):
        self.channels[channel][nick].remove(status)

    def userHasStatus(self, channel, nick, status):
        return status in self.channels[channel][nick]
    
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

    def getUserlistFromChannel(self, channel):
        return self.channels[channel]

    ### Static methods

    def getStatuslistFromNames(eventMsg):
        ''' 
        Parsing IRC 353 event

        Keyword arguments:
        eventMsg -- pyric 353 event message

        return (Users.STATUS, nick)
        '''
        users = []

        for nick in Users.getUsersFrom353EventMsg(eventMsg):
            if Users.hasStatusSymbol(nick):
                status = Users.getStatusSymbolFromNick(nick)
                nick = Users.stripStatusSymbol(nick)
                users.append((status, nick))
            else:
                users.append((Users.REGULAR, nick))

        return users


    def getModesFromEvent(eventMsg):
        '''
        Parsing modes from MODE pyric events

        Keyword arguments:
        eventMsg -- pyric MODE event message (e.g: '+o vz')

        return (isGiving, Users.STATUS, nick)
        '''

        modes, users = eventMsg.split(' ', 1)
        users = users.split(' ')
        users.reverse()

        userStatus = []

        for token in modes:
            if token == '+': add = True
            elif token == '-': add = False
            else:
                status = Users.getStatusTypeFromLetter(token)
                if add: 
                    userStatus.append((True, status, users.pop()))
                if not add: 
                    userStatus.append((False, status, users.pop()))

        return userStatus


    def stripStatusSymbol(user):
        return user[1:]

    def getStatusSymbolFromNick(nick):
        symbol = nick[0]
        return Users.getStatusFromSymbol(symbol)
    
    def hasStatusSymbol(user):
        firstLetter = user[0]
        return Users.isStatusSymbol(firstLetter)

    def getUsersFrom353EventMsg(eventMsg):
        return eventMsg.split(' ')

    def isStatusSymbol(symbol):
        return symbol in '+%@&~'

    def getStatusFromSymbol(symbol):
        if symbol == '+': return Users.VOICE
        elif symbol == '%': return Users.HALFOP
        elif symbol == '@': return Users.OP
        elif symbol == '&': return Users.ADMIN
        elif symbol == '~': return Users.OWNER
        else: return Users.REGULAR

    def getStatusTypeFromLetter(letter):
        if letter == 'o': return Users.OP
        if letter == 'v': return Users.VOICE


import api.base
class Users(api.base.BrunoAPI):
    ''' 
    Brunobot API: Users

    API for getting a list of the users in a channel, and for checking
    the status (op, voice...) of a given user in a channel.

    API Methods:
    hasStatus(channel, nick, status) -> boolean
    getUserStatus(channel, nick) -> status
    getChannelList(channel) -> List of (nick, status)

    '''

    REGULAR  = 0   
    VOICE    = 1 
    HALFOP   = 2 
    OP       = 3
    OWNER    = 4
    FOUNDER  = 5

    def __init__(self, brunobot):
        super().__init__(brunobot)

        self.channels = {} # {'#informatikk': [('vz','OP').('andern':'VOICE')]}

        self.addListener("join", self.joinEvent)
        self.addListener("part", self.partEvent)
        self.addListener("mode", self.modeEvent)
        self.addListener('353', self.namesEvent)
        
        self.api.function(self.hasStatus)
        self.api.function(self.getUserStatus)
        self.api.function(self.getChannelList)
        self.api.constants(
            [
                ('REGULAR', self.REGULAR),
                ('VOICE', self.VOICE),
                ('HALFOP', self.HALFOP),
                ('OP', self.OP),
                ('OWNER', self.OWNER),
                ('FOUNDER', self.FOUNDER),
            ]
        )

    def hasStatus(self, channel, nick, status):
        '''
        Checks if a user has the given status.

        Keyword arguments:
        channel -- IRC channel name
        nick    -- IRC user nickname
        status  -- The status to check against

        Example usage:
        >>> if hasStatus('#mychan', 'someNick', OP):
        >>>     print("The user is OPed")

        return If the user on the channel has the given status
        '''
        if self.existsChannel(channel) and self.channelHasUser(channel, nick):
            return self.userHasStatus(channel, nick, status)

        return False


    def getUserStatus(self, channel, nick):
        '''
        Looks up the status of a user in the given channel.
        A user can have the following statuses: 
        REGULAR, VOICE, HALFOP, OP, OWNER, FOUNDER

        Keyword arguments:
        channel -- IRC channel name
        nick    -- IRC user nickname

        Example usage:
        >>> if VOICE in getUserStatus('#mychan', 'someNick'):
        >>>     print("The user is VOICEed")
        
        return A list of statuses the user have
        '''
        if self.existsChannel(channel):
            if self.channelHasUser(channel, nick):
                return self.channels[channel][nick]
                
        return None

    def getChannelList(self, channel):
        '''
        Returns a list of (user, status) from a channel.

        Keyword arguments:
        channel -- IRC channel name

        Example usage:
        >>> for user, status in getChannelList('#mychan'):
        >>>     print("%s has status %s", % (user, status))

        retrun A list of (user, status)
        '''
        if self.existsChannel(channel):
            return self.getUserlistFromChannel(channel)

        return None

    def namesEvent(self, event):
        ''' 
        Takes an pyric 353 event (listing of IRC names) as an input and adds
        the users to the given channel with corresponding status codes.

        Keyword arguments:
        event -- pyric 353 event
        '''
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
        Adds a joining user to the channel list as a regular user.
        
        Keyword arguments:
        event -- pyric JOIN event
        '''
        channel = event.get('channel') 
        nick, ident, host = event.get('user')

        if not self.existsChannel(channel):
            self.addChannel(channel)
 
        self.addUserToChannel(channel, nick, self.REGULAR)


    def partEvent(self, event):
        ''' 
        Removes a parting user from the channel list.
        
        Keyword arguments:
        event -- pyric PART event
        '''
        channel = event.get('channel')
        nick, ident, host = event.get('user')

        if self.existsChannel(channel) and self.channelHasUser(channel, nick):
            self.removeUserFromChannel(channel, nick)


    def modeEvent(self, event):
        '''
        Updates the status on users based on an IRC mode event (e.g: +o user).
        
        Keyword arguments:
        event -- pyric MODE event
        '''
        channel = event.get('channel')
        modes = Users.getModesFromEvent(event.get('msg'))
        for isGiving, status, nick in modes: 
            if self.channelHasUser(channel, nick):
                self.changeStatus(channel, isGiving, status, nick)


    def changeStatus(self, channel, isGiving, status, nick):
        '''
        Changes status of an already existing user.

        Keyword arguments:
        channel  -- IRC channel name
        isGiving -- Whether the status is given or taken
        status   -- Users.STATUS code (OP, HALFOP, VOICE...)
        nick     -- IRC nickname
        '''
        if isGiving: 
            if not self.userHasStatus(channel, nick, status):
                self.addUserStatus(channel, nick, status)
        elif self.userHasStatus(channel, nick, status):
            self.removeUserStatus(channel, nick, status)


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
    
    def addChannel(self, channel):
        self.channels[channel] = {}

    def existsChannel(self, channel):
        return channel in self.channels

    def getUserlistFromChannel(self, channel):
        return self.channels[channel]




    # Static methods

    def getModesFromEvent(eventMsg):
        '''
        Parsing modes from the MODE pyric event.

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


    def getStatusFromSymbol(symbol):
        '''
        Returns the status code for a given symbol

        For an indepth explanation of symobls see:
         http://wiki.gbatemp.net/wiki/IRC_Glossary
        '''

        if symbol == '+': return Users.VOICE
        elif symbol == '%': return Users.HALFOP
        elif symbol == '@': return Users.OP
        elif symbol == '&': return Users.OWNER
        elif symbol == '~': return Users.FOUNDER

        return Users.REGULAR


    def getStatusTypeFromLetter(letter):
        '''
        Returns the status code representation of a mode letter

        For a list of IRC modes see:
         http://webtoman.com/opera/panel/ircdmodes.html
        '''

        if letter == 'o': return Users.OP
        elif letter == 'h': return Users.HALFOP
        elif letter == 'v': return Users.VOICE
        elif letter == 'q': return Users.OWNER
        elif letter == 'a': return Users.FOUNDER


    def getStatusSymbolFromNick(nick):
        symbol = nick[0]
        return Users.getStatusFromSymbol(symbol)
    
    def hasStatusSymbol(user):
        firstLetter = user[0]
        return Users.isStatusSymbol(firstLetter)

    def isStatusSymbol(symbol):
        return symbol in '+%@&~'

    def stripStatusSymbol(user):
        return user[1:]

    def getUsersFrom353EventMsg(eventMsg):
        return eventMsg.split(' ')

    def getStatuslistFromNames(eventMsg):
        ''' 
        Parsing nicks and their given status from a list of names with
        status symboles (e.g: "@user1 user2 +user3 user4").

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

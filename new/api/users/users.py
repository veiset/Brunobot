class Users:
    

    def __init__(self, bot):
        self.bot = bot
        self.chans = {} #{'#informatikk': [('vz','@').('andern':'+')]}
        self.bot.irc.addListener("join", self.joinEvent)
        self.bot.irc.addListener("part", self.partEvent)
        self.bot.irc.addListener("mode", self.modeEvent)
        self.bot.irc.addListener("names", self.namesEvent)

    def namesEvent(self, event):
        ''' '''
        print(event.get('users'))
        

    def joinEvent(self, event):
        ''' Adds a user to the channel list when joining '''
        chan = event.get('channel') 

        if not chan in self.chans:
            self.chans[chan] = {}

        self.chans[chan][event.get('user')] = None

    def partEvent(self, event):
        ''' '''
        chan = event.get('channel')

        if chan in self.chans:
            del self.chans[chan][event.get('user')]
        
    def modeEvent(self, event):
        ''' '''

    def channel(self, chan):
        ''' '''

    def user(self, chan="*"):
        ''' '''
        if chan == "*":
            return "something" 


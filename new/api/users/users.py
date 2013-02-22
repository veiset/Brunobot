
class Users:
    
    def __init__(self, bot):
        self.bot = bot
        self.chans = {} #{'#informatikk': [('vz','@').('andern':'+')]}
        self.bot.irc.addListener("join", self.joinEvent)
        self.bot.irc.addListener("part", self.partEvent)
        self.bot.irc.addListener("mode", self.modeEvent)
        self.bot.irc.addListiner("names", self.namesEvent)

    def namesEvent(self, event):
        ''' '''
        print(event.get('users'))

    def joinEvent(self, event):
        ''' '''

    def partEvent(self, event):
        ''' '''
        
    def modeEvent(self, event):
        ''' '''

    def channel(self, chan):
        ''' '''

    def user(self, chan="*"):
        ''' '''
        if chan == "*":
            return "something" 

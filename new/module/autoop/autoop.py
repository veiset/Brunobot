class Module():
    ''' Resolves title of posted URLs '''

    def __init__(self, bot):
        self.bot = bot
        self.opers = {}
        self.bot.irc.addListener("join", self.aop)

    def aop(self, event):
        ''' Checks if a joining is to be given operator status '''
        user, host = event.get('user').split('!') # nick!ident@host
        if host in self.opers:
            self.bot.irc.mode(event.get('channel'), '+o %s' % user)


    def add(self, channel, host):
        ''' 
        Keyword arguments:
        channel -- IRC channel
        host    -- host name in the format of ident@host.com
        '''
        self.opers[host] = True

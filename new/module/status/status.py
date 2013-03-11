import api.base
class UserStatus(api.base.BrunoAPI):
    ''' Resolves status of a user '''

    def __init__(self, brunobot):
        super().__init__(brunobot)
        self.auth = self.bot.api.get('auth')
        self.users = self.bot.api.get('users')

        self.addListener("cmd.status", self.status)

    def status(self, event):
        nick, ident, host = event.get('user')
        channel = event.get('channel')

        authStatus = self.auth().getLevel(nick, ident, host)
        chanStatus = self.users().getUserStatus(channel, nick)

        self.bot.irc.say(
            channel, 
            "You you have auth-level: %s, and channel status: %s" % (
                authStatus, 
                chanStatus
            )
        )


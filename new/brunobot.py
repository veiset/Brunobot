from pyric import irc

import api.manager

class Brunobot():
    def __init__(self):
        self.irc= irc.Instance('vzbot', 'vz', 'vz', 'irc.homelien.no', 6667)
        self.api = api.manager.Manager(self)
        self.api.add('api.auth.auth', 'auth')
        self.api.add('api.users.users', 'users')

        self.auth = self.api.get('auth')
        self.auth().add('vz','~vz','veiset.org', self.auth().FOUNDER)

        self.module = api.manager.Manager(self)
        self.module.add('module.urltitle.urltitle', 'urltitle')
        self.module.add('module.status.status', 'status')


bot = Brunobot()
bot.irc.connect()

bot.irc.join('#brbot')

from pyric import irc

import api.manager

class Brunobot():
    def __init__(self):
        self.irc= irc.Instance('vzbot', 'vz', 'vz', 'irc.homelien.no', 6667)
        self.api = api.manager.Manager(self)


bot = Brunobot()
bot.irc.connect()

bot.irc.join('#brbot')
bot.irc.join('#informatikk')

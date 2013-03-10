from pyric import irc

import api.manager

class Brunobot():

    def __init__(self):
        self.bot = irc.Instance('vzbot', 'vz', 'vz', 'irc.homelien.no', 6667)
        
        self.api = api.manager.Manager()

bot.connect()

bot.join('#brbot')
bot.join('#informatikk')

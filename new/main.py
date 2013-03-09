from pyric import irc
bot = irc.Instance('vzbot', 'vz', 'vz', 'irc.homelien.no', 6667)

bot.connect()
bot.join('#brbot')

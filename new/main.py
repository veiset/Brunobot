from pyric import *
class Brunobot():

    def __init__(self):
        self.irc = irc.Instance('vzbotte', 'vz', 'vz', 'irc.homelien.no', 6667)

        # Initial modules
        import module.urltitle.urltitle as urltitle
        urltitle.Module(self)

        import module.autoop.autoop as autoop
        ops = autoop.Module(self)
        ops.add('#informatikk', '~vz@veiset.org')
        

    def connect(self):
        self.irc.connect()


bot = Brunobot()
bot.connect()
bot.irc.join('#informatikk')

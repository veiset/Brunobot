from pyric import irc
from pyric import events
import pyric.test.mocks as mocks

import api.manager
import ast


class Brunobot():
    def __init__(self):
        #self.irc= irc.Instance('vzbot', 'vz', 'vz', 'irc.homelien.no', 6667)
        self.nick = 'vzbotz' 

        self.irc = irc.Instance(self.nick, 'vz', 'vz', 'irc.codetalk.io', 6667)
        self.api = api.manager.Manager(self)
        self.api.add('api.auth.auth', 'auth')
        self.api.add('api.users.users', 'users')

        self.auth = self.api.get('auth')
        self.auth().add('vz','~vz','veiset.org', self.auth().FOUNDER)

        self.module = api.manager.Manager(self)
        self.module.add('module.urltitle.urltitle', 'urltitle')
        self.module.add('module.status.status', 'status')
        self.module.add('module.ppoker.planningpoker', 'ppoker')

        self.irc.addListener('266', self.joinChannels)
        self.irc.addListener('*', self.allEvents)

    def joinChannels(self, event):
        self.irc.join('#tlob')
        #raise Exception("NOP!")

    def allEvents(self, event):
        print(event.data)
        with open('lobby.log', 'a') as log:
            log.write("%s\n" % str(event.data))

    def playback(self):
        with open('lobby.log', 'r') as log:
            for line in log.readlines():
                event = events.Event((ast.literal_eval(line)))
                bot.irc.event(event)


bot = Brunobot()
bot.irc.irc = mocks.Socket()
bot.playback()
#bot.irc.connect()

#bot.irc.join('#brbot')

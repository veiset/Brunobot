import os
import ast
from pyric import events
import api.base


class Recorder(api.base.BrunoAPI):

    def __init__(self, bot):
        super().__init__(bot)

        self.authNick = {}
        self.authIdent = {}
        self.authHost = {}

        self.api.function(self.add)


    def record(self, logfile):
        print("Starting to record.")


    def playback(self, logfile):
        with open(logfile, 'r') as log:
            for event in log:
                e = events.Event(ast.literal_eval(event))
                self.bot.irc.event(e)


    def writeEvent(self, logfile, event):
        with open(logfile, 'a') as log:
            log.write('%s\n' % str(event.data))

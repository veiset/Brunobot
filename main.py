import modulemanager

import time

class Brunobot():

    def __init__(self):
        self.modules = modulemanager.ModuleManager()

        self.connection = self.modules.core('connection')
        self.communication = self.modules.core('communication')
        self.parser = self.modules.core('parser')

        self.connection.connect()

brunobot = Brunobot()


# Enabling the bot to be quitted by ^C (control-c)
while brunobot.modules.enabled:
    try:
        time.sleep(0.3)
    except KeyboardInterrupt:
        brunobot.modules.quit()

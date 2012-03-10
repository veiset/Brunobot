import modulemanager

class Brunobot():

    def __init__(self):
        self.modules = modulemanager.ModuleManager()

        self.connection = self.modules.core('connection')
        self.communication = self.modules.core('communication')
        self.parser = self.modules.core('parser')

        self.connection.connect()

brunobot = Brunobot()

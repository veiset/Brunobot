import modulemanager
import config as cfg

class Brunobot():

    def __init__(self):
        self.modules = modulemanager.ModuleManager()

        print(self.modules.coreModules())
        
        self.connection = self.modules.core('connection')
        self.communication = self.modules.core('communication')
        self.parser = self.modules.core('parser')

        self.connection.connect(cfg.server, cfg.port)

brunobot = Brunobot()

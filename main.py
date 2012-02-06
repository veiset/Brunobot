import modulemanager

class Brunobot():

    def __init__(self):
        self.modules = modulemanager.ModuleManager()

        print(self.modules.coreModules())
        
        self.connection = self.modules.core('connection')
        self.communication = self.modules.core('communication')
        self.parser = self.modules.core('parser')

        self.connection.connect('efnet.port80.se', 6667)

brunobot = Brunobot()

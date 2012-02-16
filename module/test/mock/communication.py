'''
Interface for the Communcation module.
'''
class Communication():

    def __init__(self, connection):
        ''' Nothing to see here '''
        self.connection = connection

    def say(self, target, message):
        return (target, message)

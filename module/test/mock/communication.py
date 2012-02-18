'''
Mock object of Communication module. 
Used for testing brunobot modules. This will be 
injected instead of the real module, so that
the unit test is able to run the brunbot-plugins
main method with some expectations of behaviour.
'''
class Communication():

    def __init__(self, connection):
        ''' Nothing to see here '''
        self.connection = connection

    def say(self, target, message):
        return (target, message)

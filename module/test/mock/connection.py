'''
Mock object of Connection module. 
Used for testing brunobot modules. This will be 
injected instead of the real module, so that
the unit test is able to run the brunbot-plugins
main method with some expectations of behaviour.
'''
class Connection():

    def __init__(self, nick, ident, name):
        return True

    def connect(self, server, port):
        return True


'''
Mock object of Presistence module. 
Used for testing brunobot modules. This will be 
injected instead of the real module, so that
the unit test is able to run the brunbot-plugins
main method with some expectations of behaviour.
'''
class Presist():

    def __init__(self, extra, variables):
        ''' Do nothing here '''

    def load(self):
        return True

    def save(self):
        return True

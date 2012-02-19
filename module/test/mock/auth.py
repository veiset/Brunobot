'''
Mock object of Auth module. 
Used for testing brunobot modules. This will be 
injected instead of the real module, so that
the unit test is able to run the brunbot-plugins
main method with some expectations of behaviour.
'''
class Auth():
    
    def __init__(self):
        ''' mock '''

    def resolve(self,user,ident,host):
        return None

    def addUser(self, user, ident, host, level):
        ''' mock '''

    def remUser(self, user, ident, host):
        ''' mock '''

    def isLevel(self, user, ident, host, level):
        return None

    def listLevel(self, level):
        return []

    def isOwner(self, user, ident, host):
        return True

    def isAdmin(self, user, ident, host):
        return True

    def isUser(self, user, ident, host):
        return True

    def listOwners(self):
        return []

    def listAdmins(self):
        return []

    def listUsers(self):
        return []

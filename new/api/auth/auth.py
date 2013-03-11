class AuthUser():
    def __init__(self, nick, ident, host, level):
        self.nick = nick
        self.ident = ident
        self.host = host
        self.level = level
    
    def equals(self, user):
        return (self.sameValue(self.nick, user.nick)
            and self.sameValue(self.ident, user.ident)
            and self.sameValue(self.host, user.host))

    def canAuth(self, user):
        return (self.sameValue(self.level, user.level)
            or self.level >= user.level)

    def sameValue(self, value1, value2):
        return ((value1 == Auth.WILDCARD)
             or (value2 == Auth.WILDCARD)
             or (value1 == value2))

import api.base
class Auth(api.base.BrunoAPI):

    NONE    = 0
    USER    = 1
    ADMIN   = 2
    OWNER   = 3
    FOUNDER = 4
    
    WILDCARD = "*"
    
    def __init__(self, bot):
        super().__init__(bot)

        self.authNick = {}
        self.authIdent = {}
        self.authHost = {}

        self.api.function(self.add)
        self.api.function(self.remove)
        self.api.function(self.isAuthed)
        self.api.function(self.getLevel)
        self.api.constants(
            [
                ('NONE',    self.NONE),
                ('USER',    self.USER),
                ('ADMIN',   self.ADMIN),
                ('OWNER',   self.OWNER),
                ('FOUNDER', self.FOUNDER),
                ('WILDCARD', self.WILDCARD)
            ]
        )

    def add(self, nick, ident, host, level):
        authUser = AuthUser(nick, ident, host, level)
        self.registerNick(authUser)
        self.registerIdent(authUser)
        self.registerHost(authUser)

    def remove(self, nick, ident, host):
        authUser = AuthUser(nick, ident, host, self.WILDCARD)
        self.removeNick(authUser)
        self.removeIdent(authUser)
        self.removeHost(authUser)

    def getLevel(self, nick, ident, host):
        user = AuthUser(nick, ident, host, self.WILDCARD)
        if self.hasNick(user): return self.getNick(user).level
        if self.hasIdent(user): return self.getIdent(user).level
        if self.hasHost(user): return self.getHost(user).level

        return self.NONE

    def isAuthed(self, nick, ident, host, level):
        user = AuthUser(nick, ident, host, level)

        if self.hasNick(user):
            nAuth = self.getNick(user)
            if nAuth.equals(user) and nAuth.canAuth(user):
                return True

        if self.hasIdent(user):
            iAuth = self.getIdent(user)
            if iAuth.equals(user) and iAuth.canAuth(user):
                return True

        if self.hasHost(user):
            hAuth = self.getHost(user)
            if hAuth.equals(user) and hAuth.canAuth(user):
                return True

        return False


    def removeNick(self, authUser): self.removeUser(self.authNick[authUser.nick], authUser)
    def removeIdent(self, authUser): self.removeUser(self.authIdent[authUser.ident], authUser)
    def removeHost(self, authUser): self.removeUser(self.authHost[authUser.host], authUser)

                
    def removeUser(self, users, authUser):
        if self.hasUser(users, authUser):
            user = self.getUser(users, authUser)
            users.remove(user)

    def hasNick(self, authUser): 
        if self.existsNick(authUser.nick):
            return self.hasUser(self.authNick[authUser.nick], authUser)
        return False

    def hasIdent(self, authUser): 
        if self.existsIdent(authUser.ident):
            return self.hasUser(self.authIdent[authUser.ident], authUser)
        return False

    def hasHost(self, authUser): 
        if self.existsHost(authUser.host):
            return self.hasUser(self.authHost[authUser.host], authUser)
        return False

    def hasUser(self, users, authUser):
        for user in users:
            if user.equals(authUser):
                return True
        return False

    def getNick(self, authUser): 
        return self.getUser(self.authNick[authUser.nick], authUser)
    def getIdent(self, authUser): 
        return self.getUser(self.authIdent[authUser.ident], authUser)
    def getHost(self, authUser): 
        return self.getUser(self.authHost[authUser.host], authUser)

    def getUser(self, users, authUser):
        for user in users:
            if user.equals(authUser):
                return user

    def registerNick(self, authUser):
        if not self.existsNick(authUser.nick):
            self.createNick(authUser)

        self.authNick[authUser.nick].append(authUser)

    def registerIdent(self, authUser):
        if not self.existsIdent(authUser.ident):
            self.createIdent(authUser)

        self.authIdent[authUser.ident].append(authUser)

    def delNick(self, user): self.authNick[user.nick].remove(user)
    def delIdent(self, user): self.authIdent[user.ident].remove(user)
    def delHost(self, user): self.authHost[user.host].remove(user)

    def registerHost(self, authUser):
        if not self.existsHost(authUser.host):
            self.createHost(authUser)

        self.authHost[authUser.host].append(authUser)
   
    def createNick(self, authUser): self.authNick[authUser.nick] = []
    def createIdent(self, authUser): self.authIdent[authUser.ident] = []
    def createHost(self, authUser): self.authHost[authUser.host] = []

    def existsNick(self, nick): return nick in self.authNick
    def existsIdent(self, ident): return ident in self.authIdent
    def existsHost(self, host): return host in self.authHost

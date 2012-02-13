import config as cfg
'''

Userlevels
    1   Owner
    2   Admin
    3   User
'''
class AuthUser():
    
    def __init__(self,user,ident,host,level):
        self.user = user
        self.ident = ident
        self.host = host
        self.level = level
    
    def userf(self):
        if self.user == None:
            return '*'
        return self.user

    def identf(self):
        if self.ident == None:
            return '*'
        return self.ident
    
    def hostf(self):
        if self.host == None:
            return '*'
        return self.host


    def match(self,user,ident,host):
        if (user == '' or user == '*'):
            user = None
        if (ident == '' or ident == '*'):
            ident = None
        if (host == '' or host == '*'):
            host = None


        if (self.user == user):
            if self.ident == ident:
                if self.host == host:
                   return self.level, self

        if self.user == user:
            if self.ident == None:
                if self.host == host:
                    return self.level, self

        if self.user == None:
            if self.ident == ident:
                if self.host == host:
                    return self.level, self

        if self.user == None:
            if self.ident == None:
                if self.host == host:
                    return self.level, self

        if self.user == None:
            if self.ident == ident:
                if self.host == None:
                    return self.level, self

        if self.user == user:
            if self.ident == None:
                if self.host == None:
                    return self.level, self

        if self.user == None:
            if self.ident == None:
                if self.host == None:
                    return self.level, self


        if self.user == user:
            if self.ident == ident:
                if self.host == None:
                    return self.level, self



        #if ((self.user == user) or not user):
        #    if ((self.ident == ident) or not ident):
        #        if ((self.host == host) or not host):
        #            return self.level, self

        return None

class Auth():

    def __init__(self):
        self.users = []
        try:
            for owner in cfg.owner:
                user = owner[0]
                ident = owner[1]
                host = owner[2]
                self.addUser(user,ident,host,1)
        except:
            print '!! No owner(s) of the bot defined.'

        try:
            for admin in cfg.admin:
                user = admin[0]
                ident = admin[1]
                host = admin[2]
                self.addUser(user,ident,host,2)
        except:
            print '! Warning: No owners found.'

    def resolve(self,user,ident,host):
        for u in self.users:
            match = u.match(user,ident,host)
            if match and match[1] == u:
                return match[1]

        return None

    def addUser(self,user,ident,host,level):
        if (user == '' or user == '*'):
            user = None
        if (ident == '' or ident == '*'):
            ident = None
        if (host == '' or host == '*'):
            host = None

        self.users.append(AuthUser(user,ident,host,level))
        self.users = sorted(self.users, key=lambda user: user.level)

    def remUser(self,user,ident,host):
        for u in self.users:
            if u.match(user,ident,host):
                self.users.remove(u)
    
    def isLevel(self,user,ident,host,level):
        for u in self.users:
            match = self.resolve(user,ident,host)
            if match:
                if u == match and match.level <= level:
                    return match

        return None
       
    def listLevel(self,level):
        lvl = []
        for u in self.users:
            match = self.isLevel(u.user, u.ident, u.host, level)
            if match:
                lvl.append(u)

        return lvl

    def isOwner(self,user,ident,host):
        m = self.isLevel(user,ident,host,1)
        if m and m.level == 1:
            print 'Is Owner'
            return True
        return False

    def isAdmin(self,user,ident,host):
        m = self.isLevel(user,ident,host,2) 
        if m and m.level <= 2:
            return True
        return False

    def isUser(self,user,ident,host):
        m = self.isLevel(user,ident,host,3) 
        if m and m.level <= 3:
            return True
        return False
    
    def listOwners(self):
        return self.listLevel(1)

    def listAdmins(self):
        return self.listLevel(2)
        
    def listUsers(self):
        return self.listLevel(3)

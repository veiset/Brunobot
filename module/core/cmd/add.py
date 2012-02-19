cmd         = ['add']
usage       = 'add <level> <nick> <ident> <host>'
description = 'Adds a user to a permission group (owner/admin/user).'

def main(modules, data):
    argv          = data['argv']
    channel       = data['channel']
    communication = modules.mcore['communication']
    auth          = modules.mcore['auth']
    user          = data['nick']
    ident         = data['ident']
    host          = data['host']

    if argv:
        auth.isLevel(user,ident,host,1)
        if len(argv) != 4:
            communication.say(channel,'Usage: add level nick ident host.')
        else:
            lvl = None
            try:
                level = int(argv[0])
            except:
                if argv[0] == 'owner':
                    lvl = 1
                elif argv[0] == 'admin':
                    lvl = 2
                elif argv[0] == 'user':
                    lvl = 3
            if lvl:
                if auth.isLevel(user, ident, host, lvl):
                    auth.addUser(argv[1],argv[2],argv[3],lvl)
                    communication.say(channel,'User added.')
                else:
                    communication.say(channel,'You do not have permission to do that')
            else:
                communication.say(channel,'Could not determine user level')



cmd         = ['list']
usage       = 'list <level>, list owner, list admin, list user'
description = 'Displays users for usergroups.'

def main(modules, data):
    argv          = data['argv']
    channel       = data['channel']
    communication = modules.mcore['communication']
    auth          = modules.mcore['auth']

    if argv:
        if len(argv) != 1:
            communication.say(channel,'Usage: list <level>')
        else:
            users = []
            try: 
                users = auth.listLevel(int(argv[0]))
            except:
                if argv[0] == 'owner':
                    users = auth.listOwners()
                elif argv[0] == 'admin':
                    users = auth.listAdmins()
                elif argv[0] == 'user':
                    users = auth.listUsers()

            userlist = []
            if (len(users) > 0):
                for user in users:
                    userlist.append('%s (%s@%s)' % (user.userf(), user.identf(), user.hostf()))

                communication.say(channel,", ".join(userlist))
            else:
                communication.say(channel,"No users found for that group.")



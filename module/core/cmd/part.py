cmd         = ['part']
usage       = 'part <channel>'
description = 'Parts a channel.'

def main(modules, data):
    argv          = data['argv']
    channel       = data['channel']
    connection    = modules.mcore['connection']
    communication = modules.mcore['communication']
    auth          = modules.mcore['auth']
    user          = data['nick']
    ident         = data['ident']
    host          = data['host']

    if argv:
        if auth.isOwner(user,ident,host):
            try:
                connection.irc.send('PART %s\n' % argv[0])
                communication.say(channel, 'Parting %s ...' % argv[0])
                cfg.rem('channels','%s' % argv[0][1:])
            except:
                ''' Nothing '''
        else:
            communication.say(channel, 'You aren\'t allowed to do that.')


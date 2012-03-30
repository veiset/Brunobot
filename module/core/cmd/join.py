cmd         = ['join']
usage       = 'join <channel>'
description = 'Joins a new channel.'

from module.core.output import out

def main(modules, data):
    argv          = data['argv']
    channel       = data['channel']
    connection    = modules.mcore['connection']
    communication = modules.mcore['communication']
    auth          = modules.mcore['auth']
    cfg           = modules.mcore['cfg']
    user          = data['nick']
    ident         = data['ident']
    host          = data['host']

    if argv:
        if auth.isOwner(user, ident, host):
            try:
                chan = argv[0]
                connection.irc.send('JOIN %s\n' % chan)
                communication.say(channel, 'Joining %s ...' % chan)
                out.info('joined channel: %s ' % chan)
                cfg.set('channels','%s' % chan[1:])
            except:
                ''' Nothing '''

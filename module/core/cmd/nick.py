cmd         = ['nick']
usage       = 'nick <new nickname>'
description = 'Changes the bots nickname.'

from module.core.output import out

def main(modules, data):
    argv          = data['argv']
    channel       = data['channel']
    connection    = modules.mcore['connection']
    auth          = modules.mcore['auth']
    cfg           = modules.mcore['cfg']
    user          = data['nick']
    ident         = data['ident']
    host          = data['host']

    if argv:
        if auth.isOwner(user, ident, host):
            try:
                nick = argv[0]
                connection.irc.send(u'NICK %s\n' % nick)
                out.info('changed nick to: %s ' % nick)
                cfg.set('connection','nick', '%s' % nick)
            except:
                ''' Nothing '''

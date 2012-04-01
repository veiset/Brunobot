cmd         = ['quit']
usage       = 'quit, disconnect'
description = 'Quits the bot.'

from module.core.output import out

def main(modules, data):
    argv          = data['argv']
    channel       = data['channel']
    connection    = modules.mcore['connection']
    auth          = modules.mcore['auth']
    user          = data['nick']
    ident         = data['ident']
    host          = data['host']

    if auth.isOwner(user, ident, host):
        try:
            #connection.connected = False
            #connection.irc.send(u'QUIT \n')
            #connection.quit()
            modules.quit()
            out.info('Bot is shutting down by request of: %s!%s@%s' % (user, ident, host))
            out.newline()
        except:
            ''' Nothing '''


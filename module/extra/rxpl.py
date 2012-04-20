''' Required for Brunobot module'''
version = '1.0'
name    = 'rxpl'
require = ['communication','recentdata']
listen  = ['privmsg']
usage   = 's/<pattern>/<replacement>/'
description = 'Replaces something something'

import re
def main(data):

    nick = data['nick']
    ident = data['ident']
    host = data['host']
    channel = data['channel']
    message = data['msg']

    match = re.match('^s\/(.+?)\/(.+)/$',message)

    if match:
        user = recentdata.user(nick,ident,host)
        lastmsg = user.lastMsg()['msg']

        correct = re.sub(match.group(1), match.group(2), lastmsg)
        communication.say(channel, '%s meant: %s' % (nick, correct))


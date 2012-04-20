import sys
''' Required for Brunobot module'''
version     = '4.0'
name        = 'typoregex'
author      = 'Vegard Veiset' # optional
require     = ['communication','recentdata']
listen      = ['privmsg']
description = 'Regex style correction on last sentence'
usage       = 's/match/replacement/g'

import re

def validParse(message):
    if (len(message.split('/')) == 4
            and message[0:2] == 's/'
            and message[-2:] == '/g'):
        return True
    return False

def main(data):
    '''
    '''

    nick = data['nick']
    ident = data['ident']
    host = data['host']
    channel = data['channel']
    message = data['msg']
    
    # len(s/././g) has to be atleast 7
    if (len(message) >= 7) and validParse(message):
        p       = message.split('/')[1]
        repl    = message.split('/')[2]

        user    = recentdata.user(nick,ident,host)
        lastmsg = user.lastMsg()['msg']
        correct = re.sub(p,repl,lastmsg)

        communication.say(channel, '%s meant: %s' % (nick, correct))

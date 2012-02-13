''' Required for Brunobot module'''
version = '0.1'
name    = 'karma'
author  = 'Vegard Veiset'
require = ['communication','presist']
listen  = ['cmd','privmsg']
presist = ['karma'] # variables to save
cmd     = ['karma']
usage   = 'nick++, nick +1, nick--, nick -1'
description = 'Keeps a track of the karam of users.'

import re
karma = {}
reNICK = '([A-Za-z\[\]\\`_\^\{\|\}][A-Za-z0-9\[\]\\`_\^\{\|\}\-]{0,8})'

def main(data):
    '''
    Module listens to both cmd and privmsg, so
    checking which of the listeners to react to.
    Using presistence unit with the variable 'karma'
    so that when the bot restarts the data is saved.
    '''


    if 'cmd' in data:
        if data['argv']:
            nick = data['argv'][0]
            if nick in karma:
                communication.say(data['channel'],'Karma for %s is: %i' % (nick,karma[nick]))
            else:
                communication.say(data['channel'],'Could not find %s. (0 karma)' % nick)
        
    elif 'msg' in data:
        reKarmaPlus = reNICK + '(\+\+| \+1)'
        reKarmaMinus = reNICK + '(--| -1)'
        matchPlus = re.match(reKarmaPlus,data['msg'])
        matchMinus = re.match(reKarmaMinus,data['msg'])

        if matchPlus:
            match = matchPlus.group(1)
            if match in karma:
                karma[match] += 1
            else:
                karma[match] = 1

        elif matchMinus:
            match = matchMinus.group(1)
            if match in karma:
                karma[match] -= 1
            else:
                karma[match] = -1




import sys
''' Required for Brunobot module'''
version = '1.0'
name    = 'cmdtest'
require = ['communication']
listen  = ['cmd']

def main(data):

    channel = data['channel']

    if (data['argv']):
        communication.say(channel,"cmd '%s': argv %s !+1" % (data['cmd'], data['argv']) )
    else:
        communication.say(channel,"cmd '%s', no argv !+1" % (data['cmd']) )




''' Required for Brunobot module'''
version = '1.0'
name    = 'calc'
require = ['communication']
listen  = ['cmd']
cmd     = ['calc', 'c', 'gc']
usage   = 'calc 5+5'
description = 'Calculates something something...'

from math import *

def main(data):
    argv = data['argv']
    if argv:
        result = 0
        try:
            result = str(eval("".join(argv)))
        except:
            result = "error"

        communication.say(data['channel'],'Result: %s' % result)



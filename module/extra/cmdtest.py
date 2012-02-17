''' Required for Brunobot module'''
version = '1.0'
name    = 'cmdtest'
require = ['communication']
listen  = ['cmd']
cmd     = ['test']
usage   = 'test'
description = 'Only reply to a command. Very simple module.'

def main(data):
    communication.say(data['channel'],'test.')


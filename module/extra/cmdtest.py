'''
8ball module!
'''

''' Required for Brunobot module'''
version = '0.2'
name    = 'eightball'
author  = 'OEyvind Eide' # optional
require = ['communication']
listen  = ['cmd']
cmd     = ['eightball','8ball']
usage   = "eightball"
description = "Use this module for all big decisions in your life."

answers = ['Yes, without a doubt',
'It is certain',
'It is decidedly so',
'Without a doubt',
'Yes, definitely',
'You may rely on it',
'As I see it, yes',
'Most likely',
'Outlook good',
'Signs point to yes',
'Yes',
'Reply hazy, try again',
'Ask again later',
'Better not tell you now',
'Cannot predict now',
'Concentrate and ask again',
'Don\'t count on it',
'My reply is no',
'My sources say no',
'Outlook not so good',
'Very doubtful']

import random

def main(data):
    channel = data['channel']
    
    communication.say(channel,'%s' % (answers[random.randint(0,len(answers)-1)] ))

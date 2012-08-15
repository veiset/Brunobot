
'''
Linux man page searcher for BrunoBot.
Created on 15. August 2012
'''
__author__ = 'Alexander Polden'
__license__ = 'GPL'
__email__ = 'mockillo@gmail.com'


''' Required for Brunobot Plugin'''
version     = '0.1'
name        = 'man'
author      = 'Alexander Polden'
require     = ['communication']
listen      = ['cmd']
cmd         = ['man']
description = 'finds a man page on linux.die.net/man'
usage       = 'man <section> <command>' 


from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import re

def verifyPage(section, command):
    try:
        data = BeautifulSoup(urlopen('http://linux.die.net/man/%s/%s' % (section, command)).read())
        word = data.find('h2', {}).string.strip()
        return True
    except:
        return None

def main(data):
    argv = data['argv']
    if argv:
      if len(argv) == 2:
        html = verifyPage(argv[0], argv[1])
        if html:
          communication.say(data['channel'], '%s: http://linux.die.net/man/%s/%s' % (argv[1], argv[0], argv[1]))
        else:
          communication.say(data['channel'], 'No match for %s in section %s.' % (argv[1], argv[0]))
      elif len(argv) == 1:
        html = verifyPage('1', argv[0])
        if html:
          communication.say(data['channel'], '%s: http://linux.die.net/man/%s/%s' % (argv[0], '1', argv[0]))
        else:
          communication.say(data['channel'], 'No match for %s in section %s.' % (argv[0], '1'))
      else:
        communication.say(data['channel'], 'Usage: %s.' % (usage))
    else:
      communication.say(data['channel'], 'Usage: %s.' % (usage))

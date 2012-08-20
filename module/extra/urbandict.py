
'''
URL Resolver for brunobot.
Created on 11. feb. 2012
'''
__author__ = 'Vegard Veiset'
__license__ = 'GPL'
__email__ = 'veiset@gmail.com'


''' Required for Brunobot Plugin'''
version     = '0.1'
name        = 'urbandict'
author      = 'Vegard Veiset' # optional
require     = ['communication']
listen      = ['cmd']
cmd         = ['ud']
description = 'looks up a word in the urban dictionary'
usage       = 'ud <term>' 


from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import re

def readHTMLHeader(url):
    try:
        data = BeautifulSoup(urlopen(url).read())
        word = data.find('td', {'class':'word'}).string.strip()
        return (word, '%s' % data.html.head.meta['content'])
    except:
        return None

def main(data):
    argv = data['argv']
    if argv:
        html = readHTMLHeader("http://www.urbandictionary.com/define.php?term=%s" % " ".join(argv))
        if html:
            word, desc = html
            if desc and word.lower() == " ".join(argv).lower():
                communication.say(data['channel'], '%s: %s' % (" ".join(argv), desc))
            else:
                communication.say(data['channel'], 'No match for %s.' % " ".join(argv))
        else:
            communication.say(data['channel'], 'No match for %s.' % " ".join(argv))


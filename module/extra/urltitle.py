'''
URL Resolver for brunobot.
Created on 11. feb. 2012
'''
__author__ = 'Vegard Veiset'
__license__ = 'GPL'
__email__ = 'veiset@gmail.com'

''' Required for Brunobot Plugin'''
version     = '0.1'
name        = 'urltitle'
author      = 'Vegard Veiset' # optional
require     = ['communication']
listen      = ['privmsg']
description = 'gets the title of an URL posted'
usage       = 'something <URL> something' 


from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import re

def readHTMLHeader(url):
    try:
        data = BeautifulSoup(urlopen(url).read())
        return '%s' % data.html.head.title.string
    except:
        return None

def main(data):
    reURL = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    match = re.findall(reURL, data['msg'])
    
    if match:
        for title in match:
            header = readHTMLHeader(title)
            if header:
                header = header.replace('\n','').replace('  ','').strip() 
                print header
                communication.say(data['channel'], '[%s]' % header)

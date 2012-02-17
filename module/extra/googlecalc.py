'''
Google Calculator for brunobot
Created on 26. sep. 2011

@author: Andreas Halle
         Vegard Veiset - Porting to Brunobot v6
'''
from htmllib import HTMLParser
from re import search as rexsearch, IGNORECASE
from urllib2 import Request, quote, urlopen

''' Required for Brunobot module'''
version     = '1.1'
name        = 'googlecalc'
require     = ['communication']
listen      = ['cmd']
cmd         = ['calc','calculate','gc']
description = 'uses google to calculate different math expressions'
usage       = 'calc 5+5, calc 10^100' 
author      = 'Andreas Halle, Vegard Veiset' # optional


def search(s):
    '''
    search(s) -> string
    
    Return a string of the calculations from
    the Google Search Engine Calculator.
    
    Keyword arguments:
    search -- what to calculate
    '''
    # Add header to pretend to be Mozilla Firefox 3.6
    req = Request('http://google.com/search?q=%s' % quote(s))
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; ' \
                 + 'Linux x86_64; rv:6.0) Gecko/20100101 Firefox/6.0')

    calc = '<h2 class=r style="font-size:138%"><b>(.*?)</b>'
    
    results = urlopen(req).read()
    
    match = rexsearch(calc, results, IGNORECASE)
    if match != None:
        output = match.group(1).replace('<sup>', '^(').replace('</sup>', ')') \
                 .replace('&#215;', 'x')
        return unescape(output)
    return None



def unescape(s):
    try:
        p = HTMLParser(None)
        p.save_bgn()
        p.feed(s)
        return p.save_end()
    except:
        return s


def main(data):
    argv = data['argv']
    if argv: 
        argv = " ".join(argv)

        result = search(argv)
        if (result):
            communication.say(data['channel'],result)





'''
Wikipedia for brunobot v4
Created on 26. sep. 2011

@author: Andreas Halle
'''
from BeautifulSoup import BeautifulSoup
from urllib2 import quote, urlopen

''' Required for Brunobot module'''
version = '1.0'
name    = 'wiki'
author  = 'Andreas Halle, Vegard Veiset' # optional
require = ['communication']
listen  = ['cmd']
cmd     = ['wiki','w']
usage   = "wiki article, w article"
description = "Displays a short summary of a given wikipedia article."


def snippet(title):
    '''
    snippet(title) -> string
    
    Return a snippet of information about a title on Wikipedia.
    
    Keyword arguments:
    title -- title of an article on Wikipedia
    '''
    
    url = 'http://en.wikipedia.org/w/api.php?action=opensearch&format=' \
        + 'xml&prop=snippet&limit=1&srredirects&search=%s' % quote(title)
    
    try:
        data = BeautifulSoup(urlopen(url).read())
    except:
        return None
    title = data.find('text')
    description = data.find('description')
    if title == None or description == None:
        return None
    return '[%s] %s' % (title.contents[0], description.contents[0])


def main(data):
    if data['argv']:
        a = " ".join(data['argv'])
        article = snippet(a)
        if article:
            communication.say(data['channel'],article)
        else: 
            communication.say(data['channel'],'Could not find anything for "%s".' % a) 


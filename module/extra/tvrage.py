'''
TVRage for brunobot v4
Created on 26. sep. 2011

@author: Andreas Halle
'''
from urllib2 import quote, urlopen
from re import search as rexsearch

''' Required for Brunobot module'''
version     = '1.0'
name        = 'tvrage'
require     = ['communication']
listen      = ['cmd']
cmd         = ['tv','tvrage','show']
description = 'looks up when the next episode of a show airs'
usage       = 'tv <show>, tvrage <show> : example .tv futurama' 

class TVEpisode:
    '''
    Represent a TV episode on TVRage.com
    '''
    def __init__(self, name, season, episode, releasedate):
        '''
        Construct a TV episode.
        
        Keyword arguments:
        name        -- Episode name
        season      -- Which season the episode aired in
        episode     -- Episode number in season
        releasedate -- The date the episode will air or was aired
        '''
        self.name = name
        self.season = season
        self.episode = episode
        self.releasedate = releasedate
    
    
    
    def __cmp__(self, other):
        '''
        cmp(self, other) -> integer
        
        Compare two TV episodes by their release date.
        '''
        return cmp(self.releasedate, other.releasedate)
    
    
    
    def __str__(self):
        '''
        str() -> string
        
        Return a string representation of a TV episode.
        '''
        return '%sx%s: %s (%s)' % (self.season, self.episode, \
                                   self.name, self.releasedate)
    
    
    
class TVShow:
    '''
    Represent a TV show from TVRage.com.
    Currently only supports quickinfo from the TVRage API.
    '''
    def __init__(self, name):
        '''
        Construct a TV show.
        
        Keyword arguments:
        name -- name of the TV show
        '''
        self.name = name
        self.episodes = []
        self.quickinfo()
    
    
    
    def quickinfo(self):
        '''
        quickinfo() -> None
        
        Get the two most relevant episodes of the series via the quickinfo API.
        '''
        self.url = 'http://services.tvrage.com/tools/quickinfo.php?show=%s' \
                   % quote(self.name)
                   
        showinfo = urlopen(self.url)
        
        for line in showinfo.readlines():
            line = line.strip()
            desc = line.split('@')
            
            if desc[0] == 'Show Name':
                self.rname = desc[1]
            
            elif desc[0] == 'Latest Episode' or desc[0] == 'Next Episode':
                epgroup = rexsearch('^(\d+)x(\d+)\^(.*)\^(.*)$', desc[1])
                self.episodes.append(TVEpisode(epgroup.group(3), \
                                               epgroup.group(1), \
                                               epgroup.group(2), \
                                               epgroup.group(4)))
    
    
    
    def __str__(self):
        '''
        str() -> string
        
        Return a string representation of a TV show.
        '''
        output = self.rname
        for a in self.episodes:
            output += ' -- %s' % a
        
        return output



def main(data):
    cmd = data['cmd']
    argv = data['argv']
    if (argv):
        if cmd == "tv" or cmd == "tvshow":
            show = TVShow(" ".join(argv))
            communication.say(data['channel'],str(show))

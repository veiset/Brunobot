import re
import urllib.request
from bs4 import BeautifulSoup

import api.base
class URLTitle(api.base.BrunoAPI):
    ''' Resolves title of posted URLs '''

    reURL = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    def __init__(self, brunobot):
        super().__init__(brunobot)

        self.addListener("privmsg", self.url)
        self.addListener("cmd.url", self.urlcmd)

    def url(self, event):
        ''' Find URLs in a message and tries to resolve the URL title '''
        match = re.findall(self.reURL, event.get('msg'))

        if match:
            for url in match:
                title = URLTitle.readHTMLTitle(url)
                if title:
                    self.bot.irc.say(event.get('channel'), '[%s]' % title)

    def urlcmd(self, event):
        ''' Finds the title of a given URL '''
        if event.has('param'):
            url = event.get('param')[0]
            title = URLTitle.readHTMLTitle(url)
            if title:
                self.bot.irc.say(event.get('channel'), '[%s]' % title)
            else:
                self.bot.irc.say(event.get('channel'), 'No result')

    def readHTMLTitle(url):
        ''' Resolves the title of an URL '''
        try:
            data = BeautifulSoup(urllib.request.urlopen(url).read())
            return '%s' % data.html.head.title.string
        except:
            return None 

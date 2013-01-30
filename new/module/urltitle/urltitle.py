import re
import urllib.request
from bs4 import BeautifulSoup

class Module():
    ''' Resolves title of posted URLs '''

    def __init__(self, bot):
        self.bot = bot
        self.reURL = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        self.bot.irc.addListener("privmsg", self.url)
        self.bot.irc.addListener("cmd.url", self.urlcmd)
        self.api = {'htmlTitle' : readHTMLTitle}

    def url(self, event):
        ''' Find URLs in a message and tries to resolve the URL title '''
        match = re.findall(self.reURL, event.get('message'))

        if match:
            for url in match:
                title = readHTMLTitle(url)
                if title:
                    self.bot.irc.say(event.get('channel'), '[%s]' % title)

    def urlcmd(self, event):
        ''' Finds the title of a given URL '''
        if event.has('argv'):
            title = readHTMLTitle(event.get('argv'))
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

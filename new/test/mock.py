class Bot:
    def __init__(self):
        self.events = []
        self.irc = IRC()

class IRC:

    def __init__(self):
        self.events = []

    def event(self, e):
        self.events.append(('event', e))

    def addListener(self, eventName, func):
        self.events.append(('addListener', (eventName, func)))

    def delListener(self, eventName, func):
        self.events.append(('removeListener', (eventName, func)))

    def send(self, data):
        self.events.append(('send', data))

    def join(self, data):
        self.events.append(('join', data))

    def part(self, data):
        self.events.append(('part', data))

    def mode(self, channel, mode):
        self.events.append(('mode', (channel, mode)))

    def say(self, target, message):
        self.events.append(('message', (target, message)))

    def connect(self):
        self.events.append(('connect'))

    def disconnect(self):
        self.events.append(('disconnect'))

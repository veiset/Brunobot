import api.base
class PlanningPoker(api.base.BrunoAPI):
    ''' Scrum planning poker module  '''

    class Issue:
        def __init__(self, text, needed, author, channel):
            self.users = PlanningPoker.Users()
            self.text = text 
            self.needed = needed 
            self.author = author
            self.channel = channel

        def getCurrentVotes(self): return len(self.users.users)

    class Users:
        def __init__(self):
            self.users = {}

        def hasUser(self, user): return user in self.users
        def getUserVote(self, user): return self.users[user]
        def addUserVote(self, user, weight): self.users[user] = weight

        def getVotes(self):
            return [weight for weight in self.users.values()]

        def getAverage(self):
            if len(self.users) == 0:
                return 0

            return sum(self.getVotes())/len(self.users)

    def __init__(self, brunobot):
        super().__init__(brunobot)

        self.issueId = 0
        self.issues = {} 

        self.addListener("cmd.pp.start", self.start)
        self.addListener("cmd.pp.status", self.status)
        self.addListener("cmd.pp.agree", self.agree)
        self.addListener("privmsg", self.addVote)

    def doneVoting(self, issueId):
        issue = self.issues[issueId]

        avg = issue.users.getAverage()
        votes = issue.users.getVotes()

        issue.users = PlanningPoker.Users()
        self.bot.irc.say(
            issue.channel, 
            'Done voting on issue %s (%s), average vote: %s, votes: %s.' % (
                issueId,
                issue.text,
                avg,
                votes
            )
        )
        self.bot.irc.say(
            issue.channel, 
            'Vote on %s reset. To close it, type: .pp.agree %s' % (issueId, issueId)
        )

    def addVote(self, event):
        if event.get('channel') == None:
            user = event.get('user')
            nick, ident, host = user

            command, issueId, weight = event.get('msg').split(' ')
            if command == 'pp':
                    issueId = int(issueId)
                    weight = int(weight)
                    issue = self.issues[issueId]

                    if issue.users.hasUser(nick):
                        self.bot.irc.say(nick, "You have already voted during this round.")
                    else:
                        issue.users.addUserVote(nick, weight)
                        self.bot.irc.say(nick, "Vote registered on the issue '%s'." % issue.text)

                        if issue.getCurrentVotes() == issue.needed:
                            self.doneVoting(issueId)


    def status(self, event):
        param = event.get('param')
        issueId = int(param)
        issue = self.issues[issueId]

        self.bot.irc.say(
            event.get('channel'), 
            'Planning poker ID %s (%s): has received %s of %s votes.' % (
                issueId, 
                issue.text,
                issue.getCurrentVotes(),
                issue.needed
            )
        )

    def agree(self, event):
        param = event.get('param')
        issueId = int(param)
        issue = self.issues[issueId]

        if event.get('user') == issue.author:
            del self.issues[issueId]
            self.bot.irc.say(
                event.get('channel'), 
                'Planning poker ID %s (%s) has been closed.' % (
                    issueId, 
                    issue.text
                )
            )
        else:
            self.bot.irc.say(
                event.get('channel'), 
                'You cannot do that. Issue belongs to %s.' % issue.author
            )

    def start(self, event):
        param = event.get('param')
        people, issuetext = param.split(' ', 1)

        self.issueId += 1
        try:
            user = event.get('user')
            chan = event.get('channel')

            issue = PlanningPoker.Issue(issuetext, int(people), user, chan)

            self.issues[self.issueId] = issue
            self.bot.irc.say(
                event.get('channel'), 
                'Planning poker ID %s (%s) started.' % (self.issueId, issue.text)
            )
            self.bot.irc.say(
                event.get('channel'), 
                'type: "/msg %s pp %s <weight>" to vote on the issue.' % (self.bot.nick, self.issueId)
            )
        except:
            self.bot.irc.say(
                event.get('channel'), 
                'Could not create issue. Wrong format, please use: "<numOfPlayers> Issue Text"'
            )

        


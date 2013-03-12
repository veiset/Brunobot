Brunobot API: Users
===================
API for getting a list of the users in a channel, and for checking
the status (op, voice...) of a given user in a channel.

Constants
=========
```python
REGULAR
VOICE
HALFOP
OP
OWNER 
FOUNDER 
```

API Methods
===========
```python
hasStatus(channel, nick, status) -> boolean
getUserStatus(channel, nick) -> status
getChannelList(channel) -> List of (nick, status)
```

hasStatus
---------
```python
hasStatus(channel, nick, status)
    '''
    Checks if a user has the given status.

    Keyword arguments:
    channel -- IRC channel name
    nick    -- IRC user nickname
    status  -- The status to check against

    Example usage:
    >>> if hasStatus('#mychan', 'someNick', OP):
    >>>     print("The user is OPed")

    return If the user on the channel has the given status
    '''
```

getUserStatus
-------------
```python
getUserStatus(channel, nick)
    '''
    Looks up the status of a user in the given channel.
    A user can have the following statuses: 
    REGULAR, VOICE, HALFOP, OP, OWNER, FOUNDER

    Keyword arguments:
    channel -- IRC channel name
    nick    -- IRC user nickname

    Example usage:
    >>> if VOICE in getUserStatus('#mychan', 'someNick'):
    >>>     print("The user is VOICEed")
    
    return A list of statuses the user have
    '''
```

getChannelList
--------------
```python
```python
getChannelList(channel)
    '''
    Returns a list of (user, status) from a channel.

    Keyword arguments:
    channel -- IRC channel name

    Example usage:
    >>> for user, status in getChannelList('#mychan'):
    >>>     print("%s has status %s", % (user, status))

    retrun A list of (user, status)
    '''
```

Example module
==============
```python
import api.base
class UserStatus(api.base.BrunoAPI):
    ''' Resolves a status of a user in a channel'''

    def __init__(self, brunobot):
        super().__init__(brunobot)
        self.users = self.bot.api.get('users')

        self.addListener("cmd.status", self.status)

    def status(self, event):
        nick, ident, host = event.get('user')
        channel = event.get('channel')
        chanStatus = self.users().getUserStatus(channel, nick)

        if chanStatus == self.users().OP:
            self.bot.irc.say(channel, 'You got the power!'))
        else:
            self.bot.irc.say(channel, 'Insufficient')
```


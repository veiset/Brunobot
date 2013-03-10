import unittest
import api.users.users as users
import test.mock as mock
import test.mockdata as data
from pyric.events import Event

class UsersAPITest(unittest.TestCase):
    
    def setUp(self):
        self.bot = mock.Bot()
        self.bot.irc = mock.IRC()
        self.usersAPI = users.Users(self.bot)
    

    def test_that_joined_user_should_be_added_to_chanlist_as_regular_user(self):
        nick, ident, host = data.user
        event = data.event_join

        self.usersAPI.joinEvent(event)

        assert data.channel in self.usersAPI.channels
        assert nick in self.usersAPI.channels[data.channel]
        assert self.usersAPI.getUserModes(data.channel, nick) == [self.usersAPI.REGULAR]

    def test_that_parted_user_gets_removed_from_channel_userlist(self):
        self.usersAPI.joinEvent(data.event_join)
        part = data.event_part
        self.usersAPI.partEvent(part)
        
        channel = part.get('channel')
        assert channel in self.usersAPI.channels 
        assert len(self.usersAPI.channels[channel]) == 0

    def test_that_OP_event_gets_stored(self):
        nick, ident, host = data.user
        self.usersAPI.joinEvent(data.event_join)

        mode = data.event_mode
        mode.add('msg', '+o %s' % nick)
        self.usersAPI.modeEvent(mode)

        modes = self.usersAPI.getUserModes(data.channel, nick)
        assert self.usersAPI.OP in modes

    def test_that_multiple_modes_gets_stored(self):
        nick, ident, host = data.user
        self.usersAPI.joinEvent(data.event_join)

        mode = data.event_mode
        mode.add('msg', '+ov %s %s' % (nick, nick))
        self.usersAPI.modeEvent(mode)

        modes = self.usersAPI.getUserModes(data.channel, nick)
        assert self.usersAPI.OP in modes
        assert self.usersAPI.VOICE in modes
        
    def test_that_the_same_mode_only_gets_stored_once(self):
        nick, ident, host = data.user
        self.usersAPI.joinEvent(data.event_join)

        mode = data.event_mode
        mode.add('msg', '+o %s' % nick)
        self.usersAPI.modeEvent(mode)

        mode = data.event_mode
        mode.add('msg', '+o %s' % nick)
        self.usersAPI.modeEvent(mode)

        modes = self.usersAPI.getUserModes(data.channel, nick)
        assert self.usersAPI.OP in modes
        assert self.usersAPI.REGULAR in modes
        assert len(modes) == 2 

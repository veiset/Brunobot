import unittest
import api.users.users as users
import test.mock as mock
import test.mockdata as data
from pyric.events import Event

class UsersAPITest(unittest.TestCase):
    
    def setUp(self):
        self.bot = mock.Bot()
        self.bot.irc = mock.IRC()
        self.api = users.Users(self.bot)
    

    def test_that_joined_user_should_be_added_to_chanlist_as_regular_user(self):
        nick, ident, host = data.user
        event = data.event_join

        self.api.joinEvent(event)

        assert data.channel in self.api.channels
        assert nick in self.api.channels[data.channel]
        assert self.api.getUserStatus(data.channel, nick) == [self.api.REGULAR]

    def test_that_parted_user_gets_removed_from_channel_userlist(self):
        self.api.joinEvent(data.event_join)
        part = data.event_part
        self.api.partEvent(part)
        
        channel = part.get('channel')
        assert channel in self.api.channels 
        assert len(self.api.channels[channel]) == 0

    def test_that_OP_event_gets_stored(self):
        nick, ident, host = data.user
        self.api.joinEvent(data.event_join)

        mode = data.event_mode
        mode.add('msg', '+o %s' % nick)
        self.api.modeEvent(mode)

        status = self.api.getUserStatus(data.channel, nick)
        assert self.api.OP in status 

    def test_that_multiple_modes_gets_stored(self):
        nick, ident, host = data.user
        self.api.joinEvent(data.event_join)

        mode = data.event_mode
        mode.add('msg', '+ov %s %s' % (nick, nick))
        self.api.modeEvent(mode)

        status = self.api.getUserStatus(data.channel, nick)
        assert self.api.OP in status 
        assert self.api.VOICE in status 
        
    def test_that_the_same_mode_only_gets_stored_once(self):
        nick, ident, host = data.user
        self.api.joinEvent(data.event_join)

        mode = data.event_mode
        mode.add('msg', '+o %s' % nick)
        self.api.modeEvent(mode)

        mode = data.event_mode
        mode.add('msg', '+o %s' % nick)
        self.api.modeEvent(mode)

        status = self.api.getUserStatus(data.channel, nick)
        assert self.api.OP in status 
        assert self.api.REGULAR in status 
        assert len(status) == 2 

    def test_that_listing_of_names_add_names_to_channel(self):
        event = data.event_353
        channel = data.channel
        event.add('msg', '~vz @vx %bo +an &br sm el')

        self.api.namesEvent(data.event_353)
        userlist = self.api.getChannelList(channel)

        assert len(userlist) == 7
        # All the users have the status REGULAR
        assert self.api.FOUNDER in userlist['vz'] and len(userlist['vz']) == 2
        assert self.api.OWNER   in userlist['br'] and len(userlist['br']) == 2
        assert self.api.OP      in userlist['vx'] and len(userlist['vx']) == 2
        assert self.api.HALFOP  in userlist['bo'] and len(userlist['bo']) == 2
        assert self.api.VOICE   in userlist['an'] and len(userlist['an']) == 2
        assert self.api.REGULAR in userlist['sm'] and len(userlist['sm']) == 1


    def test_that_hasStatus_returns_stauts_of_nick(self):
        event = data.event_353
        channel = data.channel
        event.add('msg', '~vz @vx %bo +an &br sm el')

        self.api.namesEvent(data.event_353)

        assert self.api.hasStatus(data.channel, 'vz', self.api.FOUNDER)
        assert self.api.hasStatus(data.channel, 'vx', self.api.OP)


    def test_that_hasStatus_on_non_exisiting_user_returns_False(self):
        assert not self.api.hasStatus(data.channel, 'batman', self.api.REGULAR)
        

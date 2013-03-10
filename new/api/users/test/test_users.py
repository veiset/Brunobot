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
    

    def test_that_joined_user_should_be_added_to_chanlist_with_no_modes(self):
        event = data.event_join

        self.usersAPI.joinEvent(event)

        assert event.get('channel') in self.usersAPI.chans
        assert self.usersAPI.chans[event.get('channel')][event.get('user')] == None 

    def test_that_parted_user_gets_removed_from_channel_userlist(self):
        self.usersAPI.joinEvent(data.event_join)
        part = data.event_part
        self.usersAPI.partEvent(part)
        
        channel = part.get('channel')
        assert channel in self.usersAPI.chans 
        assert len(self.usersAPI.chans[channel]) == 0


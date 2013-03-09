import unittest
import api.users.users as users
import test.mock as mock
import test.mockdata as data

class UsersAPITest(unittest.TestCase):
    
    def setUp(self):
        self.bot = mock.Bot()
        self.bot.irc = mock.IRC()
        self.usersAPI = users.Users(self.bot)

    def test_newUsersObject(self):
        assert True

    def test_that_users_trigger_join_event(self):
        assert True

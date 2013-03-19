import unittest

import test.mock as mock
import test.mockdata as data
import api.manager
from pyric.events import Event

class UsersAPITest(unittest.TestCase):
    
    def setUp(self):
        self.bot = mock.Bot()
        self.bot.irc = mock.IRC()
        self.api = users.Users(self.bot)


import unittest
import test.mock as mock
import test.mockdata as data

import api.base
import api.manager

class ManagerAPITest(unittest.TestCase):
    
    def setUp(self):
        self.manager = api.manager.Manager()

    def test_that_loading_of_unadded_module_throws_exception(self):
        try:
            self.manager.load('can.not.touch.this')
            assert False
        except:
            assert True

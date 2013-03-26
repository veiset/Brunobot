import unittest
import test.mock as mock
import test.mockdata as data

import api.base
import api.manager

class ManagerAPITest(unittest.TestCase):
    
    def setUp(self):
        self.manager = api.manager.Manager(mock.Bot())

    def test_that_loading_of_unadded_module_throws_exception(self):
        try:
            self.manager.load('someapi')
            assert False
        except:
            assert True

    def test_that_loaded_api_module_can_be_used(self):
        self.manager.add("test.mockapi", "mockapi")
        self.manager.load("mockapi")
        mockapi = self.manager.get("mockapi")
        mockapi().fun1()


    def test_that_variables_in_locally_saved_api_gets_updated_when_reloaded(self):
        self.manager.add("test.mockapi", "mockapi")
        self.manager.load("mockapi")

        self.mockapi = self.manager.get("mockapi")
        
        self.mockapi().CONSTANT = 10
        assert self.mockapi().CONSTANT == 10

        self.manager.reload("mockapi")
        assert self.mockapi().CONSTANT == 15

    def test_that_changes_in_locally_saved_api_gets_removed_when_reloaded(self):
        self.manager.add("test.mockapi", "mockapi")
        self.manager.load("mockapi")

        self.mockapi = self.manager.get("mockapi")
        
        def myfun(): return 5
        self.mockapi().fun = myfun

        assert self.mockapi().fun() == 5
        
        if self.manager.isLoaded("mockapi"):
            self.manager.reload("mockapi")
            try:
                self.mockapi().fun()
                assert False
            except:
                assert True
        else:
            raise Exception("Class should be loaded, but is not.")


    def test_that_reloadall_reloads_all_modules(self):
        self.manager.add("test.mockapi", "mockapi")
        self.manager.load("mockapi")

        self.mockapi = self.manager.get("mockapi")
        
        def myfun(): return 5
        self.mockapi().fun = myfun

        assert self.mockapi().fun() == 5
        
        if self.manager.isLoaded("mockapi"):
            self.manager.reloadAll()
            try:
                self.mockapi().fun()
                assert False
            except:
                assert True
        else:
            raise Exception("Class should be loaded, but is not.")


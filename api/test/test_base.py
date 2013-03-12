import unittest
import test.mock as mock
import test.mockdata as data
import test.mockapi as mockapi

import api.base


class BaseAPITest(unittest.TestCase):
    
    def setUp(self):
        self.dummyAPI = mockapi.DummyAPI(mock.Bot())
        self.simpleAPI = api.base.SimpleAPI(self.dummyAPI)

    def test_that_simple_api_has_variables(self):
        assert self.simpleAPI.CONSTANT == mockapi.DummyAPI.CONSTANT
        assert self.simpleAPI.var1 == self.dummyAPI.var1

    def test_that_changes_in_simpleAPI_constants_doesnt_change_dummyAPI(self):
        assert self.simpleAPI.var1 == self.dummyAPI.var1
        self.simpleAPI.var1 = 'something else'
        assert not self.simpleAPI.var1 == self.dummyAPI.var1

    def test_that_function_can_access_class_variable(self):
        assert self.simpleAPI.fun3() == mockapi.DummyAPI.CONSTANT

    def test_that_private_function_is_inaccessable(self):
        try: 
            self.simpleAPI.fun4()
            assert False
        except:
            assert True

    def test_that_private_variable_is_inaccessable(self):
        try: 
            self.simpleAPI.var3
            assert False
        except:
            assert True

    def test_that_simpleAPI_can_mutate_baseAPI(self):
        newValue = "my awesome value"
        self.simpleAPI.fun2(newValue)
        assert self.dummyAPI.var3 == newValue
    
    def test_that_docstrings_are_added_to_functions(self):
        assert self.simpleAPI.fun1.__doc__ == 'Docstring'

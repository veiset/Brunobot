import unittest
import test.mock as mock
import test.mockdata as data

import api.base

class DummyAPI(api.base.BrunoAPI):
    
    CONSTANT = 15

    def __init__(self, bot):
        super().__init__(bot)

        self.var1 = 'hello'
        self.var2 = 'yes'
        self.var3 = 'nope'

        self.api.function(self.fun1)
        self.api.functions([self.fun2, self.fun3])

        self.api.constant('CONSTANT', self.CONSTANT)
        self.api.constants([('var1', self.var1), ('var2', self.var2)])

    def fun1(self): 
        '''Docstring'''
        return "dummy implementation"
    def fun2(self, param): self.var3 = param
    def fun3(self): return self.CONSTANT
    def fun4(self): return "private function"

class BaseAPITest(unittest.TestCase):
    
    def setUp(self):
        self.dummyAPI = DummyAPI(mock.Bot())
        self.simpleAPI = api.base.SimpleAPI(self.dummyAPI)

    def test_that_simple_api_has_variables(self):
        assert self.simpleAPI.CONSTANT == DummyAPI.CONSTANT
        assert self.simpleAPI.var1 == self.dummyAPI.var1

    def test_that_changes_in_simpleAPI_constants_doesnt_change_dummyAPI(self):
        assert self.simpleAPI.var1 == self.dummyAPI.var1
        self.simpleAPI.var1 = 'something else'
        assert not self.simpleAPI.var1 == self.dummyAPI.var1

    def test_that_function_can_access_class_variable(self):
        assert self.simpleAPI.fun3() == DummyAPI.CONSTANT

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

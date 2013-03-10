import unittest
import sys
import test.mock as mock
import test.mockdata as data

import api.base
import api.classloader


class ClassLoaderTest(unittest.TestCase):
    
    def setUp(self):
        self.loader = api.classloader.Loader()


    def test_that_loader_loades_unloaded_file(self):
        modulePath = "test.mockclass"
        assert not self.loader.isLoaded(modulePath)

        try:
            mockclass = test.mockclass.MockClass()
            assert False
        except:
            assert True

        self.loader.load(modulePath)
        assert self.loader.isLoaded(modulePath)
        module = self.loader.get(modulePath)

        mockclass = module.MockClass()
        assert mockclass.fun() == 'value'

    def test_unloading_of_a_module(self):
        modulePath = "test.mockclass"

        self.loader.load(modulePath)
        assert self.loader.isLoaded(modulePath)

        self.loader.unload(modulePath)
        assert not self.loader.isLoaded(modulePath)
        assert not modulePath in sys.modules
        

    def test_that_reloading_reset_state(self):
        modulePath = "test.mockclass"
        self.loader.load(modulePath)
        module = self.loader.get(modulePath)
        module.var = "not default"

        self.loader.reload(modulePath)
        module = self.loader.get(modulePath)

        assert not module.var == "not default"

    def test_that_loader_resolves_class(self):
        modulePath = "test.mockclass"
        self.loader.load(modulePath)
        mockclass = self.loader.getClass(modulePath)
        instanceOfClass = mockclass()

        assert instanceOfClass.fun() == 'value'

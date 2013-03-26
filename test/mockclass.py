import api.base

var = 'default' 

class MockClass(api.base.BrunoAPI):
    def __init__(self):
        self.value = 'value'

    def fun(self):
        return self.value

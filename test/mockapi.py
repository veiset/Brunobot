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

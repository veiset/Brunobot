import inspect

class Function():
    def __init__(self, fun):
        self.fun = fun
        self.name = fun.__name__
        self.doc = fun.__doc__
        self.args = inspect.getargspec(fun).args

class Constant():
    def __init__(self, name, value):
        self.name = name
        self.value = value

class BrunoAPI:
    
    def __init__(self, brunobot):
        self.bot = brunobot
        self.api = self.API()


    class API:
        def __init__(self):
            self.fun = []
            self.const = []

        def function(self, fun):
            ''' 
            Keyword arguments:
            fun -- Single function to be added as API function
            '''
            self.fun.append(Function(fun))

        def functions(self, funs):
            ''' 
            Keyword arguments:
            funs -- List of Functions to be added as API functions 
            '''
            for fun in funs:
                self.function(fun)

        def constant(self, name, value):
            self.const.append(Constant(name, value)) 

        def constants(self, varset):
            for name, value in varset:
                self.constant(name, value)

class SimpleAPI():
    
    def __init__(self, module):
        '''
        Takes a brunobot API module and extract the API methods and constants.
        '''
        for function in module.api.fun:
            setattr(self, function.name, function.fun)

        for variable in module.api.const:
            setattr(self, variable.name, variable.value)

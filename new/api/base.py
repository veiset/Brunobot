import inspect

class Function():
    def __init__(self, fun):
        self.fun = fun
        self.name = fun.__name__
        self.doc = fun.__doc__
        self.args = inspect.getargspec(fun).args

class BrunoAPI:
    

    def api(self):
        return self.API()

    class API:
        def __init__(self):
            self.functions = []

        def function(self, fun):
            ''' 
            Keyword arguments:
            fun -- Single function to be added as API function
            '''
            self.functions.append(Function(fun))

        def functions(self, funs):
            ''' 
            Keyword arguments:
            funs -- List of Functions to be added as API functions 
            '''
            for fun in funs:
                self.functions.append(Function(fun))

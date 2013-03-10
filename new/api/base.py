import inspect

class Function():
    def __init__(self, fun):
        self.fun = fun
        self.name = fun.__name__
        self.doc = fun.__doc__
        self.args = inspect.getargspec(fun).args

class API:

    def __init__(self, bot):
        self.API = self
        self.functions = []

    def addAPI(self, fun):
        self.functions.append(Function(fun))

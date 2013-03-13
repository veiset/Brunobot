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
        self.listeners = []

    def addListener(self, event, fun):
        self.listeners.append((event,fun))
        self.bot.irc.addListener(event, fun)
    
    def remListener(self, event, fun):
        self.listeners.remove((event,fun))
        self.bot.irc.removeListener(event, fun)

    def unload(self):
        for event, fun in self.listeners:
            self.remListener(event, fun)
        
    def getEnvironment(self):
        return [(var, self.getVariableValue(var)) for var in self.getVariables()]

    def getVariables(self):
        return [attr for attr in dir(self) 
                   if self.isVariable(attr) and not self.isDefaultVariable(attr)]

    def isVariable(self, attr):
        return not (callable(self.getVariableValue(attr)) or attr.startswith('__'))

    def isDefaultVariable(self, attr):
        return attr in ['api', 'bot', 'listeners']

    def getVariableValue(self, var):
        return self.__getattribute__(var)


    class API:
        def __init__(self):
            self.fun = []
            self.const = []
            self.presist = []

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

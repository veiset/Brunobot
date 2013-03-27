import ast
import math
from math import *
import api.base


class Calc(api.base.BrunoAPI):
    ''' Module for doing simple math operations '''

    LEGAL = ['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 
             'copysign', 'cos', 'cosh', 'degrees', 'e', 'erf', 'erfc', 'exp',
             'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum', 
             'gamma', 'hypot', 'isfinite', 'isinf', 'isnan', 'ldexp', 'lgamma', 
             'log', 'log10', 'log1p', 'log2', 'modf', 'pi', 'pow', 'radians', 
             'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'trunc', 
             'max', 'min']

    def __init__(self, brunobot):
        super().__init__(brunobot)

        self.addListener("cmd.calc", self.calc)
        self.addListener("cmd.calc.help", self.helpdoc)

    def calc(self, event):
        ''' Calculates a given expression '''
        param = event.get('param')

        if self.legalExpression(param):
            result = str(eval(param.lower()))
            self.bot.irc.say(event.get('channel'), 'Result: %s' % result)
        else:
            self.bot.irc.say(event.get('channel'), 'Result: Illegal expr.')


    def helpdoc(self, event):
        ''' Returns docstring of a function '''
        param = event.get('param')
        functions = Calc.Visitor().visit(ast.parse(param))

        if len(functions) == 1:
            function = functions[0]
            doc = self.docstring(function)

            self.bot.irc.say(event.get('channel'), '%s: %s' % (function, doc))


    def docstring(self, function):
        if function in self.LEGAL:
            return eval(function).__doc__
        return "Illegal / No such function."

    def legalExpression(self, expr):
        '''
        legalExpression(string) -> true/false

        Checks if a string is a legal python math expression.

        Keyword arguments:
        expr -- mathematical expression

        Return true if valid, false otherwise
        '''
        try:
            functions = Calc.Visitor().visit(ast.parse(expr.lower()))
            for e in functions:
                if e not in self.LEGAL:
                    return False
        except:
            return False 

        return True

    def isMathExpr(self, expr):
        ''' Returns true if expr is in standard math library '''
        return expr in [e for e in dir(math) if not e.startswith('__')]


    class Visitor(ast.NodeVisitor):
        ''' 
        Class for finding variables in an expression.
        
        >>> v = visitor()
        >>> expr = ast.parse('5+sin(x)')
        >>> v.visit(expr)
        ['sin', 'x']
        '''

        def visit_Module(self, node):
            self.functions = list()
            self.generic_visit(node)
            return self.functions

        def generic_visit(self, node):
            ast.NodeVisitor.generic_visit(self, node)

        def visit_Name(self, node): 
            self.functions.append(node.id)

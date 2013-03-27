import ast
import math
from math import *
import api.base


class Calc(api.base.BrunoAPI):
    ''' Module for doing simple math operations '''

    def __init__(self, brunobot):
        super().__init__(brunobot)

        self.addListener("cmd.calc", self.calc)

    def calc(self, event):
        ''' Calculates a given expression '''
        param = event.get('param')

        if self.legalExpression(param):
            result = str(eval(param.lower()))
            self.bot.irc.say(event.get('channel'), 'Result: %s' % result)
        else:
            self.bot.irc.say(event.get('channel'), 'Result: Illegal expr.')


    def legalExpression(self, expr):
        '''
        legalExpression(string) -> true/false

        Checks an expression against the functions in pythons math
        library and returns the expression if all variables
        in the expression are functions in python.math. 

        Will return the 'func.__doc__' if not parameters to
        the function is given.

        Keyword arguments:
        expr -- mathematical expression

        Return the expression if it is valid, false otherwise
        '''
        try:
            functions = Calc.Visitor().visit(ast.parse(expr.lower()))
            for f in functions:
                if not self.isMathExpr(f):
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

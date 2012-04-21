''' Required for Brunobot module'''
version = '1.0'
name    = 'calc'
require = ['communication']
listen  = ['cmd']
cmd     = ['calc', 'c', 'gc']
usage   = 'calc 5+5'
description = 'Calculates something something...'

import ast
from math import *

# >>> import math
# >>> pythonMath = dir(math)
pythonMath = ['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 
              'ceil', 'copysign', 'cos', 'cosh', 'degrees', 'e', 'erf', 
              'erfc', 'exp', 'expm1', 'fabs', 'factorial', 'floor', 'fmod',
              'frexp', 'fsum', 'gamma', 'hypot', 'isinf', 'isnan', 'ldexp',
              'lgamma', 'log', 'log10', 'log1p', 'modf', 'pi', 'pow', 'radians',
              'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'trunc']

class visitor(ast.NodeVisitor):

    def visit_Module(self, node):
        self.functions = list()
        self.generic_visit(node)
        return self.functions

    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Name(self, node): 
        self.functions.append(node.id)

def legalExpr(expr):
    expr = expr.lower()
    try:
        functions = visitor().visit(ast.parse(expr))
        for f in functions:
            if not f in pythonMath:
                return False
        if len(functions) == 1:
            if len(functions[0]) == len(expr):
                return '%s.__doc__' % functions[0]
        return expr
    except:
        return False 


def main(data):
    argv = data['argv']
    if argv:
        expr = legalExpr("".join(argv))
        if expr:
            try:
                result = str(eval(expr.lower()))
            except:
                result = "error"
        else:
            result = "error"

        communication.say(data['channel'],'Result: %s' % result)



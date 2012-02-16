import unittest
import sys
import inspect
import testcases as tests


class TestLogger():
    '''
    Impelementing the same function as sys.stdout, and
    thus being able to use this class as a logger instead
    of sys.stdout. This class is used remove output
    to the terminal.
    ''' 
    def __init__(self):
        ''' do nothing '''
    def write(self,data):
        ''' do nothing '''
    def flush(self):
        ''' do nothing '''

logger = TestLogger()

def printResults(successful,testsRun,errors,failures):
    print "%s/%s tests successful." % (successful,testsRun)
    if errors:
        print "Errors:"
        for error in errors:
            print '%s : %s' % (error[0],error[1])
    
    if failures:
        print "Failures:"
        for failure in failures:
            print '%s : %s' % (failure[0],failure[1])
   
    print "---- End of test results ---- "



def validateModule(module):
    tests.test_mod = module
    
    def injectModule(module):
        '''
        Injects the module that should be tested with mock objects for the 
        required modules. This is done 
        '''
        import mock.communication
        import mock.recentdata
        import mock.presist
        #import auth
    
        modules = {}
        modules['communication'] = mock.communication.Communication('yep')
        modules['recentdata']    = mock.recentdata.Data()
        #modules['presist']       = mock.presist.Presist('var','data')
            
        if (inspect.ismodule(module)):
            for coremodule in module.require:
                if not coremodule == 'presist':
                    vars(module)[coremodule] = modules[coremodule]
    
    
    def pretty(result):
        '''
        Getting the relevant information out of the 
        test result objects.
        '''
        prettyList = []
        for fail in result:
            method = fail[0]
            print fail, "\n\n"
            error  = " ".join(fail[-1:][0].split("\n")[-2:-1][0].split()[1:])
            prettyList.append([method.shortDescription(),error])

        return prettyList

    suite = unittest.TestLoader().loadTestsFromTestCase(tests.TestValidateModule)
    testResult = unittest.TextTestRunner(logger, verbosity=2).run(suite)
    
    testsRun   = testResult.testsRun
    successful = testsRun-(len(testResult.errors)+len(testResult.failures))
    
    errors   = pretty(testResult.errors)
    failures = pretty(testResult.failures)
    
    if len(failures) == 0:
        failures = None
    if len(errors) == 0:
        errors = None

    return (testResult.wasSuccessful(), (successful,testsRun), errors, failures)

import cmdtest2 as test_mod
import cmdtest as fail_mod
rtest1 = validateModule(test_mod)
rtest2 = validateModule(fail_mod)

printResults(rtest1[1][0],rtest1[1][1],rtest1[2],rtest1[3])
printResults(rtest2[1][0],rtest2[1][1],rtest2[2],rtest2[3])

#def printResults(successful,testsRun,errors,failures):

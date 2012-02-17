import unittest
import sys
import inspect
import testcases as tests
import pastebin
import config as cfg

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

def results(successful,testsRun,errors,failures):
    result = ''
    result += "%s/%s tests successful.\n" % (successful,testsRun)
    if errors:
        result += "Errors:\n"
        for error in errors:
           result += '%s : %s\n' % (error[0],error[1])
    
    if failures:
        result += "Failures:\n"
        for failure in failures:
            result += '%s : %s\n' % (failure[0],failure[1])
   
    result += "---- End of test results ---- \n"

    return result



def validateModule(module, verbose=False):
    
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
            error  = " ".join(fail[-1:][0].split("\n")[-2:-1][0].split()[1:])
            prettyList.append([method.shortDescription(),error])

        return prettyList

    injectModule(module)
    tests.test_mod = module

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

    pastebinUrl = None

    if verbose:
        result      = results(successful,testsRun, errors, failures)
        pastebinUrl = pastebin.submit(
                        result, 
                        paste_expire_date="10M",
                        paste_private=True,
                        paste_name="Error log.")
        

    return (testResult.wasSuccessful(), (successful,testsRun), errors, failures, pastebinUrl)

#import cmdtest2 as test_mod
#import cmdtest as fail_mod
#import fail
#rtest1 = validateModule(test_mod)
#rtest2 = validateModule(fail)
#rtest3 = validateModule(fail_mod)
#print rtest1
#print "\n"
#print rtest3

#printResults(rtest1[1][0],rtest1[1][1],rtest1[2],rtest1[3])
#printResults(rtest2[1][0],rtest2[1][1],rtest2[2],rtest2[3])
#
#def printResults(successful,testsRun,errors,failures):

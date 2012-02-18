import unittest
import sys
import inspect
import testcases as tests
import pastebin

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

# Creating a object that will take the place of
# standard output. This is done to avoid polution
# of the terminal.
logger = TestLogger()

def results(successful,testsRun,errors,failures):
    '''
    result() -> result log as a string

    Generating a result log as a long string. Makes the result
    look pretty. This is useful for when wanting to dump
    the result to a file, or for REST transfer. 

    '''

    result = ''
    result += "%s/%s tests successful.\n" % (successful, testsRun)
    
    if errors:
        result += "Errors:\n"
        for error in errors:
           result += '%s : %s\n' % (error[0], error[1])
    
    if failures:
        result += "Failures:\n"
        for failure in failures:
            result += '%s : %s\n' % (failure[0], failure[1])
   
    result += "---- End of test results ---- \n"

    return result



def validateModule(module, verbose=False):
    '''
    validateModule() -> test result

    Arguments:
    module  -- the brunobot module to test 
    verbose -- full error log pasted to pastebin

    Returns:
    Result from the unit test of a module,
    in the form of a dictionary with the keys:
    valid       -- true if all tests succeeded
    successful  -- number of successful tests
    tests       -- total number of tests
    errors      -- a list of errors [[test,error],..]
    failures    -- a list of failures [[test,failure],..]
    url         -- a URL to the error log if verbose is enabled

    '''
    

    def injectModule(module):
        '''
        injectModule() -> None

        Injects a brunbot module that should be tested 
        with mock objects for the required modules. 
        '''
        import mock.communication
        import mock.recentdata
        import mock.presist
        import mock.auth
    
        modules = {}
        modules['communication'] = mock.communication.Communication('test')
        modules['recentdata']    = mock.recentdata.Data()
        modules['auth']          = mock.auth.Auth()

        if (inspect.ismodule(module)):
            try:
                for coremodule in module.require:
                    if not coremodule == 'presist':
                        vars(module)[coremodule] = modules[coremodule]
            except:
                print ' ++ moduletest.injectModule() - no module.require'
    
    
    def pretty(result):
        '''
        pretty() -> list of tests run with results

        Getting the relevant information out of the 
        test result objects.
        '''

        prettyList = []
        for fail in result:
            method = fail[0]

            # The test object is a messy list of messages,
            # getting out the relevant information from the test.
            error  = " ".join(fail[-1:][0].split("\n")[-2:-1][0].split()[1:])
            prettyList.append([method.shortDescription(),error])

        return prettyList

    # Injecting mock objects so the main method of the module can be simulated 
    injectModule(module)

    tests.test_mod = module
    suite = unittest.TestLoader().loadTestsFromTestCase(tests.TestValidateModule)
    testResult = unittest.TextTestRunner(logger, verbosity=2).run(suite)
    
    # extracting information from the unit test
    testsRun    = testResult.testsRun
    successful  = testsRun - (len(testResult.errors) + len(testResult.failures))
    errors      = pretty(testResult.errors)
    failures    = pretty(testResult.failures)
    pastebinUrl = None
    
    if len(failures) == 0:
        failures = None
    if len(errors) == 0:
        errors = None

    if verbose:
        resultlog = results(successful, testsRun, errors, failures)
        pastebinUrl   = pastebin.submit(
                            resultlog, 
                            paste_expire_date="10M",
                            paste_private=True,
                            paste_name="Error log.")
   
    result = {'valid'     : testResult.wasSuccessful(),
             'successful' : successful,
             'tests'      : testsRun,
             'errors'     : errors,
             'failures'   : failures,
             'url'        : pastebinUrl}

    return result


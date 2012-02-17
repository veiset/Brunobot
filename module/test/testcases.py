import unittest
import sys
import inspect
test_mod = None

#class RunModule():
    
def runmodule(module, data):
    try:
        module.main(data)
        return [True,'Everything is ok']
    except Exception as error:
        error = str(error)
        if len(error) > 73:
            error = error[0:73] + "..."
        #print error
        return [False, error]



class TestValidateModule(unittest.TestCase):
    ''' Testing that all required variables are defined correctly '''

    def setUp(self):
        self.module = test_mod
        self.run_module = runmodule
        self.mock_cmd_data = {
                'type'    : 'cmd',
                'nick'    : 'vz',
                'ident'   : '~vz',
                'host'    : 'veiset.org',
                'channel' : '#brunobot',
                'cmd'     : None,  # defined in test
                'argv'    : None}  # defined in test
        self.mock_privmsg_data = {
                'type'    : 'privmsg',
                'nick'    : 'vz',
                'ident'   : '~vz',
                'host'    : 'veiset.org',
                'channel' : '#brunobot',
                'msg'     : None}  # defined in test  
                 

    # Required variables each module must contain.
    def testHasNameDefined(self):
        ''' Checking if 'name' is defined '''
        try: tmp = self.module.name
        except: self.assertTrue(False, "no name defined.")

    def testHasVersionDefined(self):
        ''' Checking if 'version' is defined '''
        try: tmp = self.module.version
        except: self.assertTrue(False,
                "no version defined.")

    def testHasRequireDefined(self):
        ''' Checking if 'require' is defined '''
        try: tmp = self.module.require
        except: self.assertTrue(True,
                "no required modules defined.")

    def testHasListenDefined(self):
        ''' Checking if 'listen' is defined '''
        try: tmp = self.module.listen
        except: self.assertTrue(False,
                "no action to listen on defined.")

    def testHasUsageDefined(self):
        ''' Checking if 'usage' is defined '''
        try: tmp = self.module.usage
        except: self.assertTrue(False,
                "no usage is defined.")

    def testHasDescriptionDefined(self):
        ''' Checking if 'description' is defined '''
        try: tmp = self.module.description
        except: self.assertTrue(False,
                "no description defined.")

    # End of required variables

    # Validating that the types of the defined variables
    # are correct.
    def testTypeNameIsString(self):
        ''' Checking if 'name' is of type string '''
        try: 
            tmp = self.module.name
            self.assertIsInstance(self.module.name,str,
                    "not of type string.")
            self.failIfEqual(len(self.module.name.strip()),0,
                    "of type string, but empty.")
        except:
            self.assertTrue(False,'not of type string')

    def testTypeVersionIsString(self):
        ''' Checking if 'version' is of type string '''
        try: 
            tmp = self.module.name
            self.assertIsInstance(self.module.version,str,
                "not of type string.")
            self.failIfEqual(len(self.module.version.strip()),0,
                "of type string, but empty.")
        except:
            self.assertTrue(False,'not of type string')

    def testTypeRequireIsList(self):
        ''' Checking if 'require' is of type list '''
        try: 
            tmp = self.module.name
            self.assertIsInstance(self.module.require,list,
                "not of type list.")
            self.failIfEqual(len(self.module.require),0,
                "of type list, but empty.")
        except:
            self.assertTrue(False,'not of type list')

    def testTypeListenIsList(self):
        ''' Checking if 'listen' is of type list '''
        try: 
            tmp = self.module.name
            self.assertIsInstance(self.module.listen,list,
                "not of type list.")
            self.failIfEqual(len(self.module.listen),0,
                "of type list, but empty.")
        except:
            self.assertTrue(False,'not of type list')

    def testTypeUsageIsString(self):
        ''' Checking if 'usage' is of type string '''
        try: 
            tmp = self.module.name
            self.assertIsInstance(self.module.usage,str,
                "not of type string.")
            self.failIfEqual(len(self.module.usage.strip()),0,
                "of type string, but empty.")
        except:
            self.assertTrue(False,'not of type string')

    def testTypeDescriptionIsString(self):
        ''' Checking if 'description' is of type string '''
        try: 
            tmp = self.module.name
            self.assertIsInstance(self.module.description,str,
                "not of type string.")
            self.failIfEqual(len(self.module.description.strip()),0,
                "of type string, but empty.")
        except:
            self.assertTrue(False,'not of type string')

    # End of validating Types

    # Checking that requirements are met if listens to certain modules
    def testListenToCmdAndHasCmdsDefined(self):
        ''' Checking if 'cmd' is defined '''
        if 'cmd' in self.module.listen:
            try:
                tmp = self.module.cmd
                self.failIfEqual(len(self.module.cmd),0,
                    "listens to cmd, but no commands defined.")
                self.assertIsInstance(self.module.cmd,list,
                    "cmd is not of type list")
            except:
                self.assertTrue(False,"listens to cmds, but 'cmd' is undefined.")


    # End of listen requirements

    # Checking that requirements are met if requires certain modules
    def testListenToPresistAndHasPresistDefined(self):
        ''' Checking if 'presist' is defined '''
        if 'presist' in self.module.require:
            try:
                tmp = self.module.presist
                self.failIfEqual(len(self.module.presist),0,
                    "listens to presist, but nothing to presist is defined..")
                self.assertIsInstance(self.module.presist,list,
                    "presist is not of type list")
            except:
                self.assertTrue(False,"listens to presist, but 'presist' is undefined.")
    # End of require module requirements

    def test_RunPrivmsgOfOneWord(self):
        ''' Run test [listen: privmsg, words: one] '''
        if 'privmsg' in self.module.listen:
            self.mock_privmsg_data['msg'] = 'word'
            runnable = self.run_module(self.module, self.mock_privmsg_data)
            if not runnable[0]:
                self.assertTrue(False,runnable[1])


    def test_RunPrivmsgWithMultipleWords(self):
        ''' Run test [listen: privmsg, words: multiple] '''
        if 'privmsg' in self.module.listen:
            self.mock_privmsg_data['msg'] = 'one two three words'
            runnable = self.run_module(self.module, self.mock_privmsg_data)
            if not runnable[0]:
                self.assertTrue(False,runnable[1])

    def test_RunAllCmdsDefinedWihtNoArgv(self):
        ''' Run test [listen: cmd, argv: None] '''
        if 'cmd' in self.module.listen:
            for cmd in self.module.cmd:
                self.mock_cmd_data['cmd']  = cmd
                self.mock_cmd_data['argv'] = None

                runnable = self.run_module(self.module, self.mock_cmd_data)
                if not runnable[0]:
                    self.assertTrue(False,runnable[1])

    def test_RunAllCmdsDefinedWihtStringArgv(self):
        ''' Run test [listen: cmd, argv: string] '''
        if 'cmd' in self.module.listen:
            for cmd in self.module.cmd:
                self.mock_cmd_data['cmd']  = cmd
                self.mock_cmd_data['argv'] = 'nothing'

                runnable = self.run_module(self.module, self.mock_cmd_data)
                if not runnable[0]:
                    self.assertTrue(False,runnable[1])


    def test_RunAllCmdsDefinedWihtIntegerArgv(self):
        ''' Run test [listen: cmd, argv: int(string)] '''
        if 'cmd' in self.module.listen:
            for cmd in self.module.cmd:
                self.mock_cmd_data['cmd']  = cmd
                self.mock_cmd_data['argv'] = '1'

                runnable = self.run_module(self.module, self.mock_cmd_data)
                if not runnable[0]:
                    self.assertTrue(False,runnable[1])





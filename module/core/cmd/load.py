import inspect

cmd         = ['load']
usage       = 'load <module>'
description = 'Loads a module.'

def main(modules, data):
    argv          = data['argv']
    channel       = data['channel']
    communication = modules.mcore['communication']

    nick  = data['nick']
    ident = data['ident']
    host  = data['host']

    if modules.mcore['auth'].isAdmin(nick,ident,host):
        if argv:
            name = data['argv'][0]
            verbose = False

            if len(argv) == 2:
                if argv[1] == '-v' or argv[1] == 'verbose' or argv[1] == 'report':
                    verbose = True
   
            communication.say(channel,'Running tests on module (might take some time)...')
    
            module, result = modules.dynamicLoader.load(argv[0],verbose)

            valid          = result['valid']
            successful     = result['successful']
            tests          = result['tests']
            errors         = result['errors']
            failures       = result['failures']
            url            = result['url']

            if inspect.ismodule(module) and valid:
                communication.say(channel,'%d/%d tests passed. Module %s loaded.' % (successful, tests, name))
            else:
                if url:
                    communication.say(channel,'Failed. Module %s not loaded. Error report: %s' % (successful, tests, name, url))
                else:
                    error_msg = ''
                    errorC = 0
                    failureC = 0
                    if errors and len(errors) > 0:
                        error_msg = " : ".join(errors[0])
                        errorC = len(errors)
                    if failures and len(failures) > 0:
                        error_msg = " : ".join(failures[0])
                        failureC = len(failures)

                    communication.say(channel,'Failed. Errors: %d  Failures: %d. (%s)' % (errorC, failureC, error_msg))
    else:
        communication.say(channel,'You aren\'t allowed to do that. (requires admin)')

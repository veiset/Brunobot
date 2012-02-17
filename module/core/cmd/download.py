cmd         = ['download']
usage       = 'download <url>'
description = 'Downloads and loads a module located on the web.'

def main(modules, data):
    argv          = data['argv']
    channel       = data['channel']
    communication = modules.mcore['communication']

    if argv:
        verbose = False
        if len(argv) == 2:
            if argv[1] == '-v' or argv[1] == 'verbose' or argv[1] == 'report':
                verbose = True

        communication.say(channel,'Running tests on module (might take some time)...')
        module, result = modules.dynamicLoader.download(argv[0],verbose)
        passed, status, errors, failures, url = result

        if module and passed:
            communication.say(channel,'%d/%d tests passed. Module %s loaded.' % (status[0],status[1],data['argv'][0]))
        else:
            if url:
                communication.say(channel,'Failed. %d/%d tests passed. Module %s not loaded. Error report: %s' % (status[0],status[1], data['argv'][0], url))
            else:
                communication.say(channel,'Failed. %d/%d tests passed. Module %s not loaded.' % (status[0],status[1], data['argv'][0]))



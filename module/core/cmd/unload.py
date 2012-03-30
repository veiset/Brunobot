cmd         = ['unload']
usage       = 'unload <module>'
description = 'Unloads a module.'

def main(modules, data):
    argv          = data['argv']
    channel       = data['channel']
    communication = modules.mcore['communication']

    if argv:
        unloaded, result = modules.moduleLoader.unload(argv[0])
        if unloaded: 
            communication.say(channel,'Module unloaded')
        else:
            communication.say(channel,'Failed to unload module: %s' % result)


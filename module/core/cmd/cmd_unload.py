cmd         = ['unload']
usage       = 'unload <module>'
description = 'Unloads a module.'

def main(modules, data):
    argv          = data['argv']
    channel       = data['channel']
    communication = modules.mcore['communication']

    if argv:
        msg = modules.dynamicLoader.unload(argv[0])
        communication.say(channel,msg[1])


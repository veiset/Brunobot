cmd         = ['load']
usage       = 'load <module>'
description = 'Loads a module.'

def main(modules, data):
    argv          = data['argv']
    channel       = data['channel']
    communication = modules.mcore['communication']

    if argv:
        msg = modules.dynamicLoader.load(argv[0])
        communication.say(channel,msg[1])

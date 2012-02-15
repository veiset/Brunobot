cmd         = ['reload']
usage       = 'reload <module>'
description = 'Reloads a module.'

def main(modules, data):
    argv          = data['argv']
    channel       = data['channel']
    communication = modules.mcore['communication']

    if argv:
        msg = modules.dynamicLoader.reloadm(argv[0])
        communication.say(channel,msg[1])



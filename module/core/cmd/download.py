cmd         = ['download']
usage       = 'download <url>'
description = 'Downloads and loads a module located on the web.'

def main(modules, data):
    argv          = data['argv']
    channel       = data['channel']
    communication = modules.mcore['communication']

    if argv:
        msg = modules.dynamicLoader.download(argv[0])
        communication.say(channel,msg[1])


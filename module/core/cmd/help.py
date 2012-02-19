cmd         = ['help']
usage       = 'help, help <module>'
description = 'Display help about the bot, or a specified module.'

def main(modules, data):
    argv          = data['argv']
    channel       = data['channel']
    communication = modules.mcore['communication']

    if argv:
        extra = modules.extra(argv[0])
        if (extra):
            try:
                author = "(author: %s)" % extra.author
            except:
                author = "(author: unknown)"

            communication.say(channel,"[%s %s %s]: " % (extra.name, extra.version, author))
            communication.say(channel," Description: %s" % extra.description)
            communication.say(channel," Usage:       %s" % extra.usage)
            if (modules.isCmd(extra)):
                communication.say(channel, " Listens to:  %s." % (", ".join(extra.cmd)))

        communication.say(channel, " Module %s not loaded as module.extra. Try: cmd <cmd> for help on core cmds." % argv[0])


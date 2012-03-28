cmd         = ['config','cfg']
usage       = 'config <set|rem|get|list> argv'
description = 'Edits the configuration file.'

def main(modules, data):

    argv    = data['argv']
    user    = data['nick']
    ident   = data['ident']
    host    = data['host']
    channel = data['channel']

    cfg             = modules.mcore['cfg']
    auth            = modules.mcore['auth']
    communication   = modules.mcore['communication'] 

    if argv:
        if auth.isOwner(user, ident, host):

            if argv[0] == 'get':
                if len(argv) == 3:
                    result = cfg.get(argv[1], argv[2])
                elif len(argv) == 2:
                    result = "[%s]" % (", ".join(cfg.list(argv[1])))

                communication.say(channel, result)

            elif argv[0] == 'set':
                if len(argv) == 3:
                    cfg.set(argv[1], argv[2])
                    result = "set variable '%s' in %s" % (argv[2], argv[1])

                elif len(argv) == 4:
                    cfg.set(argv[1], argv[2], argv[3])
                    result = "set variable '%s = %s' in %s" % (argv[2], argv[3], argv[1])
           
                communication.say(channel, result)
                print " .. config: %s " % result

            elif argv[0] == 'rem':
                if len(argv) == 3:
                    cfg.rem(argv[1], argv[2])
                    communication.say(channel, "unset value '%s' in %s" % (argv[2], argv[1]))
                    print " .. config: unset variable '%s' in %s" % (argv[2], argv[1])

cmd         = ['mod']
usage       = 'mod, mod <module> usage, mod <module> info'
description = 'Command to display information about loaded modules.'

def main(modules, data):
    '''
    Command to display information about loaded modules.
    '''
    argv          = data['argv']
    channel       = data['channel']
    communication = modules.mcore['communication']

    if not argv:
        core = modules.mcore.keys()
        core = ", ".join(core)
        extra = ""

        for mod in modules.mextra:
            extra += "%s %s, " % (mod.name, mod.version)
    
        if (len(extra)>1): 
            extra = extra[:-2]

        communication.say(channel,"Modules loaded: CORE[100] EXTRA[%s]" % extra) #(core,extra))
    else:
        core = modules.core(argv[0])

        if (core):
            communication.say(channel,"Module %s is a part of the CORE modules." % argv[0])
        else:
            extra = modules.extra(argv[0])
            
            if (extra):
                if len(argv) == 1:
                    extra_info = []
                    try: extra_info.append("author: %s" % extra.author)
                    except: extra_info.append("Author: uknown")
                    try: extra_info.append("url: %s" % extra.url)
                    except: extra_info.append("url: unknown")

                    communication.say(channel,  
                                      "Module (extra): %s %s REQUIRE[%s] LISTEN[%s] %s" % 
                                      (extra.name,
                                       extra.version,
                                       ", ".join(extra.require),
                                       ", ".join(extra.listen),
                                       ", ".join(extra_info)))

                elif argv[1] == 'description' or argv[1] == 'info':
                     communication.say(channel,
                                       "%s %s description: %s" % 
                                       (extra.name,
                                        extra.version,
                                        extra.description))
                
                elif argv[1] == 'usage' or argv[1] == 'use':
                    communication.say(channel,
                            "%s %s usage: %s" % \
                                    (extra.name,
                                     extra.version,
                                     extra.usage))

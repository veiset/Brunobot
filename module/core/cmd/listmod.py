cmd         = ['listmod','modlist']
usage       = 'listmod, modlist'
description = 'Lists all loaded and unloaded modules.'

import os

def main(modules, data):
    argv          = data['argv']
    channel       = data['channel']
    communication = modules.mcore['communication']

    extra = ""
    unloaded = []
    loaded = []
    
    for mod in modules.mextra:
        extra += "%s %s, " % (mod.name, mod.version)
        loaded.append(mod.name)
    
    if (len(extra)>1): 
        extra = extra[:-2]
        communication.say(channel,'Loaded: %s' % extra)
    else:
        communication.say(channel,'No modules loaded.')

    for m in os.listdir('module/extra'):
        if m[-3:] == '.py':
            unloaded.append(m[:-3])
    
    unloaded = list(set(unloaded).difference(set(loaded)))

    if len(unloaded)>0:
        communication.say(channel,'Unloaded: %s' % ", ".join(unloaded))

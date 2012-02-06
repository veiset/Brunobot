import sys
sys.path.append('../extra')
sys.path.append('../plugin')

require_modules = ['communication','connection'] # modules.mcore
listen_actions = ['privmsg','channel','system']

def validateModule(name):

    module = None
    version = None
    require = 0
    listen = 0

    author = None # Optional
    url = None # Optional

    # loading the module
    try: module = __import__(name)
    except: return 'Error: no such module; "%s".' % name

    # checking for module description
    try: version = module.version
    except: return 'Error: no version number found.'

    try: name = module.name
    except: return 'Error: no name is defined.'
    
    try:
        for r in module.require:
            for m in require_modules:
                if (r==m): require += 1
        if (require != len(module.require)): 
            return 'Error: could not require modules defined.'
    except: return 'Error: could not find requirements (require).'

    try:
        for l in module.listen:
            for a in listen_actions:
                if (l==a): listen += 1
        if (listen != len(module.listen)):
            return 'Error: could not determine actions to listen on.'
    except: return 'Error: could not find actions to listen on (listen).'

    # TODO: this should also check for method arguments
    if not (getattr(module,'main')):
        return 'Error: no main method ( def main(...) ).'

    return module

print validateModule('typofixer')

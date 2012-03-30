import ConfigParser
from module.core.output import out

class BrunobotConfig():
    cfgfile = 'config.conf'

    def __init__(self):
        self.config = ConfigParser.SafeConfigParser(allow_no_value=True)
        self.load()

    def get(self, section, variable):
        try:
            return self.config.get(section, variable)
        except:
            return None

    def set(self, section, variable, content=None):
        if content:
            self.config.set(section, variable, content)
        else:
            self.config.set(section, variable)

        self.save()

    def rem(self, section, variable):
        self.config.remove_option(section, variable)
        self.save()

    def load(self):
        self.config.read(self.cfgfile)

    def save(self):
        with open(self.cfgfile,'wb') as configfile:
            self.config.write(configfile)

    def list(self, section):
        return [key for (key,value) in self.config.items(section)]
    
    def printConfig(self):
        out.info("Configuration [connection]")
        out.info("       server:   %s (%s)" % (self.get('connection','server'),self.get('connection','port')))
        out.info("         nick:   %s (%s, %s)" % (self.get('connection','nick'),
                                 self.get('connection','ident'),
                                 self.get('connection','name')))
        out.info("     channels:   %s " % ", ".join(self.list('channels')))
        out.newline()
        out.info("Configuration [module]")
        out.info(" max_run_time:   %s" % (self.get('module','max_run_time')))
        out.info("       prefix:   %s" % (self.get('module','prefix')))
        for module in self.list('modules'):
            out.info("        module:   %s" % module)
        out.newline()
        out.info("Configuration [owners]")
        for owner in self.list('owners'):
            user, ident, host = owner.replace(' ','').split(',')
            out.info("        owner:   %s!%s@%s" % (user, ident, host))
        out.newline()


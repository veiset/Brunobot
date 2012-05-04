class Output():

    def __init__(self):
        import module.core.logger as log
        self.log = log.Logger()
        self.cfg = None 

    def info(self, string):
        print "> .. %s" % string

    def warn(self, string):
        self.warning(string)

    def warning(self, string):
        if self.cfg.get('log', 'error') in ['True','true','1','yes','on']:
            self.log.error('warning', string)
        print "> ++ %s" % string

    def error(self, string):
        if self.cfg.get('log', 'error') in ['True','true','1','yes','on']:
            self.log.error('error', string)
        print "> !! %s" % string

    def raw(self, string):
        print "%s" % string

    def newline(self):
        print ""

    def verbose(self, string):
        ''' do not display this currently '''
        # print " -- %s" % string

    def setcfg(self, cfg):
        self.cfg = cfg

out = Output()

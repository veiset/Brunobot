class Output():

    def __init__(self):
        self.cfg = None 

    def info(self, string):
        print "> .. %s" % string

    def warning(self, string):
        print "> ++ %s" % string

    def error(self, string):
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

import pickle
import StringIO

from module.core.output import out

class Presist():
    
    def __init__(self,extra,variables):
        self.module = extra
        self.variables = variables
        self.data = {}


    def load(self):
        try:
            datafile = open('presistence/%s_%s.dat' % (self.module.name, self.module.version),'r')
            self.data = pickle.load(datafile)
            datafile.close()
           
            for var in self.variables:
                try:
                    vars(self.module)[var] = self.data[var]
                except:
                    out.error('Failed to load presistence: %s [%s]' % (self.module.name, var))
        except:
            out.error('Could not load presistence data file')


    def save(self):
        try:
            for var in self.variables:
                self.data[var] = vars(self.module)[var]
           
            output = open('presistence/%s_%s.dat' % (self.module.name, self.module.version),'w')
            pickle.dump(self.data, output)
            output.close()
        except: ''' Could not save '''

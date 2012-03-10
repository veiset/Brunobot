import time
import multiprocessing
import threading

class ThreadModule(multiprocessing.Process):

    def stop(self):
        self.terminate()

    def setModule(self, w, data):
        self.module = w
        self.data = data
        self.time = time.time()

    def duration(self):
        return int(round((time.time() - self.time),0))

    def run(self):
        self.module.main(self.data)
        

class ThreadedManager(threading.Thread):
    proccesses = []
    running = True

    def stop(self):
        self.running = False

    def setConfig(self, config):
        self.cfg = config

    def setCommunication(self, communication):
        self.communication = communication

    def runModule(self, module, data):
        t = ThreadModule()

        t.setModule(module, data)
        self.proccesses.append(t)
        t.start()

    def run(self):

        while self.running:
            for proc in self.proccesses:
                duration = proc.duration()

                maxDuration = self.cfg.get('max_run_time',proc.module.name)
                try:
                    maxDuration = int(maxDuration)
                except:
                    try:
                        maxDuration = int(self.cfg.get('module','max_run_time'))
                    except:
                        maxDuration = 5

                
                if not proc.is_alive():
                    self.proccesses.remove(proc)

                elif duration >= maxDuration:
                    self.communication.say(proc.data['channel'], 
                            'Running of %s took too long (limit=%ds).' % (proc.module.name, maxDuration))
                    print ' ++ Running of %s took too long (limit=%ds)' % (proc.module.name, maxDuration)
                    proc.stop()
                    self.proccesses.remove(proc)

            time.sleep(0.3)


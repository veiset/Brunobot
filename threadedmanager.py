import time
import threading

class W():
    def main(self):
        while True:
            time.sleep(1)

class ThreadModule(threading.Thread):

    def __init__(self):
        super(ThreadModule, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def setModule(self, w):
        self.w = w
        self.time = time.time()

    def duration(self):
        return int(round((time.time() - self.time),0))

    def run(self):
        print "t started."
        self.w.main()
        

    def stopped(self):
        return self._stop.isSet()

module_max_duration = 4

class ThreadedModule(threading.Thread):
    proccesses = []
    running = True

    def stop(self):
        self.running = False


    def addModule(self, module):
        t = ThreadModule()
        t.setModule(module)
        self.proccesses.append(t)
        t.start()

    def run(self):
        print 'Threaded Module Manager started.'
        while self.running:
            for proc in self.proccesses:
                #print proc.duration()
                if proc.duration() >= module_max_duration:
                    proc.stop()
                if proc.stopped():
                    print "force removing t! %d of %d secs run." % (proc.duration(), module_max_duration)
                    self.proccesses.remove(proc)

            time.sleep(0.3)
            #print "%d threads running." % len(self.proccesses)

tc = ThreadedModule()
tc.start()

w = W()
tc.addModule(w)

time.sleep(1)
for x in range(10):

    w = W()
    tc.addModule(w)
    time.sleep(0.1)

import time
import threading

module_max_duration = 4


class ThreadModule(threading.Thread):

    def __init__(self):
        super(ThreadModule, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def setModule(self, w, data):
        self.module = w
        self.data = data
        self.time = time.time()

    def duration(self):
        return int(round((time.time() - self.time),0))

    def run(self):
        self.module.main(self.data)
        

    def stopped(self):
        return self._stop.isSet()


class ThreadedModule(threading.Thread):
    proccesses = []
    running = True
    message_queue = []

    def stop(self):
        self.running = False

    def addModule(self, module, data):
        t = ThreadModule()
        t.setModule(module, data)
        self.proccesses.append(t)
        t.start()

    def run(self):
        print 'Threaded Module Manager started.'
        while self.running:
            for proc in self.proccesses:
                duration = proc.duration()

                if duration == module_max_duration:
                    self.message_queue.append([proc.module,
                        "Forced remove. %d of %d secs run." % (duration, module_max_duration)])
                    proc.stop()

                if proc.stopped():
                    self.proccesses.remove(proc)
                print "\n"*2

            time.sleep(0.3)
            #print "%d threads running." % len(self.proccesses)
            for msg in self.message_queue:
                print msg


def test():
    ''' 
    Showing how to use the module, and a 
    test class representing module.extra.*
    '''
    class W():
        ''' Test class '''
        def main(self, data):
            while True:
                time.sleep(1)

    tc = ThreadedModule()
    tc.start()

    w = W()
    tc.addModule(w, {'abc' : 'test'})

    time.sleep(1)
    for x in range(3):

        w = W()
        tc.addModule(w, {'abc' : 'test'})
        time.sleep(0.1)


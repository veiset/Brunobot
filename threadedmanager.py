import time
import threading

module_max_duration = 5
prio_list = { }

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


class ThreadedManager(threading.Thread):
    proccesses = []
    running = True
    message_queue = []

    def stop(self):
        self.running = False

    def setCommunication(self, communication):
        self.communication = communication

    def runModule(self, module, data):
        t = ThreadModule()

        t.setModule(module, data)
        self.proccesses.append(t)
        t.start()

    def run(self):
        print 'Threaded Module Manager started.'
        while self.running:
            for proc in self.proccesses:
                duration = proc.duration()

                if proc.module.name in prio_list.keys():
                    max_duration = prio_list[proc.module.name]
                else:
                    max_duration = module_max_duration
                print duration, max_duration
                if duration >= max_duration:
                    self.communication.say(proc.data['channel'], 'Running took to long (limit=%ds).' % max_duration)
                    self.message_queue.append([proc.module,
                        "Forced remove. %d of %d secs run. [%s]" % (duration, max_duration, proc.name)])
                    proc.stop()

                if proc.stopped():
                    self.proccesses.remove(proc)

            time.sleep(0.3)


def test():
    ''' 
    Showing how to use the module, and a 
    test class representing module.extra.*
    '''
    class W():
        ''' Test class '''
        def __init__(self, name):
            self.name = name
        def main(self, data):
            self.name = data['name']
            while True:
                time.sleep(1)

    tc = ThreadedManager()
    tc.start()

    w = W('wiki')
    tc.addModule(w, {'name' : 'wiki'})

    time.sleep(1)
    for x in range(3):

        w = W('test')
        tc.addModule(w, {'name' : 'test'})
        time.sleep(0.1)


import time
import multiprocessing
import threading

from module.core.output import out

class ThreadModule(multiprocessing.Process):
    '''
    Processing is used so that the modules can be terminated,
    the problem with threads are that you cannot force termination
    of a module using threading. You can however terminate a 
    process, as described in the method stop(self).
    '''

    def stop(self):
        '''
        stop()

        Killing a process. This is done to avoid modules to be able
        to run forever. 
        
        docs.python.com (multiprocessing.terminate)
         Terminate the process. On Unix this is done using the SIGTERM 
         signal; on Windows TerminateProcess() is used. 

        Warning (docs.python.com multiprocessing.terminate):
         If this method is used when the associated process is 
         using a pipe or queue then the pipe or queue is liable to become
         corrupted and may become unusable by other process...
        '''
        
        self.terminate()

    def setModule(self, module, data):
        '''
        setModule(object, dictionary) 

        Preparing a process with the necessary data object and module,
        as these have to be defined before the process is started and
        cannot be defined as parameters in the run method.

        Keyword arguments:
        module   -- brunobot extra module with a module.main(data) method
        data     -- brunobot data dictionary object
        '''

        self.module = module
        self.data = data

    def duration(self):
        '''
        duration() -> integer

        Return the time in seconds since the running of the module started.
        '''
        return int(round((time.time() - self.time),0))

    def run(self):
        '''
        run()

        Method representing the process's activity.
        '''
        self.time = time.time()
        self.module.main(self.data)
        

class ThreadedManager(threading.Thread):
    '''
    Responsible for running and terminating brunobot extra modules.

    Threading is preferred over mutliprocessing because threading
    allow usage of share data after the thread is initialized, and
    the ThreadedManager needs to get information about new modules
    that should be run. 

    '''
    proccesses = []
    running = True

    def stop(self):
        '''
        stop()

        Stop running the ThreadedManager, used for stopping the
        thread when shutting down the bot.
        '''

        self.running = False

    def setConfig(self, config):
        '''
        setConfig()

        Prepare the ThreadedManager with the configuration
        file needed to determine how long each of the extra
        modules are allowed to run.

        Keyword arguments:
        config  -- brunobot configuration manager
        '''

        self.cfg = config

    def setCommunication(self, communication):
        '''
        setCommuncation()

        Prepare the ThreadedManager with the communication
        object used to relay messages to the IRC network socket.

        Keyword arguments:
        communication  -- brunobot connection object
        '''

        self.communication = communication

    def runModule(self, module, data):
        '''
        runModule()

        Creating a new process representation of a brunobot extra module.
        Passing the information needed for the process, then running the
        process.

        Keyword arguments:
        module   -- brunobot extra module with a module.main(data) method
        data     -- brunobot data dictionary object
        '''
        t = ThreadModule()
        t.setModule(module, data)
        self.proccesses.append(t)
        t.start()

    def run(self):
        '''
        run()

        Starting the process manager, invoked by self.start(). 
        '''
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
                    out.warn('Running of %s took too long (limit=%ds)' % (proc.module.name, maxDuration))
                    proc.stop()
                    self.proccesses.remove(proc)

            time.sleep(0.3)
        
        out.info('ThreadedManager threadmanager.ThreadedManager().run(self) terminated.')

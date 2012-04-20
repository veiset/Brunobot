''' Required for Brunobot module'''
author  = 'Russ Anderson, Vegard Veiset'
version = '1.0'
name    = 'listpid'
require = ['communication']
listen  = ['cmd']
cmd     = ['listpid','pid','pidlist']
usage   = 'pid \.py'
description = 'Displays processes matching a regular expression'

from subprocess import Popen, PIPE

def list_pids(grep):
    '''lists all PIDs which match a grep value'''
    proc = Popen(['ps aux | grep %s | grep -v grep' % (grep)], shell=True, stdin=PIPE, stdout=PIPE)
    value = proc.communicate()
 
    pids = []
    for output in value[0].split('\n'):
        if output:
            try:
                pids.append(output.split()[1])
            except:
                pass
 
    return pids

def main(data):
    if data['argv']: 
        communication.say(data['channel'], ", ".join(list_pids(data['argv'][0])))

'''Converted from brunobot v4'''

from re import findall, IGNORECASE
from decimal import Decimal, getcontext


'''Required for Brunobot module'''
version     = '1.0'
name        = 'duration'
author      = "Andreas Halle"
require     = ['communication']
listen      = ['cmd']
cmd         = ['dur', 'duration', 'time', 'seconds']
usage       = 'time 5000 seconds to hours minutes'
description = 'Convert a given representation of a duration to another one \
                                     using the time data from the grego \
                                     rian calendar.'

# Using the Gregorian Calendar, we have that:
millisecond = 1
second      = 1000 * millisecond
minute      = 60 * second
hour        = 60 * minute
day         = 24 * hour
week        = 7 * day
month       = 30.436875 * day # 4800 months in a 400 year
                              # cycle out of 146097 days.
year        = 365.2425 * day  # 146097 days in 400 years.
decade      = 10 * year
century     = 10 * decade
millennium  = 10 * century

nomenclature = [[millennium,  ['millennia', 'millennium', 'millenniums', \
                               'milleniums', 'millenia', 'millenium']],
                [century,     ['centuries', 'century', 'centurys']],
                [decade,      ['decades', 'decade']],
                [year,        ['years', 'year', 'yrs', 'yr', 'y', \
                               'annum', 'a']],
                [month,       ['months', 'month']],
                [week,        ['weeks', 'week', 'wks', 'wk', 'w']],
                [day,         ['days', 'day', 'dys', 'dy', 'd']],
                [hour,        ['hours', 'hour', 'hrs', 'hr', 'h']],
                [minute,      ['minutes', 'minute', 'mins', 'min', 'm']],
                [second,      ['seconds', 'second', 'secs', 'sec', 's']],
                [millisecond, ['milliseconds', 'millisecond', \
                               'millisecs', 'millisec', 'ms']]]
    
    

'''TODO: Add support for other calendars than just the gregorian one'''
'''TODO: Clean up from here and below.'''

def milliseconds(s):
    '''
    milliseconds(s) -> int
        
    Parse a string representating a duration of time
    and return the number of milliseconds it equals.
    
    Keyword arguments:
    string -- a string representing a duration of time
    '''
    terms = findall('[a-z]+', s, IGNORECASE)
    durations = findall('[0-9]*\.?[0-9]+', s)
        
    totalms = 0
        
    if len(terms) == len(durations): # Check if input is legal
        #Convert all the durations to milliseconds
        for a in range(len(durations)):
            try: # Parse integers
                durations[a] = int(durations[a])
            except: # Also parse floatinkg point numbers
                durations[a] = float(durations[a])
            
            # Convert them all to milliseconds
            for b in nomenclature:
                if terms[a] in b[1]:
                    totalms += durations[a] * b[0]
    return totalms

    
    
def duration(ms, s):
    '''
    duration(ms, s) -> string
    
    Keyword arguments:
    ms -- number of milliseconds
    s  -- string with terms to convert the milliseconds to
    '''
    # Use all the default terms if none is given
    terms = []
    if s == '':
        for a in nomenclature:
            terms.append(a[1][0])
    else:
        terms = findall('[a-z]+', s, IGNORECASE)
    
    output = ''
    for a in range(len(nomenclature)):
        for term in nomenclature[a][1]:
            for b in range(len(terms)):
                if term == terms[b]:
                    if b == len(terms)-1:
                        getcontext().prec = 6
                        newms = Decimal(str(ms)) / \
                                Decimal(str(nomenclature[a][0]))
                    else:
                        newms = int(ms / nomenclature[a][0])
                        ms %= int(nomenclature[a][0])
                    
                    if newms != 0:
                        if newms == 1:
                            output += ('%s %s ' % (newms, \
                                       nomenclature[a][1][1]))
                        else:
                            output += ('%s %s ' % (newms, \
                                       nomenclature[a][1][0]))
                    break
                
    return output.strip()



def dur(s):
    arr = s.split("to")
    ms = milliseconds(arr[0])
    if len(arr) == 1:
        terms = ''
    else:
        terms = arr[1]
    return duration(ms, terms)

def main(data):
    argv = data['argv']
    if argv:
        res = dur(" ".join(argv))

        if res:
            communication.say(data['channel'], '%s' % res)
        else:
            communication.say(data['channel'], 'Illegal parameter.')

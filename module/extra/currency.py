''' Required for Brunobot module'''
version = '1.0'
name    = 'currency'
require = ['communication']
listen  = ['cmd']
cmd     = ['cur', 'currency', 'cr']
usage   = 'currency 5 USD to NOK, cr 5 USD NOK'
description = 'Fetches the most current conversion rates and coverts amounts.'

import urllib2
url = 'http://download.finance.yahoo.com/d/quotes.csv?s=%s%s=X&f=sl1d1t1ba&e=.csv'

def parseInput(i):
    '''
    13 NOK in USD -> (13, NOK, USD)
    '''
    param = i.split(" ")
    if len(param) == 3:
        return param
    elif len(param) == 4:
        return param[0], param[1], param[3]

def getConversionRate(cur, cur2):
    f = urllib2.urlopen(url % (cur, cur2))
    data = f.read()
    try: 
        return float(data.split(",")[1])
    except:
        return None

def main(data):
    argv = data['argv']
    if argv:
        result = 0.0
        param = parseInput(" ".join(argv))
        if param:
            amount, cur1, cur2 = param
            rate = getConversionRate(cur1, cur2)
            if rate:
                communication.say(data['channel'], '%s %s to %s: %f' % (amount, cur1, cur2, float(amount)*rate))
            else:
                communication.say(data['channel'], 'Could not determine conversion rate.')
        else:
            communication.say(data['channel'], 'Incorrect input.')


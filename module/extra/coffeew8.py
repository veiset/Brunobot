''' Required for Brunobot module'''
version = '1.0'
name    = 'coffeew8'
require = ['communication']
listen  = ['cmd']
cmd     = ['coffee', 'coffeew8']
usage   = 'coffee'
description = 'Tells the state of the coffemaker at the reading hall of informatics (University of Bergen)'

import json
from urllib2 import urlopen

url = 'http://veiset.org:4567/api/last/1'
def main(data):
    state = json.dumps(urlopen(url).read())
    communication.say(data['channel'],'Coffee state: %s' % state)

#!/usr/bin/env python

'''
Yahoo Weather for brunobot
Created on 24. mar. 2012

@author: Russ Anderson
'''

from urllib2 import Request, quote, urlopen
from BeautifulSoup import BeautifulSoup

'''By default this module will NOT use Yahoo's GeoPlanet API. For a more complete
weather script with the ability to search for weather results in multiple fashions
(without the use of only a zip code), it is recommended that the GeoPlanet API is
used. To use the API, you must get an application id which can be obtained from 
the here:

	http://developer.yahoo.com/geo/geoplanet/

By changing the variable below to your Yahoo ID, you are enabling the use of the
GeoPlanet API with this script. Otherwise, this script will use the method to 
retrieve weather as demonstrated here:

    http://developer.yahoo.com/weather/archive.html'''
	

APP_ID		= 'DoQgQvfV34Gu6wfbhq7OiZY.tXBsnE8koKeElxiPkUbfXabYYzqcbF0f1.SuZE8WjTrRtb8N2mjU3.X4Afl8f5PBanQTaBI-' # change this to your Yahoo ID if you wish to use Yahoo's GeoPlanet API (read above).


'''Required for brunobot module'''
version     = '1.0'
name        = 'yahoo weather'
require     = ['communication']
listen      = ['cmd']
cmd         = ['wz','weather']
description = 'fetches weather information from yahoo'
usage       = 'wz 90210' 
author      = 'Russ Anderson'



'''Set required variables for script to work'''
CHNG_STR = '{\\??\\}'
USER_AGT = "Mozilla/5.0 (X11; Linux x86_64; rv:6.0) Gecko/20100101 Firefox/6.0"
BASE_URL = 'http://weather.yahooapis.com/forecastrss'
if APP_ID:
	FC_URL	= "http://where.yahooapis.com/v1/places.q('%s')?appid=%s" % (CHNG_STR, APP_ID)
else: 
	FC_URL	= '%s?p=%s' % (BASE_URL, CHNG_STR)

	
def search(s):
	'''search for weather information'''

	req = Request(FC_URL.replace(CHNG_STR, quote(s)))
	req.add_header('User-Agent', USER_AGT)
				 
	results = urlopen(req).read()

	if APP_ID:
		'''using yahoo's geoplanet api, grab woeid first then fetch weather information'''
		woeid = getWoeid(results)
		
		if not woeid:
			return 'Search for "%s" displayed no results.' % (s)
		
		else:
			'''found a woeid, grab weather information'''
			
			req = Request("%s?w=%s" % (BASE_URL, woeid))
			req.add_header('User-Agent', USER_AGT)
			results = urlopen(req).read()
			return getForecast(s, results)
	else:
		'''a yahoo application id was not provided, search by zip code
		   use a seperate function for this to reduce redundancy if an
		   application id was provided but search results found no id'''
		   
		req = Request(FC_URL.replace(CHNG_STR, quote(s)))
		req.add_header('User-Agent', USER_AGT)
		results = urlopen(req).read()
		return getForecast(s, results)
		
		
		
def getForecast(s, results):
		soup = BeautifulSoup(results)
		results = soup.find("title").contents
		if "error" not in results[0].lower():
			weather = []
			weather.append("\002%s\002" % (results[0].replace('Yahoo!', '')))
			for x in soup.findAll('yweather:condition'):
				if x["text"]: weather.append("\n\002%s\002 @" % (x["text"]))
				if x["temp"]: weather.append("\002%sF\002" % (x["temp"]))
				if x["date"]: weather.append("[updated: %s]" % (x["date"]))
				
			for x in soup.findAll('yweather:forecast', { 'day' : True }):
				if x["day"]: weather.append('\n[%s' % (x["day"]))
				if x["date"]: weather.append('%s]' % (x["date"]))
				if x["low"]: weather.append('Low: %sF' % (x["low"]))
				if x["high"]: weather.append('High: %sF ->' % (x["high"]))
				if x["text"]: weather.append('%s' % (x["text"]))
		
			return " ".join(weather)
		else:
			return 'Search for "%s" displayed no results.' % (s)
				
def getWoeid(results):
	'''fetch the WOEID number of the provided area which is then used to grab forecast information'''
	if 'yahoo:total="0"' not in results:
		soup = BeautifulSoup(results)
		del results
		results = soup.find("woeid").contents
		if results:
			return str(results[0])

		else: 
			return False
	else: return False
	
	
	
def main(data):
	argv = data['argv']
	if argv:
		argv = " ".join(argv)
		result = search(argv)
		if (result):
			communication.say(data['channel'],result)
			
#!/usr/bin/env python

'''
TLD Origin Checker
Created on 26. mar. 2012

@author: Russ Anderson
'''

'''Required for brunobot module'''
version     = '1.0'
name        = 'TLD Lookup'
require     = ['communication']
listen      = ['cmd']
cmd         = ['tld']
description = "converts a domain name to it's origin"
usage       = 'tld .com' 
author      = 'Russ Anderson'


TLD_dict = { ".aero" : "Air-Transport Industry.", ".asia" : "Asia-Pacific", ".biz" : "Business", ".cat" : "Catalan",
             ".com" : "Commerical", ".coop" : "Cooperatives", ".edu" : "Educational", ".gov" : "U.S. Governmental",
             ".info" : "Information", ".int" : "International Organizations", ".jobs" : "Companies", ".mil" : "U.S. Military",
             ".mobi" : "Mobile Devices", ".museum" : "Museums", ".name" : "Individuals", ".net" : "Network", ".org" : "Organization",
             ".pro" : "Professions", ".tel" : "Internet Communication Services", ".travel" : "Travel and Tourism",
             ".ac" : "Ascension Island", ".ad" : "Andorra", ".ae" : "United Arab Emirates", ".af" : "Afganistan",
             ".ag" : "Antigua and Barbuda", ".ai" : "Anguilla", ".al" : "Albania", ".am" : "Armenia", ".an" : "Netherlands Antilles",
             ".ao" : "Angola", ".aq" : "Antarctica", ".ar" : "Argentina", ".as" : "American Samoa", ".at" : "Austria",
             ".au" : "Australia including Ashmore, Cartier Islands, and Coral Sea Islands", ".aw" : "Aruba", ".ax" : "Aland",
             ".az" : "Azerbaijan", ".ba" : "Bosnia and Herzegovina", ".bb" : "Barbados", ".bd" : "Bangladesh", ".be" : "Belgium",
             ".bf" : "Burkina Faso", ".bg" : "Burlgaria", ".bh" : "Bahrain", ".bi" : "Burundi", ".bm" : "Bermuda",
             ".bn" : "Brunei Darussalam", ".bo" : "Boliva", ".br" : "Brazil", ".bs" : "Bahamas", ".bt" : "Bhutan",
             ".bv" : "Bouvet Island", ".bw" : "Botswana", ".by" : "Belarus", ".bz" : "Belize", ".ca" : "Canada",
             ".cc" : "Cocos Islands", ".cd" : "Democratic Republic of the Congo Formerly Zaire", ".cf" : "Central African Republic",
             ".cg" : "Republic of the Congo", ".ch" : "Switzerland",
             ".ci" : "Cote d'Ivoire", ".ck" : "Cook Islands", ".cl" : "Chile", ".cm" : "Cameroon", ".cn" : "People's Republic of China",
             ".co" : "Colombia", ".cr" : "Costa Rica", ".cu" : "Cuba", ".cv" : "Cape Verde", ".cx" : "Christmas Island",
             ".cy" : "Cyprus", ".cz" : "Czech Republic", ".de" : "Germany (Deutschland)", ".dj" : "Djibouti", ".dk" : "Denmark",
             ".dm" : "Dominica", ".do" : "Dominican Republic", ".dz" : "Algeria (Dzayer)", ".ec" : "Ecuador", ".ee" : "Estonia (Eesti)",
             ".eg" : "Egypt", ".er" : "Eritrea", ".es" : "Spain", ".et" : "Ethiopia", ".eu" : "European Union",
             ".fi" : "Finland", ".fj" : "Fiji", ".fk" : "Falkland Islands", ".fm" : "Federated States of Micronesia",
             ".fo" : "Faroe Islands", ".fr" : "France", ".ga" : "Gabon", ".gb" : "United Kingdom", ".gb" : "Grenada",
             ".ge" : "Georgia (Country)", ".gf" : "French Guiana", ".gg" : "Guernsey", ".gh" : "Ghana", ".gi" : "Gibraltar",
             ".gl" : "Greenland", ".gm" : "The Gambia", ".gn" : "Guinea", ".gp" : "Guadeloupe", ".gq" : "Equatorial Guinea",
             ".gr" : "Greece", ".gs" : "South Georgia and the South Sandwich Islands", ".gt" : "Guatemala", ".gu" : "Guam",
             ".gw" : "Guinea-Bissau", ".gy" : "Guyana", ".hk" : "Hong Kong", ".hm" : "Heard Island and McDonald Islands",
             ".hn" : "Honduras", ".hr" : "Croatia (Hrvatska)", ".ht" : "Haiti", ".hu" : "Hungary", ".id" : "Indoesia",
             ".ie" : "Republic of Ireland", ".il" : "Israel", ".im" : "Isle of Man", ".in" : "India", ".io" : "British Indian Ocean Territory",
             ".iq" : "Iraq", ".is" : "Iceland", ".ir" : "Iran", ".it" : "Italy", ".je" : "Jersey", ".jm" : "Jamaica",
             ".jo" : "Jordan", ".jp" : "Japan", ".ke" : "kenya", ".kg" : "Kyrgyzstan", ".kh" : "Cambodia",
             ".ki" : "kiribati", ".km" : "Comoros", ".kn" : "Saint Kitts and Nevis", ".kp" : "Democratic People's of Korea",
             ".kr" : "Republic of Korea", ".kw" : "Kuwait", ".ky" : "Cayman Islands", ".kz" : "Kazakhstan", ".la" : "Laos",
             ".lb" : "Lebanon", ".lc" : "Saint Lucia", ".li" : "Liechtenstein", ".lk" : "Sri Lanka", ".lr" : "Liberia", ".ls" : "Lesotho",
             ".lt" : "Lithuania", ".lu" : "Luxembourg", ".lv" : "Latvia", ".ly" : "Libya", ".ma" : "Morocco", ".mc" : "Monaco",
             ".md" : "Moldova", ".me" : "Montenegro", ".mg" : "Madagascar", ".mh" : "Marshall Islands",
             ".mk" : "Republic of Macedonia the former Yugoslav Republic of Macedonia", ".ml" : "Mali", ".mm" : "Myanmar",
             ".mn" : "Mongolia", ".mo" : "Macau", ".mp" : "Northern Mariana Islands", ".mq" : "Martinique", ".mr" : "Maurtania",
             ".ms" : "Montserrat", ".mt" : "Malta", ".mu" : "Mauritius", ".mv" : "Maldives", ".mw" : "Malawi", ".mx" : "Mexico",
             ".my" : "Malaysia", ".mz" : "Mozambique", ".na" : "Namibia", ".nc" : "New Caledonia", ".ne" : "Niger", ".nf" : "Norfolk Island",
             ".ng" : "Nigeria", ".ni" : "Nicaragua", ".nl" : "Netherlands", ".no" : "Norway", ".np" : "Nepal", ".nr" : "Nauru",
             ".nu" : "Niue", ".nz" : "New Zealand", ".om" : "Oman", ".pa" : "Panama", ".pe" : "Peru", ".pf" : "French Polynesia with Clipperton Island",
             ".pg" : "Papua New Guinea", ".ph" : "Philippines", ".pk" : "Pakistan", ".pl" : "Poland", ".pm" : "Saint-Pierre and Miquelon",
             ".pn" : "Pitcairn Islands", ".pr" : "Puerto Rico", ".ps" : "Palestinian Territories", ".pt" : "Portugal", ".pw" : "Palau",
             ".py" : "Paraguay", ".qa" : "Qatar", ".re" : "Reunion", ".ro" : "Romania", ".rs" : "Serbia", ".ru" : "Russia",
             ".rw" : "Rwanda", ".sa" : "Saudi Arabia", ".sb" : "Solomon Islands", ".sc" : "Seychelles", ".sd" : "Sudan", ".se" : "Sweden",
             ".sg" : "Singapore", ".sh" : "Saint Helena", ".si" : "Slovenia", ".sj" : "Svalbard and Jan Mayen Islands",
             ".sk" : "Slovakia", ".sl" : "Sierra Leone", ".sm" : "San Marino", ".sn" : "Senegal", ".so" : "Somalia",
             ".sr" : "Suriname", ".st" : "Sao Tome and Principe", ".su" : "Former Soviet Union", ".sv" : "El Salvador", ".sy" : "Syria",
             ".sz" : "Swaziland", ".tc" : "Turks and Caicos Island", ".td" : "Chad", ".tf" : "French Southern and Antarctic Lands",
             ".tg" : "Togo", ".th" : "Thailand", ".tj" : "Tajikistan", ".tk" : "Tokelau", ".tl" : "East Timor", ".tm" : "Turkmenistan",
             ".tn" : "Tunisia", ".to" : "Tonga", ".tp" : "East Timor", ".tr" : "Turkey", ".tt" : "Trinidad and Tobago", 
             ".tv" : "Tuvalu. Also used by Television Broadcasters.", ".tw" : "Republic of China (Taiwan)", ".tz" : "Tanzania",
             ".ua" : "Ukraine", ".ug" : "Uganda", ".uk" : "United Kingdom", ".us" : "United States of America", ".uy" : "Uruguay",
             ".uz" : "Uzbekistan", ".va" : "Vatican City", ".vc" : "Saint Vincent and the Grenadines", ".ve" : "Venezuela",
             ".vg" : "British Virgin Islands", ".vi" : "U.S. Virgin Islands", ".vn" : "Vietnam", ".vu" : "Vanuatu",
             ".wf" : "Wallis and Futuna", ".ws" : "Samoa", ".ye" : "Yemen", ".yt" : "Mayotte", ".yu" : "Yugoslavi, Now used for Serbia and Montenegro",
             ".za" : "South Africa (Zuid-Afrika)", ".zm" : "Zabmbia", ".zw" : "Zimbabwe", ".arpa" : "Address and Routing Parameter Area.", ".xxx" : "8====D ({})" }
             
             
def search(params):
	try:
		results = "%s -> %s" % (params, TLD_dict[params])
	except:
		results = "%s not found." % (params)
	return results
	
             
def main(data):
	argv = data['argv']
	if argv:
		argv = " ".join(argv)
		result = search(argv)
		if (result):
			communication.say(data['channel'],result)
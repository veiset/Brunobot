# This Python file uses the following encoding: utf-8
'''
brunobot v5

@author: Andreas Halle

These specifications are mainly taken from RFC 1459 and RFC 2812.
RFC 1459: http://www.irchelp.org/irchelp/text/rfc1459.txt
RFC 2812: http://www.irchelp.org/irchelp/rfc/rfc2812.txt
'''

'''
From RFC 1459:

Channels names are strings (beginning with a '&' or '#' character) of length
up to 200 characters. Apart from the the requirement that the first character
being either '&' or '#'; the only restriction on a channel name is that it
may not contain any spaces (' '), a control G (^G or ASCII 7), or a comma (','
which is used as a list item separator by the protocol).
'''
CHAN = '[&\#][^ ,\x07]{1,200}'


'''
From RFC 2812:

nickname   =  ( letter / special ) *8( letter / digit / special / "-" )

letter     =  %x41-5A / %x61-7A       ; A-Z / a-z
digit      =  %x30-39                 ; 0-9
special    =  %x5B-60 / %x7B-7D
              ; "[", "]", "\", "`", "_", "^", "{", "|", "}"
'''                   
NICK = '[A-Za-z\[\]\\`_\^\{\|\}][A-Za-z0-9\[\]\\`_\^\{\|\}\-]{0,8}'

'''
From RFC 2812:

user       =  1*( %x01-09 / %x0B-0C / %x0E-1F / %x21-3F / %x41-FF )
                ; any octet except NUL, CR, LF, " " and "@"
'''
IDENT = '[^\r\n@ ]+'


'''
:nick!ident@host PRIVMSG channel :text
'''
MSG = ':(%s)!(%s)@([A-Za-z0-9\-\./]+) PRIVMSG (%s) :(.*)' % (NICK, IDENT, CHAN)

'''
From RFC 2812:

message    =  [ ":" prefix SPACE ] command [ params ] crlf
prefix     =  servername / ( nickname [ [ "!" user ] "@" host ] )
command    =  1*letter / 3digit
params     =  *14( SPACE middle ) [ SPACE ":" trailing ]
           =/ 14( SPACE middle ) [ SPACE [ ":" ] trailing ]
           
nospcrlfcl =  %x01-09 / %x0B-0C / %x0E-1F / %x21-39 / %x3B-FF
                ; any octet except NUL, CR, LF, " " and ":"
                
middle     =  nospcrlfcl *( ":" / nospcrlfcl )
trailing   =  *( ":" / " " / nospcrlfcl )

SPACE      =  %x20        ; space character
crlf       =  %x0D %x0A   ; "carriage return" "linefeed"

target     =  nickname / server
msgtarget  =  msgto *( "," msgto )
msgto      =  channel / ( user [ "%" host ] "@" servername )
msgto      =/ ( user "%" host ) / targetmask
msgto      =/ nickname / ( nickname "!" user "@" host )
channel    =  ( "#" / "+" / ( "!" channelid ) / "&" ) chanstring
              [ ":" chanstring ]
servername =  hostname
host       =  hostname / hostaddr
hostname   =  shortname *( "." shortname )
shortname  =  ( letter / digit ) *( letter / digit / "-" )
              *( letter / digit )
                ; as specified in RFC 1123 [HNAME]
hostaddr   =  ip4addr / ip6addr
ip4addr    =  1*3digit "." 1*3digit "." 1*3digit "." 1*3digit
ip6addr    =  1*hexdigit 7( ":" 1*hexdigit )
ip6addr    =/ "0:0:0:0:0:" ( "0" / "FFFF" ) ":" ip4addr
nickname   =  ( letter / special ) *8( letter / digit / special / "-" )
targetmask =  ( "$" / "#" ) mask
                ; see details on allowed masks in section 3.3.1
chanstring =  %x01-07 / %x08-09 / %x0B-0C / %x0E-1F / %x21-2B
chanstring =/ %x2D-39 / %x3B-FF
                ; any octet except NUL, BELL, CR, LF, " ", "," and ":"
channelid  = 5( %x41-5A / digit )   ; 5( A-Z / 0-9 )

user       =  1*( %x01-09 / %x0B-0C / %x0E-1F / %x21-3F / %x41-FF )
                ; any octet except NUL, CR, LF, " " and "@"
letter     =  %x41-5A / %x61-7A       ; A-Z / a-z
digit      =  %x30-39                 ; 0-9
hexdigit   =  digit / "A" / "B" / "C" / "D" / "E" / "F"
special    =  %x5B-60 / %x7B-7D
'''

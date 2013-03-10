from pyric.events import Event

user    = ('vz', '~vz', 'veiset.org')
server  = 'irc.homelien.no'
channel = '#brunobot'

event_001 = Event(
    {
        'msg': 'Welcome to the EFNet Internet Relay Chat Network vzbot',
        'user': None,
        'type': '001',
        'server': server,
        'channel': None,
        'recipient': None
    }
)
event_002 = Event(
    {
        'msg': 'Your host is irc.homelien.no[195.159.0.90/6667]running version ircd-ratbox-2.2.6',
        'user': None,
        'type': '002',
        'server': server,
        'channel': None,
        'recipient': None
    }
)
event_003 = Event(
    {
        'msg': 'This server was created Mon Sep 24 2007 at 13:54:13 CEST',
        'user': None,
        'type': '003',
        'server': server,
        'channel': None,
        'recipient': None
    }
)
event_004 = Event(
    {
        'msg': None,
        'user': None,
        'type': '004',
        'server': server,
        'channel': None,
        'recipient': None
    }
)
event_005 = Event(
    {
        'msg': '50 PREFIX=(ov)@+ MAXLIST=beI:100 NETWORK=EFNet MODES=4 STATUSMSG=@+ KNOCK CALLERID=g :are supported by this server',
        'user': None,
        'type': '005',
        'server': server,
        'channel': None,
        'recipient': None
    }
)
event_250 = Event(
    {
        'msg': 'Highest connection count: 1550 (1549 clients) (52361 connections received)',
        'user': None,
        'type': '250',
        'server': server,
        'channel': None,
        'recipient': None
    }
)
event_251 = Event(
    {
        'msg': 'There are 7898 users and 26915 invisible on 38 servers',
        'user': None,
        'type': '251',
        'server': server,
        'channel': None,
        'recipient': None
    }
)
event_252 = Event(
    {
        'msg': 'IRC Operators online',
        'user': None,
        'type': '252',
        'server': server,
        'channel': None,
        'recipient': None
    }
)
event_254 = Event(
    {
        'msg': 'channels formed',
        'user': None,
        'type': '254',
        'server': server,
        'channel': None,
        'recipient': None
    }
)
event_255 = Event(
    {
        'msg': 'I have 1210 clients and 1 servers',
        'user': None,
        'type': '255',
        'server': server,
        'channel': None,
        'recipient': None
    }
)
event_265 = Event(
    {
        'msg': 'Current local users 1210, max 1549',
        'user': None,
        'type': '265',
        'server': server,
        'channel': None,
        'recipient': None
    }
)
event_266 = Event(
    {
        'msg': 'Current global users 34813, max 36268',
        'user': None,
        'type': '266',
        'server': server,
        'channel': None,
        'recipient': None
    }
)
event_322 = Event(
    {
        'msg': 'Let us all have great fun! :D',
        'user': None,
        'type': '332',
        'server': server,
        'channel': channel,
        'recipient': None,
    }
)
event_privmsg = Event(
    {
        'msg': 'this is a test', 
        'user': user,
        'type': 'PRIVMSG', 
        'server': None, 
        'channel': channel, 
        'recipient': channel
    }
)
event_ping = Event(
    {
        'msg': server, 
        'user': None, 
        'type': 'PING', 
        'server': None, 
        'channel': None, 
        'recipient': None
    }
)
event_mode = Event(
    {
        'msg': '+v vzbot', 
        'user': user,
        'type': 'MODE', 
        'server': None, 
        'channel': channel, 
        'recipient': None
    }
)
event_part = Event(
    {
        'msg': channel,
        'user': user,
        'type': 'PART',
        'server': None,
        'channel': channel,
        'recipient': None
    }
)
event_join = Event(
    {
        'msg': channel,
        'user': user,
        'type': 'JOIN',
        'server': None,
        'channel': channel,
        'recipient': None
    }
)

event_nick = Event(
    {
        'msg': 'vznew', 
        'type': 'NICK', 
        'server': None, 
        'user': user,
        'channel': None, 
        'recipient': None
    }
)

import sqlite3
import time
class Logger():
    '''
    Module for managing databases used by the brunobot framework.

    error.db   is used for stroing error and warning messages
               caused by the bot (e.g, a module failing to
               execute or the bot crashing).

    irc.db     is used to store all incomming data from the 
               irc server. 

    bruno.db   is used to store information about events the
               brunobot executes (e.g, runs a module, joins
               or parts a channel, connect to the network...)
    '''

    def __init__(self):
        ''' 
        Creates the databases if they do not exist. 
        '''
        self.createDB('data/error.db',
                      """CREATE TABLE IF NOT EXISTS error 
                         (date   integer, 
                          type   text, 
                          msg    text)""")

        self.createDB('data/irc.db',  
                      """CREATE TABLE IF NOT EXISTS log
                         (date   integer, 
                          nick   text, 
                          ident  text, 
                          host   text, 
                          event  text,
                          targer text,
                          data   text)""")

        self.createDB('data/bruno.db',  
                      """CREATE TABLE IF NOT EXISTS event 
                         (date   integer,
                          event  text,
                          data   text)""")

    def createDB(self, database, query):
        '''
        createDB(string, string) 

        Keyword arguments:
        database -- sqlite3 database location
        query    -- sqlite3 database create query
        '''
        db = sqlite3.connect(database)
        c = db.cursor()
        c.execute(query)
        db.commit()
        db.close()

    def error(self, level, message, time=time.time()):
        '''
        error(string, string)

        Keyword arguments:
        level    -- severity level: error/warning/info
        message  -- error/warning message
        '''
        db = sqlite3.connect('data/error.db')
        c = db.cursor()
        c.execute("INSERT INTO error VALUES (?, ?, ?)", (int(time), level, message))
        db.commit()
        db.close()

    def irc(self, nick, ident, host, event, target, data, time=time.time()):
        '''
        irc(string, string, string, string, string, string, string)

        Keyword arguments:
        nick    --  irc nickname
        ident   --  irc ident
        host    --  irc hostname
        event   --  irc event-type (e.g: privmsg/action/ctcp)
        target  --  irc target (e.g: #brunobot/bruno)
        data    --  data (e.g: message)
        '''
        db = sqlite3.connect('data/irc.db')
        c = db.cursor()
        c.execute("INSERT INTO log VALUES (?, ?, ?, ?, ?, ?, ?)", (int(time), nick, ident, host, event, target, data))
        db.commit()
        db.close()
    
    def bruno(self, event, data, time=time.time()):
        '''
        bruno(string, string)

        Keyword arguments:
        event   -- event type
        data    -- data of the event
        '''
        db = sqlite3.connect('data/bruno.db')
        c = db.cursor()
        c.execute("INSERT INTO event VALUES (?, ?, ?)", (int(time), event, data))
        db.commit()
        db.close()

#log = Logger()
#log.error('error', 'bot crashed')
#log.bruno('module_run', 'urltitle')
#log.irc('vz', 'vz', 'veiset.org', 'privmsg', '#brunobot', 'hello')

#db = sqlite3.connect('data/error.db')
#c = db.cursor()
#
#for row in c.execute('SELECT * FROM error ORDER BY date'):
#    print row
#
#db.close()



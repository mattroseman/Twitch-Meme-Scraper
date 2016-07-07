import MySQLdb as mdb
import sys
from threading import Thread

"""
Script to get latest chat messages from a twitch stream and add them to a file
arguments: url of twitch site
using:
    http://code.activestate.com/recipes/299411-connect-to-an-irc-server-and-store-messages-into-a/
"""

import sys, socket, string, datetime

class DataBot(Thread):

    # make the cursor a dictionary
    # can now reference rows as a dictions
    # print row['id']

    SERVER = 'irc.twitch.tv'
    PORT = 6667
    NICKNAME = 'mroseman_bot'
    PASSWORD = 'oauth:glz9hskrj3umqvzix5876fc6fdj0u9'
    
    BUFFER_SIZE = 1024
    

    def __init__(self, channel, channel_id):
        Thread.__init__(self)
        self.daemon = True
    #  open socket
        # self.IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con = mdb.connect('localhost', 'root', 'lolipop123', 'twitch_mining');
        self.con.autocommit(True)
        self.cur = self.con.cursor(mdb.cursors.DictCursor)

        self.IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.channel_id = channel_id
        self.irc_conn()
        self.login(self.NICKNAME, self.PASSWORD)
        self.join(channel)

        print "succesfully joined channel"
        self.start()
    
    #  open connection
    def irc_conn(self):
        self.IRC.connect((self.SERVER, self.PORT))
    
    #  send data through socket
    def send_data(self, command):
        self.IRC.send(command + '\r\n')
    
    #  get data through socket
    def get_data(self):
        return self.IRC.recv(self.BUFFER_SIZE)
    
    #  join a channel
    def join(self, channel):
        self.send_data("JOIN %s" % channel)
    
    #  send login data
    def login(self, nickname, password=None):
        self.send_data("PASS %s" % password)
        self.send_data("NICK %s" % nickname)
    
    
    def insert_message(self, username, msg, timestamp):
        self.cur.execute("INSERT INTO messages(stream_id, user, message, timestamp) VALUES(%s, %s, %s, %s)", (self.channel_id, username, msg, timestamp))
        # optionally print the messages
        # print timestamp, username, msg

    def run(self):
        readbuffer = ""

        while 1:
            readbuffer=readbuffer + self.get_data()
            temp = string.split(readbuffer, '\n')
            readbuffer = temp.pop()
    
            for line in temp:
                line = string.rstrip(line)
                line = string.split(line)
                
                if (line[0] == 'PING'):
                    self.send_data('PONG %s' % line[1])
                if (line[1] == 'PRIVMSG'):
                    username = line[0].replace(":", "",  1)
                    index = line[0].find('!')
                    username = username[:index - 1]
    
                    timestamp = datetime.datetime.utcnow().strftime("%b %d %H:%M:%S %Y")
                    msg = ' '.join(line[3:])[1:]

                    self.insert_message(username, msg, timestamp)

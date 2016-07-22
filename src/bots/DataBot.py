import MySQLdb as mdb
from threading import Thread
import sys, socket, string, datetime

"""
Script to get latest chat messages from a twitch stream and add them to database 
Implements Thread interface

using:
    http://code.activestate.com/recipes/299411-connect-to-an-irc-server-and-store-messages-into-a/
"""


class DataBot(Thread):

    # DO NOT CHANGE
    SERVER = 'irc.twitch.tv'
    PORT = 6667
    NICKNAME = 'mroseman_bot'
    PASSWORD = 'oauth:glz9hskrj3umqvzix5876fc6fdj0u9'
    
    BUFFER_SIZE = 1024

    
    # default constructor
    def __init__(self, channel, channel_id):
        # initialize threading
        Thread.__init__(self)
        self.daemon = True
        # connect to DB
        # TODO handle this more securely
        # self.con = mdb.connect('localhost', 'root', 'lolipop123', 'twitch_mining');
        # self.con.autocommit(True)
        # self.con.ping(True)
        # self.cur = self.con.cursor(mdb.cursors.DictCursor)

        # create IRC socket object 
        self.IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # join the channel and authenticate
        self.channel_id = channel_id
        self.irc_conn()
        self.login(self.NICKNAME, self.PASSWORD)
        self.join(channel)

        print ("succesfully joined channel " + channel)
        # execute thread
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
    
    
    # insert to database
    def insert_message(self, username, msg):
        self.cur.execute("INSERT INTO messages(stream_id, user, message, time) VALUES(%s, %s, %s, NOW())", (self.channel_id, username, msg))
        # optionally print the messages
        # print timestamp, username, msg

    # override run function from interface
    def run(self):
        readbuffer = ""

        while 1:
            # self.con.close()
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
    
                    msg = ' '.join(line[3:])[1:]
                    self.con = mdb.connect('localhost', 'root', 'lolipop123', 'twitch_mining');
                    self.con.autocommit(True)
                    self.con.ping(True)
                    self.cur = self.con.cursor(mdb.cursors.DictCursor)

                    self.insert_message(username, msg)

                    self.con.close()

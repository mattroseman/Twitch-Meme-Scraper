import MySQLdb as mdb
import sys

"""
Script to get latest chat messages from a twitch stream and add them to a file
arguments: url of twitch site
using:
    http://code.activestate.com/recipes/299411-connect-to-an-irc-server-and-store-messages-into-a/
"""

import sys, socket, string, datetime

class DataBot():

    stream_id = '1'
    con = mdb.connect('localhost', 'root', 'lolipop123', 'twitch_mining');
    con.autocommit(True)
    # make the cursor a dictionary
    # can now reference rows as a dictions
    # print row['id']
    cur = con.cursor(mdb.cursors.DictCursor)

    SERVER = 'irc.twitch.tv'
    PORT = 6667
    NICKNAME = 'mroseman_bot'
    PASSWORD = 'oauth:glz9hskrj3umqvzix5876fc6fdj0u9'
    
    BUFFER_SIZE = 1024
    
    IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, channel):
    #  open socket
        # self.IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc_conn()
        self.login(self.NICKNAME, self.PASSWORD)
        self.join(channel)
        print "succesfully joined channel"
    
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
        self.cur.execute("INSERT INTO messages(stream_id, user, message, timestamp) VALUES(%s, %s, %s, %s)", (self.stream_id, username, msg, timestamp))
        print timestamp
        print username
        print msg

    def log_chat(self):
        readbuffer = ""
        username = ""
        timestamp = ""
        msg = ""
    
        while 1:
            readbuffer=readbuffer + self.get_data()
            print readbuffer
            temp = string.split(readbuffer, '\n')
            readbuffer = temp.pop()
    
            for line in temp:
                line = string.rstrip(line)
                line = string.split(line)
                print line[0]
                tempp = line[0].find('!')
                if tempp != '-1':
                    username = line[0].replace(":", "",  1)
                    username = username[:tempp - 1]
    
                timestamp = datetime.datetime.utcnow().strftime("%b %d %H:%M:%S %Y")
                msg = ' '.join(line[3:])[1:]
    
                if (line[0] == 'PING'):
                    self.send_data('PONG %s' % line[1])
                if (line[1] == 'PRIVMSG'):
                    # comment below code to disable printing to terminal
                    self.insert_message(username, msg, timestamp)
# myBot = DataBot("esl_csgo")
# myBot.log_chat()

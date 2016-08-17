#!/usr/bin/python
import MySQLdb as mdb
from threading import Thread
import requests
import sys, socket, string, datetime
from visualization.db_connect import SQLConnection
import json

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
    PASSWORD = 'oauth:1a6m7cnaoispip8l00zy0h9nv2hten'

    BUFFER_SIZE = 1024

    #  if the user count drops below this stop monitoring
    user_limit = 250

    
    # default constructor
    def __init__(self, channel_id, channel):
        # initialize threading
        Thread.__init__(self)
        self.daemon = True

        # create IRC socket object 
        self.IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # join the channel and authenticate
        self.channel_id = channel_id
        self.channel = channel
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
        self.send_data("JOIN #%s" % channel)
    
    #  send login data
    def login(self, nickname, password=None):
        self.send_data("PASS %s" % password)
        self.send_data("NICK %s" % nickname)
    
    # insert to database
    def insert_message(self, username, msg):
        msg = msg.replace('\'', '\\\'')
        msg = msg.replace ('\"', '\\\"')

        #  insert the username if it doesnt already exist
        query = """
        INSERT IGNORE Users (UserName, Monitor) VALUES ('{0}', FALSE);
        """.format(username)
        self.con.query(query)

        #  insert this specific message to the Messages table
        query = """
        INSERT INTO Messages (StreamerID, UserID, Message, Time, GameID)
        VALUES ('{0}', (SELECT ID FROM Users WHERE UserName='{1}'), %(msg)s, NOW(),
        '{2}');
        """.format(self.channel_id, username, '1')
        self.con.query(query, {'msg':msg})

        # optionally print the messages
        # print timestamp, username, msg

    def keep_monitoring(self):
        """
        queries the database to see if this channel should still be monitored
        returns true if the thread should remain and false if the thread should
        stop
        """
        query = """
        SELECT Monitor FROM Users
        WHERE UserName=%(channel)s;
        """
        #  if the channel is no longer set to monitor in the database
        if not self.con.query(query, {'channel':self.channel})[0].get('Monitor'):
            return False

        #  if the channel has fewer than 250 users
        num_users = int(requests.get('https://api.twitch.tv/kraken/' +\
                                 'search/streams/{0}'.format(self.channel)).json()['viewers'])
        if num_users < user_limit:
            return False
        
        return True

    # override run function from interface
    def run(self):
        print ('thread started')

        self.con = SQLConnection()

        readbuffer = ""

        while 1:
            #  Check to see if this channel should still be monitored
            if not self.keep_monitoring():
                print ('killing self')
                self.con.close()
                #kill self
                sys.exit(0)

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

                    self.insert_message(username, msg)

#!/usr/bin/python

"""
Script to get latest chat messages from a twitch stream and add them to a file
arguments: url of twitch site
using:
    http://code.activestate.com/recipes/299411-connect-to-an-irc-server-and-store-messages-into-a/
"""

import sys, socket, string, datetime

SERVER = 'irc.twitch.tv'
PORT = 6667
NICKNAME = 'mroseman_bot'
PASSWORD = 'oauth:glz9hskrj3umqvzix5876fc6fdj0u9'

BUFFER_SIZE = 1024

IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#  open connection
def irc_conn():
    IRC.connect((SERVER, PORT))
    print "connected"

#  send data through socket
def send_data(command):
    IRC.send(command + '\r\n')

#  get data through socket
def get_data():
    return IRC.recv(BUFFER_SIZE)

#  join a channel
def join(channel):
    send_data("JOIN %s" % channel)

#  send login data
def login(nickname, password=None):
    send_data("PASS %s" % password)
    send_data("NICK %s" % nickname)


def log_chat(channel):
    irc_conn()
    login(NICKNAME, PASSWORD)
    join(channel)
    print "joined channel"
    readbuffer = ""
    username = ""
    timestamp = ""
    msg = ""

    while 1:
        readbuffer=readbuffer + get_data()
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
                send_data('PONG %s' % line[1])
            if (line[1] == 'PRIVMSG'):
                # comment below code to disable printing to terminal
                print timestamp
                print username
                print msg
        print "entering while loop"
log_chat("beyondthesummit")
# myBot.log_chat()

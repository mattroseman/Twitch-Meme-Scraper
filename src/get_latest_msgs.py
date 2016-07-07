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

#  open socket
IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#  open connection
def irc_conn():
    IRC.connect((SERVER, PORT))

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


def main():
    if len(sys.argv) != 2:
        print 'missing channel name argument'
        return

    #  log file
    try:
        log = open('../log/%s_log.txt' % sys.argv[1], 'a')
    except IOError:
        print 'could not open file'
    channel = '#%s' %  sys.argv[1]

    irc_conn()
    login(NICKNAME, PASSWORD) 
    join(channel)
    readbuffer = ""

    while 1:
        readbuffer=readbuffer + get_data()
        temp = string.split(readbuffer, '\n')
        readbuffer = temp.pop()

        for line in temp:
            line = string.rstrip(line)
            line = string.split(line)

            log_msg = datetime.datetime.utcnow().strftime("%b %d %H:%M:%S %Y") + \
                      ' | ' + ' '.join(line[3:])[1:] + '\n'

            if (line[0] == 'PING'):
                send_data('PONG %s' % line[1])
            if (line[1] == 'PRIVMSG'):
                try:
                    log.write(log_msg)
                except IOError:
                    print 'error printing to file'
                #Comment below code to disable printing to terminal
                print log_msg

            

if __name__ == '__main__':
    sys.exit(main())

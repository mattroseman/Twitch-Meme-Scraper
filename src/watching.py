from visualization.db_connect import SQLConnection
import requests, socket, sys, string

print ('Connecting to DataBase')
con = SQLConnection()

SERVER = 'irc.twitch.tv'
PORT = 6667
NICKNAME = 'mroseman_bot'
PASSWORD = 'oauth:1a6m7cnaoispip8l00zy0h9nv2hten'

BUFFER_SIZE = 1024

#  connect to twitch irc server
IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IRC.connect((SERVER, PORT))

def send_data(command):
    IRC.send(command + '\r\n')

send_data('PASS %s' % PASSWORD)
send_data('NICK %s' % NICKNAME)
send_data('CAP REQ :twitch.tv/membership')
readbuffer = ''
readbuffer = readbuffer + IRC.recv(BUFFER_SIZE)
temp = string.split(readbuffer, '\n')
readbuffer = temp.pop()
for line in temp:
    print (line)

#  run forevor
while True:
    #  get list of channels that are being monitored
    query = """
    SELECT Id FROM Users
    WHERE Monitored=True;
    """
    streams = self.con.query(query)

    for stream in streams:
        #  for each stream get the list of users
        

        #  TODO I bet there is a better way of doing this -Matt
        query = """
        START TRANSACTION;
            DELETE FROM Watching
            WHERE StreamId=%(stream)s;
            
            INSERT 
        """

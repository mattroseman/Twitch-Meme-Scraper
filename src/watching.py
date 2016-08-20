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

def get_users(channel):
    """
    takes in a channel name and gathers the list of users currently signed into
    twitch and watching that channel
    @return: returns an array of strings that are users watching this channel
    """
    send_data('JOIN #{0}'.format(channel))

    users = []

    listing_names = False
    while True:
        readbuffer = ''
        readbuffer = readbuffer + IRC.recv(BUFFER_SIZE)
        temp = string.split(readbuffer, '\n')
        readbuffer = temp.pop()

        for line in temp:
            line = string.rstrip(line)
            print (line)
            if 'JOIN' in line:
                listing_names = True
                continue
            if 'End of /NAMES list' in line:
                listing_names = False
                return users
            if listing_names:
                line = line.replace(':', '')
                line = line.split(' ')
                line = line[5:]
                users = users + line

def get_userid(username):
    """
    takes a username and returns the coresponding user id from the database
    """
    query = """
    SELECT Id FROM Users
    WHERE UserName=%(username)s;
    """
    return con.query(query, {'username':username})[0].get('Id')

#  run forevor
while True:
    #  get list of channels that are being monitored
    query = """
    SELECT UserName FROM Users
    WHERE Monitor=True;
    """
    streams = map(lambda x: x.get('UserName'), con.query(query))

    for stream in streams:
        #  get id of this stream
        stream_id = get_userid(stream)

        print ('getting users for stream: {0}/{1}'.format(stream, stream_id))

        #  for each stream get the list of users
        users = get_users(stream)
        print (users)

        #  for each user get id and add it to the list of new rows
        new_rows = ''
        for user in users:
            #  add this user to Users if it doesn't already exist
            query = """
            INSERT IGNORE INTO Users (UserName)
            VALUE (%(username)s);
            """
            con.query(query, {'username':user})

            user_id = get_userid(user)
            print ('adding user: {0}/{1}'.format(user, user_id))

            new_rows = new_rows + '({0}, {1}), '.format(user_id, stream_id)

        #  take off the last ', ' of new_rows
        new_rows = new_rows[:-2]

        #  TODO I bet there is a better way of doing this -Matt
        query = """
        START TRANSACTION;
            DELETE FROM Watching
            WHERE StreamId=(SELECT Id FROM Users
                            WHERE UserName=%(stream)s);

            INSERT IGNORE INTO Watching (UserId, StreamId)
            VALUES %(rows)s;
        COMMIT;
        """

        print ('updating watching table for stream: {0}'.format(stream))
        con.query(query, {'stream':stream, 'rows':new_rows})

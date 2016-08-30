from visualization.db_connect import SQLConnection
import requests, socket, sys, string, json

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
    r = requests.get('https://tmi.twitch.tv/' +
                     'group/user/{0}/chatters'.format(channel)).json()
    users = []
    if (r['chatter_count'] >= 1000):
        print ('usercount over 1000')
        r = r['chatters']
        #  get user count from api instead
        if r['moderators']:
            users = r['moderators']
        if r['staff']:
            users = users + r['staff']
        if r['admins']:
            users = users + r['admins']
        if r['global_mods']:
            users = users + r['global_mods']
        if r['viewers']:
            users = users + r['viewers']
        return users

    else:
        send_data('JOIN #{0}'.format(channel))

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
        query = """
        SELECT Id FROM Users
        WHERE UserName='%(user)s';
        """
        stream_id = get_userid(stream)
        print ('streamid is ' + str(stream_id))

        #  for each stream get the list of users
        users = get_users(stream)
        print (users)

        #  update Users to make sure it has all users
        user_values = '(' + '), ('.join(users) + ')'
        query = """
        INSERT IGNORE INTO Users (UserName)
        VALUES %(users)s;
        """

        #  for each user add it to the list of new rows
        new_rows = ''
        json_users = {}
        for user in users:
            #  TODO maybe try havving a %(quote)s and have that map in a single
            #  quote
            user_id = ("(SELECT Id FROM Users WHERE " +\
                       "UserName=%({0})s)").format(user)
            json_users[user] = "'{0}'".format(user)
            new_rows = new_rows + '({0}, {1}), '.format(user_id, stream_id)

        #  take off the last ', ' of new_rows
        new_rows = new_rows[:-2]

        #  TODO I bet there is a better way of doing this -Matt
        #query = """
        #START TRANSACTION;
        #    DELETE FROM Watching
        #    WHERE StreamId = {0};

        #    INSERT IGNORE INTO Watching (UserId, StreamId)
        #    VALUES {1};
        #COMMIT;
        #""".format(stream_id, new_rows)
        query = """
        INSERT IGNORE INTO Watching (UserId, StreamId)
        VALUES {0};
        """.format(new_rows)

        print (new_rows)
        print (json_users)

        print ('updating watching table for stream: {0}'.format(stream))
        con.query(query, json_users)

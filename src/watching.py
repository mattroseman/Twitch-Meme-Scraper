import requests, socket, sys, string, json, time, random, re, sets
from db_connect import SQLConnection
from db_connect import NoSQLConnection
from pymongo import MongoClient

print ('connecting to SQL database')
con = SQLConnection()

print ('connecting to noSQL database')
nosql_con = NoSQLConnection()

## Constants
SERVER = 'irc.twitch.tv'
PORT = 6667
NICKNAME = 'mroseman_bot'
PASSWORD = 'oauth:1a6m7cnaoispip8l00zy0h9nv2hten'

BUFFER_SIZE = 2048

join_ttl = 300  #  the time to live for the joining user elements in database
leave_ttl = 300 #  this is the number of seconds before leave elements are
                #  removed

irc_min_users = 100 #  if the number of users from IRC is less then 100 then
                    # the result is double checked with an API call

headers = { 'Client-ID': 'sdu5b9af6eoqgkxdkb0qrkd9fgcp6ch'}
names_substring = ':{0}.tmi.twitch.tv 353 {0} = #{1} :'

#  connect to twitch irc server
print ('connecting to twitch IRC')
IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IRC.connect((SERVER, PORT))

last_api_call = time.time() #  time used to limit twitch API calls to one per second

class IRCBadMessage(Exception):
    pass

def send_data(command):
    """
    sends the given command to the IRC server
    """
    IRC.send(command + '\r\n')

send_data('PASS %s' % PASSWORD)
send_data('NICK %s' % NICKNAME)
send_data('CAP REQ :twitch.tv/membership')

def parse_line(line):
    """
    takes an irc message and parses it into prefix, command and args
    @return: (prefix, command, args)
    """
    prefix = ''
    if not line:
        raise IRCBadMessage("Empty line.")
    if line[0] == ':':
        prefix, line = line[1:].split(' ', 1)
    if line.find(' :') != -1:
        line, trailing = line.split(' ', 1)
        args = line.split()
        args.append(trailing)
    else:
        args = line.split()
    command = args.pop(0)
    if not command or not args:
        raise IRCBadMessage('Improperly formatted line: {0}'.format(line))
    return prefix, command, args

#  TODO change this so that it just gets all the users from irc and returns
#  them as an array
def get_irc_users(channel):
    """
    gets a list of users from the IRC NAMES command
    @return: an array of users from the irc (may be just OPs)
    """
    #  join the IRC channel
    send_data('JOIN #{0}'.format(channel))
    users = []
    while True:
        readbuffer = ''
        readbuffer = readbuffer + IRC.recv(BUFFER_SIZE)
        temp = string.split(readbuffer, '\n')
        readbuffer = temp.pop()
        for line in temp:
            line = string.rstrip(line)
            try:
                _,command,args = parse_line(line)
            except IRCBadMessage as e:
                print (e)
                return []

            #  if this is a response to NAMES
            if command == '353':
                users += ((args[0].split(':', 1))[1].split())
            if 'End of /NAMES list' in args[0]:
                print ('test1')
                send_data('PART #{0}'.format(channel))
                return users

def get_users(channel):
    """
    takes in a channel name and gathers the list of users currently signed into
    twitch and watching that channel
    @return: returns an array of strings that are users watching this channel
    """
    global headers


    #  if less then a second has passed since the last call wait
    global last_api_call
    temp_names_substring = names_substring.format(NICKNAME, channel)
    while ((time.time() - last_api_call) < 1):
        pass
    last_api_call = time.time()

    print ('getting users for: ' + channel)
    users = get_irc_users(channel)
    print ('length of users gotten from IRC is {0}'.format(len(users)))

    #  print random string to make reading terminal easier
    #print (''.join(random.choice(string.ascii_uppercase + string.digits) for _
    #       in range(5)))

    if len(users) < irc_min_users:
        print (('IRC user count is less than {0}, now double checking with ' +
                'API call').format(irc_min_users))
        r = requests.get(('https://tmi.twitch.tv/' +
                          'group/user/{0}/chatters').format(channel),
                         headers=headers).json()
        users = []

        if r is None:
            print ('null response gotten')
        else:
            usercount = r['chatter_count']
            print ('usercount = {0}'.format(usercount))
            if (usercount > 0):
                r = r['chatters']

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

def get_monitored_streams():
    #  get list of channels that are being monitored
    query = """
    SELECT UserName FROM Users
    WHERE Monitor=True;
    """
    return map(lambda x: x.get('UserName'), con.query(query))

while True:
    print("""

    -------------------------------------------------------
    streams updated now starting from beginning 
    -------------------------------------------------------

    """)

    streams = get_monitored_streams()

    nosql_con.delete(
            { 
                'streamname': 
                {
                    #  delete any documents where the streamname is not present
                    #  in streams
                    '$nin': streams
                }
            }
    )

    for stream in streams:
        users = get_users(stream)
        users_joining = []
        users_leaving = []
        #  really these are an array of json objects
        joining_json = []
        leaving_json = []

        # figure out any new users and any users that have left
        old_users = nosql_con.query(
                { 
                    'streamname': stream 
                },
                {
                    '_id': False,
                    'watching':True
                }
        )
        #  if this stream is in the database get joining and leaving users
        if old_users.count() == 1:
            old_users = sets.Set(old_users[0]['watching'])
            new_users = sets.Set(users)
            #  users in new_users that aren't in old_users
            users_joining = new_users.difference(old_users)
            #  users in old_users that are no longer in new_users
            users_leaving = old_users.difference(new_users)

        print ('\njoining users in {0}: {1}'.format(stream, users_joining))
        print ('leaving users in {0}: {1}\n'.format(stream, users_leaving))

        #  create the new joining and leave json to add to the database
        for user in users_joining:
            joining_json.append(
                {
                    'username': user,
                    'last_updated': time.time()
                }
            )
        for user in users_leaving:
            leaving_json.append(
                {
                    'username': user,
                    'last_updated': time.time()
                }
            )

        #  add these users to this streams document
        #  TODO make sure the joining and leaving json appends to the list and that
        #  any elements that have expiredd are removed
        print ('updating watching users in the database')
        result = nosql_con.update(
            { 'streamname': stream },
            {
                '$set': {
                    'watching': users,
                },
                '$push': {
                    'joining': {
                        '$each': joining_json,
                    },
                    'leaving': {
                        '$each': leaving_json
                    }
                },
                '$setOnInsert': {
                    'streamname': stream,
                }
            }
        )
        #  removing any stale joining or leaving users
        result = nosql_con.update(
            { 'streamname': stream },
            {
                '$pull': {
                    'joining': {
                        'last_updated': {
                            '$lte': time.time() - join_ttl
                        }
                    },
                    'leaving': {
                        'last_updated': {
                            '$lte': time.time() - leave_ttl
                        }
                    }
                }
            }
        )

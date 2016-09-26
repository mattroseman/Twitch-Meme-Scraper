import sys, string, json, time, random, re, sets
from irc_connect import IRCConnection
from api_connect import APIConnection
from db_connect import SQLConnection
from db_connect import NoSQLConnection
from pymongo import MongoClient

print ('connecting to SQL database')
con = SQLConnection()

print ('connecting to noSQL database')
nosql_con = NoSQLConnection()

print ('connecting to IRC server')
irc = IRCConnection()

print ('creating API connection')
api = APIConnection()

## Constants
join_ttl = 300  #  the time to live for the joining user elements in database
leave_ttl = 300 #  this is the number of seconds before leave elements are
                #  removed

irc_min_users = 100 #  if the number of users from IRC is less then 100 then
                    # the result is double checked with an API call

last_api_call = time.time() #  time used to limit twitch API calls to one per second

def get_users(channel):
    """
    takes in a channel name and gathers the list of users currently signed into
    twitch and watching that channel
    @return: returns an array of strings that are users watching this channel
    """
    global headers

    #  if less then a second has passed since the last call wait
    global last_api_call
    while ((time.time() - last_api_call) < 1):
        pass
    last_api_call = time.time()

    print ('getting users for: ' + channel)
    users = irc.get_channel_users(channel)
    print ('length of users gotten from IRC is {0}'.format(len(users)))

    #  print random string to make reading terminal easier
    #print (''.join(random.choice(string.ascii_uppercase + string.digits) for _
    #       in range(5)))

    if len(users) < irc_min_users:
        print (('IRC user count is less than {0}, now double checking with ' +
                'API call').format(irc_min_users))
        users = api.get_users(channel)

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
        #  if the users list is empty something wen't wrong
        if len(users) == 0:
            continue

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

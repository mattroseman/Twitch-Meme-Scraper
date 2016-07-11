from twitch import TopStreams
import requests
import sys
import MySQLdb as mdb

try:
    # TODO move these credentials to a separate file
    con = mdb.connect('localhost', 'root', 'lolipop123', 'twitch_mining');

    con.autocommit(True)
    # mysql terminates idle connection (8 hrs). ping(true) attempts a reconnect if con has been terminated
    con.ping(True)
    cur = con.cursor(mdb.cursors.DictCursor)
    test_list = list()
    test_list = ["hello", "hi"]
    print test_list

    # query = "INSERT INTO streams (name) VALUES %r;" % (tuple(test_list),)
    # cur.execute(query)

    # cur.execute('INSERT INTO table (name) VALUES (?);', [','.join(test_list)])

    # get the list of channels to listen on
    cur.execute("SELECT * FROM streams")
    rows = cur.fetchall()
    # for row in rows:
        # print row['name']

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    
# close connection to DB
finally:    
    if con:    
        con.close()

# create object to check twitch for the top streams
# takes parameters - how many games to check, and how many streams to check within the games

payload = {'limit' : '15'}
b = requests.get('https://api.twitch.tv/kraken/games/top', params = payload)
for i in range(int(payload['limit'])): 
    game_name = b.json()['top'][i]['game']['name']
    print game_name
    twitch = TopStreams.TopStreams(game_name)
# game_name = b.json()['top'][0]['game']['name']
# twitch = TopStreams.TopStreams(game_name)

while True:
    pass


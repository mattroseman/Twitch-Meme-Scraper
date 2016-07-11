from twitch import TopStreams
import requests
import sys
import MySQLdb as mdb

# TODO figure out where exactly this goes
# cron job run this program

"""
Main controller function that creates objects, which find the top streams for the top games
Lots of debug code is still present
"""

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

# change the limit to adjust how many of the top games you want to track
payload = {'limit' : '15'}
b = requests.get('https://api.twitch.tv/kraken/games/top', params = payload)
for i in range(int(payload['limit'])): 
# create object to check twitch for the top streams
    game_name = b.json()['top'][i]['game']['name']
    print game_name
    twitch = TopStreams.TopStreams(game_name)

# keep main thread alive
# TODO add in thread.join() statements in order to elegantly end the program
while True:
    pass


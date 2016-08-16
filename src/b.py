from visualization.db_connect import SQLConnection
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
    con = SQLConnection()

    # get the list of channels to listen on
    df = con.query("SELECT * FROM Users WHERE Monitor = TRUE")

except mdb.Error as e:
    print ("Error %d: %s" % (e.args[0],e.args[1]))
    
# close connection to DB
finally:    
    #  close connection
    pass

# change the limit to adjust how many of the top games you want to track
payload = {'limit' : '15'}
b = requests.get('https://api.twitch.tv/kraken/games/top', params = payload)
for i in range(int(payload['limit'])): 
# create object to check twitch for the top streams
    game_name = b.json()['top'][i]['game']['name']
    print (game_name)
    twitch = TopStreams.TopStreams(game_name)

# keep main thread alive
# TODO add in thread.join() statements in order to elegantly end the program
while True:
    pass


from bots import DataBot
from threading import Thread
import MySQLdb as mdb
import sys
# tryexcept block for initial mysql connection
try:
    # TODO move these credentials to a separate file
    con = mdb.connect('localhost', 'root', 'lolipop123', 'twitch_mining');

    con.autocommit(True)
    cur = con.cursor(mdb.cursors.DictCursor)

    # get the list of channels to listen on
    cur.execute("SELECT * FROM streams")
    rows = cur.fetchall()

    for row in rows:
        # for each channel, create a bot instance
        bot = DataBot.DataBot('#' + row['name'], row['id'])
    # keep the main thread alive in order to keep child threads alive as well
    while True:
        pass

# print mysql error messages
except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
# close connection to DB
finally:    
    if con:    
        con.close()


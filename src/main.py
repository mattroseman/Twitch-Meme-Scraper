from bots import DataBot
# from threading import Thread
import MySQLdb as mdb
import sys
from db_connect import SQLConnection
import time

update_interval = 300

# tryexcept block for initial mysql connection
try:

    while True:
        print ('checking for new streams')
        con = SQLConnection()

        # get the list of channels to listen on
        rows = con.query("SELECT * FROM Users WHERE Monitor=TRUE")

        for row in rows:
            # for each channel, create a bot instance
            bot = DataBot.DataBot(row['ID'], row['UserName'])
        # keep the main thread alive in order to keep child threads alive as well

        con.close()
        time.sleep(update_interval)


# print mysql error messages
except mdb.Error as e:
    print ("Error %d: %s" % (e.args[0],e.args[1]))
    sys.exit(1)
    
# close connection to DB
finally:    
    #  possibly close connection
    pass

from bots import DataBot
# from threading import Thread
import MySQLdb as mdb
import sys
from visualization.db_connect import SQLConnection

# tryexcept block for initial mysql connection
try:
    con = SQLConnection()

    # get the list of channels to listen on
    df = con.query("SELECT * FROM Users WHERE Monitor=TRUE")

    for index, row in df.iterrows():
        # for each channel, create a bot instance
        bot = DataBot.DataBot(row['ID'], '#' + row['UserName'])
    # keep the main thread alive in order to keep child threads alive as well
    while True:
        pass

# print mysql error messages
except mdb.Error as e:
    print ("Error %d: %s" % (e.args[0],e.args[1]))
    sys.exit(1)
    
# close connection to DB
finally:    
    #  possibly close connection
    pass

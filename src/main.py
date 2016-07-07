from bots import DataBot
from threading import Thread
import MySQLdb as mdb
import sys
def attach_bot(name, stream_id):
    """thread worker function"""
    print stream_id, name 
    bot = DataBot.DataBot('#' + name, stream_id)
    # bot.log_chat()
    return
try:
    con = mdb.connect('localhost', 'root', 'lolipop123', 'twitch_mining');

    con.autocommit(True)
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute("SELECT * FROM streams")
    rows = cur.fetchall()

    for row in rows:
        bot = DataBot.DataBot('#' + row['name'], row['id'])
    while True:
        pass
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
    if con:    
        con.close()

# myBot = DataBot.DataBot("#esl_csgo", 1)
# myBot.log_chat()

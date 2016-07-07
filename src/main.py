from bots import DataBot
import threading
import MySQLdb as mdb
import sys
threads = []
def attach_bot(name, stream_id):
    """thread worker function"""
    print stream_id, name 
    bot = DataBot.DataBot('#' + name, stream_id)
    bot.log_chat()
    return
try:
    con = mdb.connect('localhost', 'root', 'lolipop123', 'twitch_mining');

    con.autocommit(True)
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute("SELECT * FROM streams")
    rows = cur.fetchall()
    for row in rows:
        t = threading.Thread(target=attach_bot(row['name'], row['id']))
        threads.append(t)
        t.start()
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
    if con:    
        con.close()

# myBot = DataBot.DataBot("#esl_csgo")
# myBot.log_chat()

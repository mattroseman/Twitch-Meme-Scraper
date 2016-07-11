import MySQLdb as mdb
import sys
import requests
from threading import Thread
"""
Script to get the top 8 games from Twitch, and the top 8 streams for each game
Implements Thread interface

"""

class TopStreams(Thread):
    PASSWORD = 'oauth:glz9hskrj3umqvzix5876fc6fdj0u9'
    OAUTH = 'glz9hskrj3umqvzix5876fc6fdj0u9'

    def get_top(self):
        # self.game_name = 'NBA 2K16'
        # payload = {'q' : self.game_name, 'limit' : '100'}
        payload = {'q' : self.game_name, 'limit' : '100'}
        stream_list = list()
        r = requests.get('https://api.twitch.tv/kraken/search/streams', params = payload)
        streams_limit = int(r.json()["_total"])
        offset = 0
        print "Stream limit: ", streams_limit
        # print r.json()['streams'][0]['viewers'], r.json()['streams'][0]['channel']['name']
        print r.json()['_links']['next']
        # sort the streams in order to find top 10 
        try: 
            while streams_limit > offset: 
                # print streams_limit, offset
                offset = offset + 100
                print "----------------------------------------------------------------------------- START ITERATION ---------------------------------------------------"
                try: 
                    for i in range(10):
                        if r.json()['streams'][i]['game'] == self.game_name and int(r.json()['streams'][i]['viewers']) > 250:
                            print r.json()['streams'][i]['viewers'], r.json()['streams'][i]['channel']['name'], i
                            stream_list.append(str(r.json()['streams'][i]['channel']['name']))
                        else:
                            pass
                    r = requests.get(r.json()['_links']['next'])
                except:
                    print "list index out of range, no biggie"
            print "FINISHED N"
            print stream_list
            return list(set(stream_list))
        except NameError as ex:
            print "FINISHEDEXCEPTI"
            print ex
            e = sys.exc_info()[0]
            print e
            return list(set(stream_list))


    def __init__(self, game_name):
        # initialize threading
        Thread.__init__(self)
        self.daemon = True
        
        self.game_name = game_name

        self.con = mdb.connect('localhost', 'root', 'lolipop123', 'twitch_mining');
        self.con.autocommit(True)
        self.con.ping(True)
        self.cur = self.con.cursor(mdb.cursors.DictCursor)

        self.start()    

    def run(self):
        payload = {'oauth_token' : self.OAUTH}
        # r = requests.get('https://api.twitch.tv/kraken/', params = payload)


        stream_list = self.get_top()
        print "in run function again"
        print stream_list
        for i in stream_list:
            query = 'INSERT INTO streams (name) VALUES ("' + i + '")'
            print query
            try: 
                self.cur.execute(query)
            except mdb.Error, e:
                print "Error %d: %s" % (e.args[0],e.args[1])

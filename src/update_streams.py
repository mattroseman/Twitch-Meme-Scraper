from db_connect import SQLConnection
import requests, urllib, json, time

##  constants
update_interval = 60    # time in seconds between top stream updates
game_limit = 20         # the number of top games to get
stream_limit = 20       # the number of streams to get for each game (as long as
                        #they are over the viewer limit
viewer_limit = 200      # the minimum number of viewers a stream must have to be
                        # monitored

con = SQLConnection()

streams = []

def get_top_streams(game_name):
    """
    find the top channels for a specific game on twitch
    @param game_name: the name of the game to search
    @return: no return, simply adds streams to global streams list
    """
    global streams

    print (('requesting top {0} streams for game {1} from' +
            'API').format(stream_limit, game_name))
    game_name = game_name
    payload = urllib.urlencode({
                'game': game_name,
                'limit': str(stream_limit),
                'stream_type': 'live',
                'language': 'en'
              })
    r = requests.get('https://api.twitch.tv/kraken/streams',
                     params=payload).json()
    for stream in r['streams']:
        #  if the stream has enough viewers to be monitored
        if stream['viewers'] >= viewer_limit:
            streams.append(stream['channel']['name'])


while True:
    print ('requesting top {0} games from API'.format(game_limit))
    payload = {'limit': str(game_limit)}
    r = requests.get('https://api.twitch.tv/kraken/games/top',
                     params=payload).json()

    for game in r['top']:
        game_name = game['game']['name']
        get_top_streams(game_name)
    escaped_streams = '(%(' + ')s, True), (%('.join(streams) + ')s, True)'
    json_streams = {}
    print ('adding these streams to database to be monitored...')
    for stream in streams:
        print ('\t{0}'.format(stream))
        json_streams[stream] = stream
    query = """
    INSERT INTO Users (UserName, Monitor)
    VALUES {0}
    ON DUPLICATE KEY UPDATE Monitor=True;
    """.format(escaped_streams)
    con.query(query, json_streams)
    time.sleep(update_interval)

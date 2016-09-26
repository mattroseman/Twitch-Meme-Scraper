import requests, string, time

headers = { 'Client-ID': 'sdu5b9af6eoqgkxdkb0qrkd9fgcp6ch'}
viewer_limit = 200 #  the mimnimum number of viewers a stream must have to be
                   #  monitored
timeout = 10 #  the number of seconds that will be waited if a 503 response is
             #  gotten
num_tries = 3 #  the number of times to retry the request before giving up

class APIBadRequest(Exception):
    pass

class APIConnection:

    def __init__(self):
        self.log = open('watching_log.txt', 'w')

    def _send_request(self, request, params=None):
        """
        sends an api request with params and headers
        keeps sending if there is a 503 result (times out for 'timeout' 
        seconds
        """
        for i in xrange(0,num_tries):
            result = requests.get(request, params=params,
                                  headers=headers)
            if self._valid_result(result):
                return result.json()
            else:
                print (('\n{0} request failed, waiting {1} seconds to try' +
                        'again\n').format(i, timeout))
            time.sleep(timeout)
        raise APIBadRequest('after {0} tries the api continues to send bad' +
                            'results')

    def _valid_result(self, result):
        """
        checks the status code of the result
        """
        if result.status_code == 200:
            return True
        else:
            self.log.write(str(time.time()) + 
                           ': ' + str(result.status_code) +
                           '\n')
            print (result.status_code)
            return False

    def get_top_games(self, limit):
        """
        gets the top 'limit' games from twitch
        @return: a list of top game names
        """
        games = []
        payload = {'limit': str(limit)}
        result = self._send_request('https://api.twitch.tv/kraken/games/top',
                                    payload)
        for game in r['top']:
            games.append(game['game']['name'])

        return games

    def get_top_streams(self, game, limit):
        """
        returns the 'limit' top streams for a game 'game'
        """
        streams = []
        payload = urllib.urlencode({
                    'game': game,
                    'limit': str(limit),
                    'stream_type': 'live',
                    'language': 'en'
                })
        result = self._send_request('https://api.twitch.tv/kraken/streams',
                                    payload)

        for stream in result['streams']:
            #  if the stream has enough viewers to be monitored
            if stream['viewers'] >= viewer_limit:
                streams.append(stream['channel']['name'])

        return streams

    def get_users(self, channel):
        """
        gets all the viewers of a specific channel
        """
        users = []
        url = 'https://tmi.twitch.tv/group/user/{0}/chatters'.format(channel)
        result = self._send_request(url)

        usercount = result['chatter_count']
        print ('usercount = {0}'.format(usercount))
        if (usercount > 0):
            result = result['chatters']

            if result['moderators']:
                users = result['moderators']
            if result['staff']:
                users = users + result['staff']
            if result['admins']:
                users = users + result['admins']
            if result['global_mods']:
                users = users + result['global_mods']
            if result['viewers']:
                users = users + result['viewers']

        return users

import socket, string

## Constants
SERVER = 'irc.twitch.tv'
PORT = 6667
NICKNAME = 'mroseman_bot'
PASSWORD = 'oauth:1a6m7cnaoispip8l00zy0h9nv2hten'

BUFFER_SIZE = 2048

class IRCBadMessage(Exception):
    pass

class IRCConnection:
    """
    Used to connect to the twitch irc server and get messages, etc from
    different channels
    """

    def __init__(self):
        self.IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IRC.connect((SERVER, PORT))

        self.send_data('PASS %s' % PASSWORD)
        self.send_data('NICK %s' % NICKNAME)
        self.send_data('CAP REQ :twitch.tv/membership')

    def send_data(self, command):
        """
        sends the given command to the IRC server
        """
        self.IRC.send(command + '\r\n')


    def _parse_line(self, line):
        """
        takes an irc message and parses it into prefix, command and args
        @return: (prefix, command, args)
        """
        prefix = ''
        if not line:
            raise IRCBadMessage("Empty line.")
        if line[0] == ':':
            prefix, line = line[1:].split(' ', 1)
        if line.find(' :') != -1:
            line, trailing = line.split(' ', 1)
            args = line.split()
            args.append(trailing)
        else:
            args = line.split()
        command = args.pop(0)
        if not command or not args:
            raise IRCBadMessage('Improperly formatted line: {0}'.format(line))
        return prefix, command, args

    def get_channel_users(self, channel):
        """
        gets a list of users from the IRC NAMES command
        @return: an array of users from the irc (may be just OPs)
        """
        #  join the IRC channel
        self.send_data('JOIN #{0}'.format(channel))
        users = []
        while True:
            readbuffer = ''
            readbuffer = readbuffer + self.IRC.recv(BUFFER_SIZE)
            temp = string.split(readbuffer, '\n')
            readbuffer = temp.pop()
            for line in temp:
                line = string.rstrip(line)
                try:
                    _,command,args = self._parse_line(line)
                except IRCBadMessage as e:
                    print ('bad IRC message received, returning empty user' +
                           'list')
                    print (e)
                    return []

                #  if this is a response to NAMES
                if command == '353':
                    users += ((args[0].split(':', 1))[1].split())
                if 'End of /NAMES list' in args[0]:
                    print ('test1')
                    self.send_data('PART #{0}'.format(channel))
                    return users
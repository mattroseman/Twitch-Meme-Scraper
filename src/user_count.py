from db_connect import SQLConnection
import requests, socket, sys, string, json

print ('Connecting to DataBase')
con = SQLConnection()

def get_userid(username):
    """
    takes a username and returns the coresponding user id from the database
    """
    query = """
    SELECT Id FROM Users
    WHERE UserName=%(username)s;
    """
    return con.query(query, {'username':username})[0].get('Id')

while True:
    #  get list of channels that are being monitored
    query = """
    SELECT UserName FROM Users
    WHERE Monitor=True;
    """
    streams = map(lambda x: x.get('UserName'), con.query(query))

    for stream in streams:
        query = """
        SELECT Id FROM Users
        WHERE UserName=%(user)s;
        """
        stream_id = get_userid(stream)

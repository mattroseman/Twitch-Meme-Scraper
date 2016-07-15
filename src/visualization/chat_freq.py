#!/usr/bin/python
import sys
from db_connect import SQLConnection

con = SQLConnection()

def main():
    #  query the database for just message times and nothing else
    times = con.query("SELECT timestamp FROM messages")
    con.close_connection()

    graph = open('chat_freq.html', 'a')


if __name__ == '__main__':
    sys.exit(main())

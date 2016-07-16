#!/usr/bin/python
import sys, re
from datetime import datetime
from db_connect import SQLConnection
import matplotlib.pyplot as plt

"""
used libraries: http://matplotlib.org/
"""
 #  interval measured in minutes, so 60min=hour 24hr=day
frequency_interval = 60*24
con = SQLConnection()

def get_date(utc_date):
    """takes a utc string date and finds the minutes since epoch"""
    try:
        date = datetime.strptime(utc_date, '%b %d %H:%M:%S %Y')
    except ValueError:
        print ('the utc date given was not in the correct format\n' +
               'should be: \"%b %d %H:%M:%S %Y\"')
        return None
    return date


def main():
    #  query the database for just message times and nothing else
    times = con.query("SELECT timestamp FROM messages")
    con.close_connection()

    print (times[0][0])
    print (times[-1][0])
    start_day = get_date(times[0][0]).days
    end_day = get_date(times[-1][0]).days
    print (start_day)
    print (end_day)

    msg_index = 0
    y_axis = range(start_day, end_day)


    graph = open('chat_freq.html', 'a')


if __name__ == '__main__':
    sys.exit(main())

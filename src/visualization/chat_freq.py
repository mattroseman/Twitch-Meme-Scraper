#!/usr/bin/python
import sys, re
from datetime import datetime
from db_connect import SQLConnection
import numpy as np
import matplotlib.pyplot as plt

"""
used libraries: http://matplotlib.org/
"""
 #  interval measured in minutes, so 60min=hour 24hr=day
frequency_interval = 60*24
con = SQLConnection()

"""
plt.figure(figsize=(8,6), dpi=80)
plt.subplot(111)
"""

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
    start_day = get_date(times[0][0]).day
    end_day = get_date(times[-1][0]).day
    print (start_day)
    print (end_day)

    #  TODO this won't work accross multiple months
    day_freq = [0] * (end_day - start_day + 1)

    #  for every message time
    for time in times:
        day_freq[get_date(time[0]).day - start_day] += 1

    day_axis = np.array(range(start_day, end_day + 1))
    freq_axis = np.array(day_freq)

    print (day_axis)
    print (freq_axis)

    plt.plot(day_axis, freq_axis, color='blue', linewidth=1.0, linestyle='-')

    plt.xlim(day_axis.min()*1.1, day_axis.max()*1.1)
    plt.ylim(0, freq_axis.max()*1.1)

    plt.xticks(np.linspace(start_day, end_day, 1, endpoint=True))
    plt.yticks(np.linspace(0, freq_axis.max(), 1, endpoint=True))

    plt.show()


if __name__ == '__main__':
    sys.exit(main())

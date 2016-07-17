#!/usr/bin/python
import sys, re, time, pandas
from datetime import datetime
from db_connect import SQLConnection
import numpy as np
import matplotlib.pyplot as plt

"""
used libraries: http://matplotlib.org/
"""
#  the name of the column in the database that contains the timestamp
timestamp_col = 'timestamp'

#  interval measured in minutes, so 60min=hour 24hr=day
frequency_interval = 60*24
con = SQLConnection()

plt.figure(figsize=(30, 18), dpi=80)

def get_time(utc_date):
    """takes a utc string date and finds the minutes since epoch"""
    try:
        date = datetime.strptime(utc_date, '%b %d %H:%M:%S %Y')
    except ValueError:
        print ('the utc date given was not in the correct format\n' +
               'should be: \"%b %d %H:%M:%S %Y\"')
        return None
    return int(round(time.mktime(date.timetuple()) / 60))


def main():
    #  query the database for just message times and nothing else
    times = con.query("SELECT timestamp FROM messages")
    print ('database query completed')

    print (times.info())

    print (times[timestamp_col].iloc[0])
    print (times[timestamp_col].iloc[-1])
    start_min = get_time(times[timestamp_col].iloc[0])
    end_min = get_time(times[timestamp_col].iloc[-1])
    print (end_min - start_min + 1)

    min_freq = [0] * (end_min - start_min + 1)

    #  for every message time
    for time in times[timestamp_col]:
        #  at index (delta min) increment frequency
        min_freq[get_time(time) - start_min] += 1

    min_axis = np.array(range(start_min, end_min + 1))
    freq_axis = np.array(min_freq)

    plt.plot(min_axis, freq_axis, color='blue', linewidth=1.0, linestyle='-')

    plt.xlim(min_axis.min(), min_axis.max())
    plt.ylim(0, freq_axis.max()*1.1)

    print (range(start_min, end_min + 1, 60))

    #  show ticks every hour
    plt.xticks(np.array(range(start_min, end_min + 1, 60)))
    plt.yticks(np.array(range(0, freq_axis.max(), 100)))

    plt.savefig("figures/test.png", dpi=72)

    plt.show()


if __name__ == '__main__':
    sys.exit(main())

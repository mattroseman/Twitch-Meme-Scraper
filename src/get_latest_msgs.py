#!/usr/bin/python

"""
Script to get latest chat messages from a twitch stream and add them to a file
arguments: (url of twitch site) (how many new messages to grab)
using:
    http://docs.python-guide.org/en/latest/scenarios/scrape/
"""
#  general imports
import sys
#  scrapper imports
from lxml import html
import requests

def main():
    if len(sys.argv) <> 2:
        print 'There are: ', len(sys.argv), ' arguments instead of 2'
        return
    url_string = sys.argv[1]
    num_new_msgs = sys.argv[2]

    page = requests.get(url_string)
    tree = html.fromstring(page.content)


if __name__ == '__main__':
    sys.exit(main())

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
    if len(sys.argv) <> 3:
        print 'There are: ', len(sys.argv) - 1, ' arguments instead of 2'
        return
    url_string = sys.argv[1]
    num_new_msgs = int(sys.argv[2])

    page = requests.get(url_string)
    tree = html.fromstring(page.content)

    messages = tree.xpath('//span[@class="message"]/text()')

    for msg in messages[:num_new_msgs]:
        print 'message: ', msg
        

if __name__ == '__main__':
    sys.exit(main())

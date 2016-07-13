#!/usr/bin/python
import sys, ConfigParser, MySQLdb

config = ConfigParser.RawConfigParser()
config.read('db.cfg')

section_name = 'Database Details'

try:
    db_name = config.get(section_name, 'db_name')
    hostname = config.get(section_name, 'hostname')
    ip_address = config.get(section_name, 'ip_address')
    user = config.get(section_name, 'user')
    password = config.get(section_name, 'password')
except ConfigParser.NoOptionError as e:
    print ('one of the options in the config file has no value\n{0}: ' +
           '{1}').format(e.errno, e.strerror)
    sys.exit()

print ('database name: {0}\nhostname: {1}\nip address: {2}\nuser: {3}\n' +
       'password: {4}').format(db_name, hostname, ip_address, user, password)

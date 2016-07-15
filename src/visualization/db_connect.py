#!/usr/bin/python
import sys, ConfigParser, MySQLdb

class SQLConnection:
    """Used to connect to a SQL database and send queries to it"""
    def __init__(self):
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

        self.db = MySQLdb.connect(host=hostname,
                            user=user,
                            passwd=password,
                            db=db_name)

        self.cur = db.cursor()

    def query(self, query_string):
        """take in a query string and simply pass it on to the database"""
        self.cur.execute(query_string)

        #  an array of arrays that is the query result table
        return self.cur.fetchall()

    def close_connection(self):
        """close the database connection"""
        self.db.close()

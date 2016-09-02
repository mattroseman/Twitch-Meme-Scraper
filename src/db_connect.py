#!/usr/bin/python
import sys, ConfigParser, numpy
import MySQLdb as mdb


class SQLConnection:
    """Used to connect to a SQL database and send queries to it"""
    config_file = 'db.cfg'
    section_name = 'Database Details'

    _db_name = ''
    _hostname = ''
    _ip_address = ''
    _username = ''
    _password = ''

    def __init__(self):
        config = ConfigParser.RawConfigParser()
        config.read(self.config_file)

        try:
            _db_name = config.get(self.section_name, 'db_name')
            _hostname = config.get(self.section_name, 'hostname')
            _ip_address = config.get(self.section_name, 'ip_address')
            _user = config.get(self.section_name, 'user')
            _password = config.get(self.section_name, 'password')
        except ConfigParser.NoOptionError as e:
            print ('one of the options in the config file has no value\n{0}: ' +
                '{1}').format(e.errno, e.strerror)
            sys.exit()

        self.con = mdb.connect(_hostname, _user, _password, _db_name)
        self.con.autocommit(False)
        self.con.ping(True)

        self.cur = self.con.cursor(mdb.cursors.DictCursor)


    def query(self, sql_query, values=None):
        """
        take in 1 or more query strings and perform a transaction
        @param sql_query: either a single string or an array of strings
            representing individual queries
        @param values: either a single json object or an array of json objects
            representing quoted values to insert into the relative query
            (values and sql_query indexes must line up)
        """
        #  TODO check sql_query and values to see if they are lists
        #  if sql_query is a string
        if isinstance(sql_query, basestring):
            self.cur.execute(sql_query, values)
            self.con.commit()
        #  otherwise sql_query should be a list of strings
        else:
            #  execute each query with relative values
            for query, sub_values in zip(sql_query, values):
                self.cur.execute(query, sub_values)
            #  commit all these queries
            self.con.commit()

        return self.cur.fetchall()

    def close(self):
        self.cur.close()

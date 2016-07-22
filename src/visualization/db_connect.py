#!/usr/bin/python
import sys, ConfigParser, sqlalchemy, pandas, numpy


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

        sql_con_string = 'mysql://{0}:{1}@{2}/{3}'.format(_user,
                                                          _password,
                                                          _hostname,
                                                          _db_name)
        self.engine = sqlalchemy.create_engine(sql_con_string)

    def query(self, sql_query):
        """
        take in a query string and simply pass it on to the database
        @param sql_query: an already properly formated SQL query string
        @return: a pandas dataframe object of the query results
        """
        return pandas.read_sql_query(sql_query, self.engine)

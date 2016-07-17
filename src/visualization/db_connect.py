#!/usr/bin/python
import sys, ConfigParser, sqlalchemy, pandas

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

        sql_con_string = 'mysql://{0}:{1}@{2}/{3}'.format(user,
                                                          password,
                                                          hostname,
                                                          db_name)
        self.engine = sqlalchemy.create_engine(sql_con_string)

    def query(self, query_string):
        """
        take in a query string and simply pass it on to the database
        @return: a pandas dataframe object of the query results
        """
        return pandas.read_sql_query(query_string, self.engine)

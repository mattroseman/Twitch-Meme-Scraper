#!/usr/bin/python
import sys, ConfigParser, sqlalchemy, pandas, numpy

_query_buff_size = 10000 #  number of rows for a query chunk

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

    def query(self, table, columns, output_file):
        """
        take in a query string and simply pass it on to the database
        @param table: the name of the database table
        @param columsn: an array of column names or a single column name
        @param output_file: where the csv of the query is put
        @return: a pandas dataframe object of the query results
        """
        query_string = 'SELECT'
        #  if an array of columns have been given
        if isinstance(columns, (list, tuple, numpy.ndarray)):
            for col in columns:
                query_string += ' ' + col
        #  if the columns is just one string
        else:
            query_string += ' ' + columns

        query_string += ' FROM ' + table

        query_index = 0
        num_rows = int(pandas.read_sql_query(('SELECT COUNT(*) FROM ' +
                                             '{0}').format(table),
                                             self.engine)['COUNT(*)'].iloc[0])

        #  clear the output file incase its being reused
        open(output_file, 'w').close()
        while query_index <= num_rows:
            print('reading rows {0} to {1} of {2}'.format(query_index,
                                                          query_index + 
                                                          _query_buff_size,
                                                          num_rows))
            df = pandas.read_sql_query('{0} LIMIT {1}, {2}'.format(query_string,
                                                                   query_index,
                                                                   _query_buff_size),
                                        self.engine)
            df.to_csv(output_file, sep=',', mode='a', encoding='utf-8')
            query_index += _query_buff_size

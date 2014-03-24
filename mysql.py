#!/usr/bin/env python2
# coding: utf-8

import re
import MySQLdb
import ConfigParser

FIELDS = []
FIELDS_TYPE = []

class MySQLHandler:
    def __init__(self):
        self.read_conf()
        try:
            self.conn = MySQLdb.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user, passwd=self.mysql_password)
            self.conn.set_character_set('utf8')
            self.cursor = self.conn.cursor()
            self.cursor.execute('CREATE DATABASE IF NOT EXISTS %s;' % self.mysql_db)
            self.conn.select_db(self.mysql_db)
            schema_sql = self.get_schema(table='test', header=FIELDS, col_types=FIELDS_TYPE)
            self.cursor.execute(schema_sql)
        except Exception, e:
            self.cursor = None
            common.logger.info('Fail to connect to MySQL database: %s' % str(e))

    def read_conf(self):
        """Load settings
        """
        cfg = ConfigParser.ConfigParser()
        cfg.read('setting.ini')

        try:
            self.mysql_host = cfg.get('setting', 'mysql_host')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError), e:
            self.mysql_host = 'localhost'
        try:
            self.mysql_port = int(cfg.get('setting', 'mysql_port').strip())
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError), e:
            self.mysql_port = 3306
        try:
            self.mysql_user = cfg.get('setting', 'mysql_user')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError), e:
            self.mysql_user = 'root'
        try:
            self.mysql_db = cfg.get('setting', 'mysql_db')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError), e:
            self.mysql_db = 'test'

    def get_schema(self, table, header, col_types):
        """Generate the schema for this table from given types and columns
        """
        schema_sql = """CREATE TABLE IF NOT EXISTS %s (
        IcId int(11) NOT NULL AUTO_INCREMENT,""" % table

        for col_name, col_type in zip(header, col_types):
            schema_sql += '\n%s %s DEFAULT NULL,' % (col_name, col_type)
        schema_sql += """\nPRIMARY KEY (Id),
        UNIQUE KEY (`number`)
        ) DEFAULT CHARSET=utf8 ROW_FORMAT=COMPRESSED;"""
        return schema_sql

    def add_row(self, table, bag):
        if self.cursor:
            sql = 'INSERT INTO %s (%s) VALUES(%s);' % (table, ','.join(bag.keys()), ','.join(['%s']*len(bag)))
            self.cursor.execute(sql, tuple(bag.values()))
            self.conn.commit()

    def query_table(self, number):
        if self.cursor:
            sql = 'SELECT url FROM test WHERE number=%s;'
            self.cursor.execute(sql, tuple([number]))
            r = self.cursor.fetchone()
            if not r:
                #如果不存在，就返回0
                return 0
            else:
                return 1

    def update_table(self, par, par_value, update_id, update_value):
        if self.cursor:
            sql = 'UPDATE element14 SET %s = %s WHERE %s =' % (par, par_value, update_id) + '%s;'
            self.cursor.execute(sql, (update_value, ))
            self.conn.commit()

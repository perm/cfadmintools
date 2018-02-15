#!/usr/bin/env python
import sqlite3
from contextlib import contextmanager
import os

class AdminDatabase(object):
    def __init__(self, db_path):
        self.db_path = db_path

    @contextmanager
    def get_connection(self, cursor=False):
        self.conn = sqlite3.connect(self.db_path)
        #self.conn = None
        try:
            if cursor == True:
                yield self.conn.cursor()
            else:
                yield self.conn
            self.conn.commit()
            self.conn.close()
        except (sqlite3.DatabaseError, Exception):
            self.conn.rollback()
            self.conn.close()

    def _execute(self, query):
        with self.get_connection() as connect:
            type(connect)
            connect.execute(query)
        #print 'res is %s' % res
        #return res

    def _execute_script(self, query):
        with self.get_connection() as connect:
            res = connect.executescript(query)
        return res

    def _create_table(self, tablename, query, recreate=False):
        check_exists_query = "SELECT COUNT(*) FROM sqlite_master WHERE name=%s" % tablename
        try:
            exists = self._execute(check_exists_query).fetchone()[0]
        except:
            exists = False

        if not recreate and not exists:
            res = self._execute_script(query)
            return res 
        elif recreate == True:
            drop_table = "DROP TABLE IF EXISTS %s;" % tablename
            query = drop_table + query
            res = self._execute_script(query)
            return res
        else:
            pass


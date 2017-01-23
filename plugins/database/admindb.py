#!/usr/bin/env python
import sqlite3
from contextlib import contextmanager
import os

class AdminDatabase(object):
    def __init__(self, db_path):
        self.db_path = db_path

    @contextmanager
    def get_connection(self, cursor=False):
        conn = sqlite3.connect(self.db_path)
        self.conn = None
        try:
            if cursor == True:
                yield conn.cursor()
            else:
                yield conn
            conn.commit()
            conn.close()
        except (sqlite3.DatabaseError, Exception):
            conn.rollback()
            conn.close()

    def _execute(self, query):
        with self.get_connection() as connect:
            res = connect.execute(query)
        return res

    def _execute_script(self, query):
        with self.get_connection() as connect:
            res = connect.executescript(query)
        return res

    def _create_table(self, tablename, query, recreate):
        check_exists_query = "SELECT COUNT(*) FROM sqlite_master WHERE name=%s" % tablename
        exists = self._execute(check_exists_query).fetchone()[0]

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

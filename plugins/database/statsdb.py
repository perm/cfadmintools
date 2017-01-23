#!/usr/bin/env python

import datetime
from admindb import AdminDatabase
from datetime import timedelta

class StatsDatabase(AdminDatabase):

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        if not os.path.exists(self.db_path) or \
           os.path.getsize(self.db_path) == 0:
            self.create_table_remounted()
        #check for db, setup a connection
        #check for proper schema

    def create_table_remounted(self, recreate=False):
        tablename = 'remounted'
        query = """
            CREATE TABLE %s (
                    created_date TEXT DEFAULT '0',
                    failed_device TEXT,
                    failed_port TEXT,
                    failed_unit TEXT,
                    failed_status TEXT,
                    serial TEXT,
                    model TEXT,
                    firmware TEXT,
                    capacity TEXT,
                    progress INT DEFAULT 1,
                    pager INT DEFAULT 0
            );
                """  % tablename
        
        res =  _create_table(tablename, query, recreate)
        return res




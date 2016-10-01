#!/usr/bin/env python
import sqlite3
from contextlib import contextmanager
import os

class AdminDatabase(object):
    def __init__(self, db_path):
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        self.conn = None
        try:
            yield conn
            conn.commit()
            conn.close()
        except (sqlite3.DatabaseError, Exception):
            conn.rollback()
            conn.close()

    def execute(self, conn, query):
        res = conn.execute(query)
        return res

    def execute_script(self, conn, query):
        res = conn.executescript(query)
        print res
        return res


class FailuresDatabase(AdminDatabase):
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        print "before if"
        if not os.path.exists(self.db_path) or \
           os.path.getsize(self.db_path) == 0:
            print "in if"
            with self.get_connection() as self.conn:
                conn = self.conn
                c = conn.cursor()
                self.create_table_drive_info(c)
                self.create_table_ticket_info(c)
        #check for db, setup a connection
        #check for proper schema
        


    def create_table_drive_info(self, conn, recreate=False):
        query = """select count(*) from sqlite_master where name='drive_info'"""
        if not recreate and not self.execute(conn, query).fetchone()[0]:
            print "matched first if in create_drive_info"
            query = """
                CREATE TABLE drive_info (
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
                    """
            res = self.execute_script(conn, query)
            return res 
             
        elif recreate == True:
            print "matched second if"
            query = """
                DROP TABLE IF EXISTS drive_info;
                CREATE TABLE drive_info (
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
                    """

            res = self.execute_script(conn, query)
            return res
        
        else:
            print "matched last else"
            pass     


    def create_table_ticket_info(self, conn, recreate=False):
        query = """select count(*) from sqlite_master where name='ticket_info'"""
        if not recreate and not self.execute(conn, query).fetchone()[0]:
            print "matched first if in create_ticket_info"
            query = """
                   CREATE TABLE ticket_info (
                        ticket_number TEXT PRIMARY KEY,
                        created_date TEXT DEFAULT '0',
                        server_number INT,
                        server_name TEXT,
                        server_type TEXT,
                        datacenter TEXT,
                        core_account_id INT,
                        core_account_name TEXT,
                        failed_device TEXT,
                        failed_unit TEXT,
                        failed_port TEXT,
                        error_type TEXT,
                        ticket_status INT DEFAULT 1,
                        pager INT DEFAULT 0
                    );
                """ 
            res = self.execute(conn, query)
            return res

        elif recreate == True:
            print "matched second if"
            query = """                    
                    DROP TABLE IF EXISTS ticket_info;
                    CREATE TABLE ticket_info (
                         ticket_number TEXT PRIMARY KEY,
                         created_date TEXT DEFAULT '0',
                         server_number INT,
                         server_name TEXT,
                         server_type TEXT,
                         datacenter TEXT,
                         core_account_id INT,
                         core_account_name TEXT,
                         failed_device TEXT,
                         failed_unit TEXT,
                         failed_port TEXT,
                         error_type TEXT,
                         ticket_status INT DEFAULT 1,
                         pager INT DEFAULT 0
                     );
                    """
            res = self.execute_script(conn, query)
            return res

        else:
            pass

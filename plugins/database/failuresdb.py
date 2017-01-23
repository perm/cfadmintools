#!/usr/bin/env python

from admindb import AdminDatabase

class FailuresDatabase(AdminDatabase):

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        if not os.path.exists(self.db_path) or \
           os.path.getsize(self.db_path) == 0:
            self.create_table_drive_info()
            self.create_table_ticket_info()
        #check for db, setup a connection
        #check for proper schema

    def create_table_drive_info(self, recreate=False):
        tablename = 'drive_info'
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

    def create_table_ticket_info(self, recreate=False):
        tablename = 'ticket_info'
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
                """  % tablename

        res =  self._create_table(tablename, recreate)
        return res

    def insert_drive_info(self, date_id, device, collected_data):
        tablename = 'drive_info'
        query = """
            INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s
                                  %s, %s, %s, %s, %s);
                                                   """   % (tablename,
                                                            date_id,
                                                            device['name'],
                                                            device['port'],
                                                            device['unit'],
                                                            collected_data['status'],
                                                            collected_data['serial'],
                                                            collected_data['model'],
                                                            collected_data['firmware'],
                                                            collected_data['capacity'],
                                                            1,
                                                            0)
        
        res = self._execute(self, query)
        return res
  
    def insert_ticket_info(self, date_id, ticket,
                           server_info, device, device_info):
        tablename = 'ticket_info'
        query = """
            INSERT INTO %s VALUES(%s %s, %s, %s, %s, %s, %s, %s,
                                  %s, %s, %s, %s, %s, %s, %s);
                                                           """ % (tablename,
                                                                  str(ticket),
                                                                  date_id,
                                                                  server_info['server'],
                                                                  server_info['server_name'],
                                                                  server_info['platform'],
                                                                  server_info['datacenter'],
                                                                  server_info['customer'],
                                                                  server_info['customer_name'],
                                                                  device['name'],
                                                                  device['unit'],
                                                                  device['port'],
                                                                  device_info['status'],
                                                                  ticket_status,
                                                                  pager)
        
        res = self._execute(self, query)
        return res

    def isdevice_inprogress(self, device):
        tablename = 'drive_info'
        query = """
            SELECT count(*) FROM tablename WHERE
               failed_device=%s
               and (progress=1 or progress=2);
                                         """ % (tablename,
                                                device['name'])
        
        res = self._execute(self, query)

        if res.fetchone()[0]:
            return True
        else:
            return False 
                                                
    def get_inprogress_tickets():
        tablename = 'ticket_info'
        query = """
             SELECT ticket_number, created_date, 
             server_number, datacenter, failed_device, 
             failed_unit, failed_port from ticket_info
             WHERE ticket_status = 1
             ORDER BY failed_unit
                                """
        res = self._execute(self, query).fetchall()
         
        if len(res) == 0:
              return
        else:
            tablename = 'drive_info'
            rows = []
            for tkt in res:
                query = "SELECT model from %s WHERE created_date = %s" % (tablename, tkt[1])
                model = self._execute(self, query).fetchone()
                rows.append(tkt + model)

            return rows
   
    def get_failed_drive(device='None'):
        tablename = 'drive_info'
        if device == 'None':
            query = """
                 SELECT created_date, failed_device,
                 failed_port, failed_unit from %s
                 WHERE progress = 2
                                  """ % tablename
        else:
            query = """
                 SELECT created_date, failed_device,
                 failed_port, failed_unit from %s
                 WHERE failed_device = %s and failed_port = %s
                 and progress = 2
                                """ % (tablename, device['name'], device['port'])

        res = self._execute(self, query).fetchall()
        return res

    def get_failed_ticket(date_id='None'):
        tablename = 'ticket_info'
        if data_id == 'None':
            query = """
                 SELECT ticket_number, created_date,
                 failed_port, failed_unit from %s
                 WHERE ticket_status = 2
                                        """ % tablename

        
        else:
            query = """
                SELECT ticket_number, created_date,
                server_number, failed_device,
                failed_port, failed_unit from %s
                WHERE created_date = %s and ticket_status = 2
                                                             """ % (tablename, date_id)

        res = self._execute(self, query).fetchall()
        return res


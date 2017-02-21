#!/usr/bin/env python
import ConfigParser

class parseConfig(object):
    def __init__(self, configfile):
        #try:
   
            self.config = ConfigParser.ConfigParser()
            self.configfile = configfile
            self.config.read(self.configfile)
        #except:
        #    print "no config found"

    def get_admintools_homedir(self):
        try:
            homedir = self.config.get('admintools', 'homedir')
            return homedir
        except:
            return '/etc/swift-admintools'
            
    def get_admintools_failures_database(self):
        try:
            database = self.config.get('admintools', 'database')
            return database
        except:
            return '/etc/swift-admintools/failures.db'
    
    def get_admintools_template_dir(self):
        try:
            template_dir = self.config.get('admintools', 'template_dir')
            return template_dir
        except:
            return '/etc/swift-admintools/templates'

    def get_controller_type(self):
        try:
            c_type = self.config.get('controller', 'controller_type')
            return c_type.lower()
        except:
            return None 
    
    def get_controller_binary(self):
        try:
            c_binary = self.config.get('controller', 'controller_binary')
            return c_binary.lower()
        except:
            return None
    
    def get_secondary_controller(self):
        try:
            c_type = self.config.get('controller', 'secondary_controller')
            return c_type.lower()
        except:
            return None

    def get_secondary_controller_binary(self):
        try:
            c_binary = self.config.get('controller', 'secondary_controller_binary')
            return c_binary.lower()
        except:
            return None

    def get_enclosure_model(self):
        try:
            enclosure =  self.config.get('enclosure', 'enclosure_model')
            return enclosure.lower()
        except:
            return None

    def get_ticketing_type(self):
        try:
            ticketing_type = self.config.get('ticketing', 'ticketing_type')
            return ticketing_type.lower()
        except:
            return None

    def get_ticket_requester(self):
        try:
            ticket_requester = self.config.get('ticketing', 'ticket_requester')
            return ticket_requester.lower()
        except:
            return None
    
    def get_ticket_user(self):
        try:
            ticket_user = self.config.get('ticketing', 'ticket_user')
            return ticket_user
        except:
            return None

    def get_ticket_pass(self):
        try:
            ticket_pass = self.config.get('ticketing', 'ticket_pass')
            return ticket_pass
        except:
            return None 

if __name__ == '__main__':
    p = parseConfig('admintools.conf')
    q = parseConfig('admintools2.conf')
    print p.get_controller_type()
    print p.get_controller_binary()
    print p.get_admintools_homedir()
    print p.get_admintools_failures_database()
    print p.get_admintools_template_dir()
    print p.get_secondary_controller()
    print p.get_secondary_controller_binary()
    print p.get_enclosure_model()
    print q.get_controller_type()
    print p.get_ticketing_type()
    print p.get_ticket_requester()
    print p.get_ticket_user()
    print p.get_ticket_pass()


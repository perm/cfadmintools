#!/usr/bin/env python
import ConfigParser
import re

global root_device

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
    
    def get_controller_device_mounts(self):
        #try:
           d = {}
           c_dm = self.config.get('controller', 'device_mounts')
           c = c_dm.split(',')
           device_configuration = c[0]
           #print device_configuration
           device_mounts = c[-1].split(',')
           d['drive_config'] = device_configuration
           device_mount_regex = [re.compile(items) for items in device_mounts]
           #print device_mounts
           #print device_mount_regex
           return c
        #except:
        #   return None
    
    def get_controller_exclude_mounts(self):
        c_em = self.config.get('controller', 'exclude_mounts_file')
        f = open(c_em)
        exclude_mounts = f.read().split(',')
        exclude_mounts[-1] = exclude_mounts[-1].rstrip('\n')
        return exclude_mounts
    
    def get_secondary_controller(self):
        try:
            c_type = self.config.get('secondary_controller', 'controller_type')
            return c_type.lower()
        except:
            return None

    def get_secondary_controller_binary(self):
        try:
            c_binary = self.config.get('secondary_controller', 'controller_binary')
            return c_binary.lower()
        except:
            return None

    def get_secondary_controller_device_mounts(self):
        try:
           sc_dm = self.config.get('secondary_controller', 'device_mounts')
           return sc_dm
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
    p = parseConfig('/home/jbrown/cfadmintools/plugins/common/swift_admintools.conf')
    #q = parseConfig('admintools2.conf')
    print 'controller_type = %s' % (p.get_controller_type())
    print 'controller_binary = %s' % (p.get_controller_binary())
    print 'homedir = %s' % (p.get_admintools_homedir())
    print 'database = %s' % p.get_admintools_failures_database()
    print 'template_dir = %s' % p.get_admintools_template_dir()
    print 'controller_type = %s' % p.get_secondary_controller()
    print 'controller_binary = %s' % p.get_secondary_controller_binary()
    print 'enclosure_model = %s' % p.get_enclosure_model()
    print 'ticketing_type = %s' % p.get_ticketing_type()
    print 'ticket_requester = %s' % p.get_ticket_requester()
    print 'ticket_user = %s' % p.get_ticket_user()
    print 'ticket_pass = %s' % p.get_ticket_pass()
    print 'device_mounts = %s' % p.get_controller_device_mounts()
    print 'secondary_device_mounts = %s' % p.get_secondary_controller_device_mounts()
    print 'exclude_device_mounts = %s' % p.get_controller_exclude_mounts()

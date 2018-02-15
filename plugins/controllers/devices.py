#!/usr/bin/env python
import os
import re
from  ..common.config import parseConfig 
from pprint import pprint

class Devices(object):
    '''
    Returns a dict with the controllers and devices on the controllers that should be monitored
    '''
    def __init__(self):
        p = parseConfig('/home/jbrown/cfadmintools/plugins/common/swift_admintools.conf')    
        self.controller = p.get_controller_type()
        self.controller_exclude_mounts = p.get_controller_exclude_mounts()
        self.controller_device_mounts = p.get_controller_device_mounts()
        ##print 'self.controller_device_mounts is %s' % self.controller_device_mounts
        self.devices = {'controller_type': self.controller,
                         'single':[],
                         'raid':[]  } 

    def get_devices_to_monitor(self):

        for item in self.controller_device_mounts:
            ##print 'item is %s' % item
            l = item.split(':')
            ##print 'l is %s' % l
            volume_type = l[0].lower()
            ##print 'volume_type is %s' % volume_type
            dev_path = l[1]
            devices = dev_path.split('/')[-1]
            dev_path_list = dev_path.split('/')[:-1]

            path = ''
            for dir in  dev_path_list:
                path = path + dir + '/'

            
            device_regex = re.compile(devices)
            dev_dir = os.listdir(path)
            ##print 'dev_dir is %s' % dev_dir
            all_devices = filter(device_regex.match, dev_dir)
            ##print 'all_devices is %s' % all_devices
            for dev in all_devices:
                self.devices[volume_type.lstrip()].append(path + dev)
            #self.devices[volume_type] = all_devices

        #for item in self.controller_exclude_mounts
        #pprint(self.devices)
        ##print 'self.controller_exclude_mounts: %s' % self.controller_exclude_mounts 
        exclude_device_regex = [re.compile(i) for i in self.controller_exclude_mounts]
        ##print 'exclude_device_regex: %s ' % exclude_device_regex
        exclude_devices_found = []
        for search_pattern in exclude_device_regex:
            match_single = filter(search_pattern.match, self.devices['single'])
            if match_single:
                for device in match_single:
         #           #print 'device is %s' % device
                    exclude_devices_found.append(device)
        ##print exclude_devices_found
        for excluded_device in exclude_devices_found:
            if excluded_device in self.devices['single']:
                self.devices['single'].remove(excluded_device)
      #rewrite this to use a function          
        for excluded_device in exclude_devices_found:
            if excluded_device in self.devices['raid']:
                self.devices['raid'].remove(excluded_device)
        return self.devices       
        ##print 'self.devices %s' % self.devices
        #for excluded_device in exclude_devices_found:
        #    if excluded_device in self.devices['single']:
         #       #print '%s in self.devices' % excluded_device
         #   else:
         #       #print '%s NOT in self.devices' % excluded_device
            #match_raid = filter(search_pattern, self.device['raid'])                       

    def check_device_mounts(self):
        '''return a list of unmounted devices'''
        unmounted = []
        d = Devices.get_devices_to_monitor(self)
        for device in self.devices['single']:
            if not os.path.ismount(device):
                unmounted.append(device)
        return unmounted

if __name__ == '__main__':
    d = Devices()
    #print d.get_devices_to_monitor()
    print d.check_device_mounts()


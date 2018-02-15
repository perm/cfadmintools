#!/usr/bin/env python
import os
import re
from  ..common.config import parseConfig
from pprint import pprint

class Devices(object):
    def __init__(self):
        p = parseConfig('/home/jbrown/cfadmintools/plugins/common/swift_admintools.conf')
        self.controller = p.get_controller_type()
        self.controller_device_mounts = p.get_controller_device_mounts()
        self.devices = {'controller_type': self.controller,
                         'single':[],
                         'raid':[]  }
        for item in self.controller_device_mounts:
            l = item.split(':')
            volume_type = l[0].lower()
            dev_path = l[1]
            devices = dev_path.split('/')[-1]
            dev_path_list = dev_path.split('/')[:-1]

            path = ''
            for dir in  dev_path_list:
                path = path + dir + '/'


            device_regex = re.compile(devices)
            dev_dir = os.listdir(path)
            all_devices = filter(device_regex.match, dev_dir)
            self.devices[volume_type] = all_devices
            pprint(self.devices)
        #c = self.controller_device_mounts.split(',')
        #for item in c:
        #    l = item.split(':')
        #    print l[-1]

if __name__ == '__main__':
    d = Devices()


#!/usr/bin/env python

import re
import subprocess
from admin_os import AdminOS
from pprint import pprint

class Pmc8885qController(object):

    #def __init__(self, config_dict, logger):
    #    self.config = config_dict
    #    self.logger = logger
    #    self.arcconf_path = self.config['pmc8885q']['arcconf_path']
    #    self.device_root = self.config.get('device_root', '/srv/node')
    #    self.admin = AdminOS()
    def get_ld_info(self, controller, device, binary='/usr/bin/arcconf'):
        '''
        :param controller
        :param device
        :binary location of arcconf raid util
        :returns a dict with logical disk information
        '''
        device = device.split('u')[1]
        a = AdminOS()
        stdout,stderr = a.run('%s getconfig %s LD %s' % (binary,
                                                         controller,
                                                         device))
        device_info = stdout.split('\n')[5:-8]
        segment_info = stdout.replace(',','').replace(')', '').split('\n')[-6].split('(')[1].split()
        ld_info = {}
        for item in device_info:
            if item.endswith('--'):
                continue
            else:
                item = item.split(':')
                key = item[0].lstrip().rstrip().lower()
                value = item[1].lstrip().lower()
                ld_info[key] = value
        ld_info['pd_size'] =  segment_info[0].lower()
        ld_info['interface'] = segment_info[1].lower()
        ld_info['drive_type'] = segment_info[2].lower()
        ld_info['enclosure'] = segment_info[3].split(':')[1]
        ld_info['slot'] = segment_info[4].split(':')[1]
        ld_info['serial'] = segment_info[5].lower()
        return ld_info

    def _fetchall_pd_info(self, controller, binary='/usr/bin/arcconf'):
        '''
        puts output of an arcconf pd listing into a consumable form.
        :param controller
        :param device
        :binary location of arcconf raid util
        :returns a list of dictionaries that container a dictionary of 
         device attributes
        '''
        a = AdminOS()
        pd_list = []
        stdout,stderr = a.run('%s getconfig %s PD' % (binary,
                                                      controller))
        res = re.split(" +Device\ #", stdout)
        for item in res:
            device_id = item.split('\n')[0]
            if re.search('^\d+$', device_id):
                d = {}
                for attr in item.split('\n'):
                    if ':' in attr:
                        try:
                            p = attr.split(' :')
                            key = p[0].lstrip().rstrip().lower()
                            value = p[1].lstrip().lower()
                            d[key] = value
                        except IndexError:
                            continue
                dev_info={device_id: d}
                pd_list.append(dev_info)

        return pd_list

    def get_pd_info(self, pd, controller):

if __name__ == '__main__':
    p = Pmc8885qController()
    #ld_info = p.get_ld_info('1', 'c1u1')
    #pprint(ld_info)

    pd_info = p._fetchall_pd_info('1')
    pprint(pd_info)

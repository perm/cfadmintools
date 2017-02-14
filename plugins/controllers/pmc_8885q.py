#!/usr/bin/env python

import re
import subprocess
from admin_os import AdminOS
from storage_enclosures import Enclosure
from pprint import pprint

class Pmc8885qController(object):
    def __init__(self, enclosure, binary='/usr/bin/arcconf'):
        self.enclosure = enclosure
        self.binary = binary
        self.admin = AdminOS()
        #self.logger = logger


    def blink_device(self, controller, device, pd=False):
       if pd:
           pd_loc = Pmc8885qController.derive_pd(self, device)
           device = '%s %s' % (pd_loc[0], pd_loc[1])
           stdout,stderr = self.admin.run('%s IDENTIFY %s DEVICE %s start' % (self.binary,
                                                                              controller,
                                                                              device))
           print stdout

       else:
           device = device.split('u')[1]
           stdout,stderr = self.admin.run('%s IDENTIFY %s LOGICALDRIVE %s start' % (self.binary,
                                                                                    controller,
                                                                                    device))
           print stdout

    def unblink_device(self, controller, device, pd=False):
        if pd:
            pd_loc = Pmc8885qController.derive_pd(self, device)
            device = '%s %s' % (pd_loc[0], pd_loc[1])
            stdout,stderr = self.admin.run('%s IDENTIFY %s DEVICE %s stop' % (self.binary,
                                                                              controller,
                                                                              device))
            print stdout
        else:
            device = device.split('u')[1]
            stdout,stderr = self.admin.run('%s IDENTIFY %s LOGICALDRIVE %s stop' % (self.binary,
                                                                                    controller,
                                                                                    device))
            print stdout
            

    def derive_pd(self, device):
       '''
       device: 'a string such as c1u1'
       returns: list of the channel and device for specified device
       '''
       j = Enclosure(self.enclosure)
       rdevice = int(device.split('u')[1])
       if rdevice > (j.drive_count()) - 1:
           #logger
           print 'invalid drive'
           return
       pd = j.derive_physical_id('8885Q', device).split(" ")
       return pd
       
    def get_pd_info(self, controller, device):         
        '''
        '''
        pd_data = Pmc8885qController._fetchall_pd_info(self,controller)
        pd_loc = Pmc8885qController.derive_pd(self, device)
        for pd_pool in pd_data:
            for dev in pd_pool:
               if pd_loc[1] in pd_pool[dev]['reported channel,device(t:l)']:
              #if '58' in pd_pool[dev]['reported channel,device(t:l)']:
                   pprint(pd_pool[dev]) 


    def uninit(self, controller, device):
        #The uninitialize command clears Adaptec meta-data and any OS partitions from a drive; 
        #existing data on the drive is destroyed. Drives can uninitialized only if they are in 
        #the Raw or Ready state (that is, not part of any logical drive). A drive in the Raw 
        #state has no Adaptec meta-data but may or may not have an OS partition.
        #e.g arcconf UNINIT 1 0 16
        stdout,stderr = self.admin.run('%s UNINIT %s %s' %  (self.binary,
                                                             controller))

    def uninit_all(self, controller):
        #The uninitialize command clears Adaptec meta-data and any OS partitions from a drive; 
        #existing data on the drive is destroyed. Drives can uninitialized only if they are in 
        #the Raw or Ready state (that is, not part of any logical drive). A drive in the Raw 
        #state has no Adaptec meta-data but may or may not have an OS partition.
        #e.g arcconf UNINIT 1 ALL
        stdout,stderr = self.admin.run('%s UNINIT %s ALL' %  (self.binary,
                                                              controller))

    def remove_ld(self, controller, device):
        #Deletes a logical drive, JBOD, or maxCache logical device. 
        #All data stored on the logical drive or JBOD will be lost
        '''
        :param controller
        :param device
        :returns a boolean. True on success, False on failure.
        '''
        device = device.split('u')[1]
        stdout,stderr = self.admin.run('%s DELETE %s LOGICALDRIVE %s' % (self.binary,
                                                                         controller,
                                                                         device))
        if stderr:
            return False
        else:
            return True

    def get_ld_info(self, controller, device):
        '''
        :param controller
        :param device
        :returns a dict with logical disk information
        '''
        device = device.split('u')[1]
        stdout,stderr = self.admin.run('%s getconfig %s LD %s' % (self.binary,
                                                                  controller,
                                                                  device))
        try:
            device_info = stdout.split('\n')[5:-8]
        except:
            #no device info was found
            return {}
        try:
            segment_info = stdout.replace(',','').replace(')', '').split('\n')[-6].split('(')[1].split()
        except:
            segment_info = False #no segment info was discovered
        ld_info = {}
        for item in device_info:
            if item.endswith('--'):
                continue
            else:
                item = item.split(':')
                key = item[0].lstrip().rstrip().lower()
                value = item[1].lstrip().lower()
                ld_info[key] = value
        if segment_info:
            ld_info['pd_size'] =  segment_info[0].lower()
            ld_info['interface'] = segment_info[1].lower()
            ld_info['drive_type'] = segment_info[2].lower()
            ld_info['enclosure'] = segment_info[3].split(':')[1]
            ld_info['slot'] = segment_info[4].split(':')[1]
            ld_info['serial'] = segment_info[5].lower()
        else:
            ld_info['pd_size'] = 'na'
            ld_info['interface'] = 'na'
            ld_info['drive_type'] = 'na'
            ld_info['enclosure'] = 'na'
            ld_info['slot'] = 'na'
            ld_info['serial'] = 'na'

        return ld_info

    def _fetchall_pd_info(self, controller):
        '''
        puts output of an arcconf pd listing into a consumable form.
        :param controller
        :param device
        :returns a list of dictionaries that contai a dictionary of 
         device attributes
        '''
        pd_list = []
        stdout,stderr = self.admin.run('%s getconfig %s PD' % (self.binary,
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


if __name__ == '__main__':
    p = Pmc8885qController('sc847')
    ld_info = p.get_ld_info('1', 'c1u20')
    pprint(ld_info)
    
    pd_info = p._fetchall_pd_info('1')
    pprint(pd_info)
    #p.remove_ld('1','c1u25') 
    #p.get_pd_info('1', 'c1u44', 'sc847')
    #print(p.derive_pd('c1u44', 'sc847'))
    #p.blink_device('1', 'c1u44', 'sc847')
    #p.unblink_device('1', 'c1u44', 'sc847')
    #p.blink_device('1', 'c1u44', 'sc847', pd=True)
    #p.unblink_device('1', 'c1u44', 'sc847', pd=True)


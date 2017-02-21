#!/usr/bin/env python

import re
import subprocess
from admin_os import AdminOS
from pprint import pprint

class StorageController(object):
    def __init__(self, controller_type, controller_id, enclosure, binary=None):
        self.controller_type = controller_type.lower()
        self.controller_id = controller_id
        self.enclosure = enclosure
        self.binary = binary 
        select_module = {'8885q':  'aacraid',
                         'h810':   'megaraid_sas_dell',
                         'h710':   'megaraid_sas_dell',
                         'p840':   'hpsa',
                         'h244br': 'hpsa',
                         'aacraid': 'aacraid',
                         'megaraid_sas_dell' : 'megaraid_sas_dell'}
        module = select_module.get(controller_type, None)
        if module == 'aacraid':
            from aacraid import AacraidController
            if self.binary:
                self.controller = AacraidController(self.controller_id, self.enclosure, binary=self.binary)
            else:
                self.controller = AacraidController(self.controller_id, self.enclosure)
        
        elif module == 'megaraid_sas_dell':
            from megaraid_sas import MegaraidSasDellController
        
        elif module == 'hpsa':
            from hpsa import HpsaController

    def get_logical_device(self, device, native=False):
        #if native:
        ld = self.controller.get_ld_info(device)
        return ld

    def get_physical_device(self, device, native=False):
        pd = self.controller.get_pd_info(device)
        return pd
   
    def blink_device(self, device, pd=False):
        if pd:
            self.controller.blink_device(device, pd=True)
        else:
            self.controller.blink_device(device)
    
    def create_logical_device(self, device, pd=False):
        if pd:
            self.controller.create_ld(device, pd=True)
        else:
            self.controller.create_ld(device)
    
    def delete_logical_device(self, device):
        result = self.controller.remove_ld(device)
        return result

if __name__ == '__main__':
    p = StorageController('8885q', '1', 'sc847')
    #pprint(p.get_logical_device('c1u26'))
    pprint(p.get_physical_device('c1u26'))

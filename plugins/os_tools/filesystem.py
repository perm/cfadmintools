#!/usr/bin/env python


class Filesystem(object):
    def __init__(self, device, device_size=None):
        self.device = device
        self.device_size = device_size

class Xfs(Filesystem): 
    def repair(self, memory=2048, xfs_repair_path='/usr/local/sbin/xfs_repair_v4.5'):
        cmd = '/usr/local/sbin/xfs_repair_v4.5 -m %s /dev/%s' % (memory, self.device)
        print cmd    
    
    def create(self, block_size='4096', s_size='4096', label=True):
        if label:
            cmd = 'mkfs.xfs -b size=%s -s size=%s  -f -L %s /dev/%sp1' % (block_size, 
                                                                          s_size, 
                                                                          self.device, 
                                                                          self.device)
        else:
            cmd = 'mkfs.xfs -b size=%s -s size=%s  -f /dev/%sp1' % (block_size, 
                                                                    sector_size, 
                                                                    self.device)
        print cmd


class Partition(object):
    def __init__(self, device, parted_path='/sbin/parted', fs='xfs'):
        self.device = device
        self.parted_path = parted_path
        self.fs = fs
    
    def make_label(self):
        cmd = '%s -s /dev/%sp mklabel gpt' % (self.parted_path, 
                                              self.device)
        print cmd
    
    def make_part(self):
        cmd = '%s -s /dev/%sp mkpart primary %s 40s 100%%' % (self.parted_path, 
                                                             self.device,
                                                             self.fs)     	                                                   print cmd


if __name__ == '__main__':
    xfs = Xfs('c1u1')
    xfs.repair(memory=4096)
    xfs.create('c1u1')

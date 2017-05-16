#!/usr/bin/env python
from admin_os import AdminOS

class Filesystem(object):
    def __init__(self, device, device_size=None):
        self.device = device
        self.device_size = device_size
        self.admin = AdminOS()

class Xfs(Filesystem):
    def repair(self, memory=2048, xfs_repair_path='/usr/local/sbin/xfs_repair_v4.5'):
        stdout,stderr = self.admin.run('/usr/local/sbin/xfs_repair_v4.5 -m %s /dev/%s' % (memory, self.device))

    def create(self, block_size='4096', s_size='4096', label=True):
        if label:
            stdout,stderr = self.admin.run('mkfs.xfs -b size=%s -s size=%s  -f -L %s /dev/%sp1' % (block_size,
                                                                                                   s_size,
                                                                                                   self.device,
                                                                                                   self.device))
        else:
            stdout,stderr = self.admin('mkfs.xfs -b size=%s -s size=%s  -f /dev/%sp1' % (block_size,
                                                                                         sector_size,
                                                                                         self.device))


class Partition(object):
    def __init__(self, device, parted_path='/sbin/parted', fs='xfs'):
        self.device = device
        self.parted_path = parted_path
        self.fs = fs
        self.admin = AdminOS()

    def make_label(self):
        stdout,stderr = self.admin.run('%s -s /dev/%sp mklabel gpt' % (self.parted_path,
                                                                       self.device))


    def make_part(self):
        stdout,stderr = self.admin.run('%s -s /dev/%sp mkpart primary %s 40s 100%%' % (self.parted_path,
                                                                                       self.device,
                                                                                       self.fs))


if __name__ == '__main__':
    #part = Partition('c2u28')
    #xfs = Xfs('c2u28')
    #part.make_label()
    #part.make_part()
    #xfs.create()
    #xfs.repair(memory=4096)
    #xfs.create('c1u1')


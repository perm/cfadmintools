#!/usr/bin/env python
import subprocess
from swift.common.ring.ring import Ring
import sys

class Swift(object):
    def __init__(self, ring):
        ring = ring.lower()
        if ring == 'account':
            self.ring = Ring('/etc/swift/account.ring.gz')
        elif ring == 'container':
            self.ring = Ring('/etc/swift/container.ring.gz')
        elif ring == 'object':
            self.ring = Ring('/etc/swift/object.ring.gz')
        else:
            print 'Please provide ring type, \"account, container, or object\"'
            sys.exit(1)

        p = subprocess.Popen(['ip', 'addr'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        for item in stdout.split():
            if item.startswith('172'):
                if item.endswith('255'):
                    continue
                self.ip = item.split('/')[0]

                print self.ip
        self.ring_data = self.ring.devs


    def isweight_zero(self, device):
        for dev in self.ring.devs:
            try:
                if dev['ip'] == self.ip and dev['device'] == device:
                    if dev['weight'] == 00.0:
                        return True
                    else:
                        return False
            except TypeError:
                continue

def main():
    s = Swift('object')
    for drive in range(44):
        weight = s.isweight_zero('c1u%s' % drive )
        if weight:
            print 'c1u%s' % drive

if __name__ == '__main__':
    main()
:

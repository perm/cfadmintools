#!/usr/bin/env python

class Jbod(object):
    '''
    '''
    def __init__(self, jbod_model):
        if jbod_model.lower() == 'sc847':
            self.jbod_model = jbod_model
            self.drives = 45

    def derive_physical_id(self, controller_model, device):

        device_number = int(device.split('u')[1])
        if int(device_number) > self.drives - 1:
            raise ValueError("Invalid device: %s" % device)
        if controller_model.lower() == '8885q' and self.jbod_model == 'sc847':
            physical_location = '0 %s' % (16 + device_number)
        elif controller_model.lower() == 'h810' and self.jbod_model == 'sc847':
            x, y = divmod(int(device_number), 24)
            physical_location = '%d:0:%d' % (x, y)
        else:
            return None

        return physical_location

    def drive_count(self):
        return self.drives

if __name__ == '__main__':
    f = Jbod('sc847')
    l = f.derive_physical_id('8885Q', 'c1u1')
    print l
    x = Jbod('sc847')
    m = x.derive_physical_id('H810', 'c2u34')
    print m
    print(x.drive_count())


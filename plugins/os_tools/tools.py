#!/usr/bin/env python
import subprocess
import shlex
import os
import pwd
import grp
import sys
import fileinput

class AdminOS(object):
    def run(self, cmd):
        run_cmd = shlex.split(cmd)
        p = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        returncode = p.returncode
        return stdout, stderr, returncode

    def mount(self, device, label=True, mount_path='/bin/mount', mount_dest=None):
        if label:
            cmd = '%s LABEL=%s' % (mount_path, device)
        elif mount_dest is not None:
            cmd = '%s /dev/%s %s' % (mount_path, device, mount_dest)
        self.run(cmd)

    def chown(self, device, user='swift', group='swift', path='/srv/node/'):
        uid = pwd.getpwnam(user).pw_uid
        gid = grp.getgrnam(group).gr_gid
        path = path + device
        print 'os.chown(%s, %s, %s)' % (path, uid, gid)

    def uncomment_fstab(self, device, fstab_path='/etc/fstab'):
        label_good = False
        try:
            for line in fileinput.input(fstab_path, inplace=1):
                if 'LABEL=%s ' % (device) in line:
                    if line.startswith('#'):
                        line = line.lstrip('#')
                        logger.info("Uncommented %s in %s" % (label, fstab_path))
                    if line.startswith('LABEL=%s ' % (device)):
                        label_good = True
                sys.stdout.write(line)
        except (OSError,IOError) as e:
            #logger.error(str(e))
            label_good = False

            return label_good

    def get_mount_points(self, dir='/srv/node'):
        return os.listdir(dir)
   
    def get_raw_device_name(self, device, devdir='/dev/'):
        return os.readlink(devdir + device + 'p')
            

    def get_servernumber(self):
        f = open('/root/.servernumber')
        servernumber = f.read()
        f.close()
        return servernumber

if __name__ == '__main__':
    i = AdminOS()
    dirs = i.get_mount_points()
    print dirs
    raw_dev = i.get_raw_device_name('c1u25')
    print raw_dev


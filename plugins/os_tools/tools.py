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
        return stdout, stderr

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
            except (OsError, IOError) as e:
                #logger.error(str(e))
                label_good = False
            
            return label_good 
          

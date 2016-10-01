#!/usr/bin/env python

import subprocess
import shlex

class AdminOS(object):
    def run(self, cmd):
        run_cmd = shlex.split(cmd)
        subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return stdout, stderr

#!/usr/bin/env python

import xmlrpclib
import json
import os
import sys

class Core(object):
    def __init__(self, core_user, core_pass):
        self.core_user = core_user
        self.core_pass = core_pass

class Core_xmlrpc(Core):
    def __init__(self, core_user, core_pass, core_server='https://ws.core.rackspace.com/xmlrpc'):
        self.core_user = core_user
        self.core_pass = core_pass
        self.core_server = core_server
        self.auth = xmlrpclib.ServerProxy('%s/Auth' % self.core_server)        
        try:
            self.auth_token = json.load(open('/tmp/.core_token'))
        except:
            self.auth_token =  self.auth.systemLogin(self.core_user, self.core_pass)
            f = open('/tmp/.core_token','w')
            f.write(json.dumps(self.auth_token))
            f.close()
            print 'im here'
        
        if self.auth.isTokenValid(self.auth_token) == 1:
           print 'token %s is valid' % self.auth_token
          
        else:
           print 'token %s is invalid' % self.auth_token 
           try:
               self.auth_token =  self.auth.systemLogin(self.core_user, self.core_pass)
               f = open('/tmp/.core_token','w')
               f.write(json.dumps(self.auth_token))
               f.close()
           except:
               print 'there was an exception I\'m leaving'
               sys.exit(1) 
        
        self.core_url = self.core_server + self.auth_token


class Core_ctkapi(Core):
    pass

if __name__ == '__main__':

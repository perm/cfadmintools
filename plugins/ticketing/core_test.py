#!/usr/bin/env python
from coreclient.exceptions import CoreError, CoreHttpError
from coreclient.client import CoreClient
import json

user = 'cfiles'
password = 'DXkQ!6-8Y/X2'

client = CoreClient('https://ws.core.rackspace.com/ctkapi/',user=user, password=password)
client.auth()

resp = client.query({"class": "Account.Account",
              "load_arg": "923088",
              "attributes": [
                   {
                   "id": "name",
                   "attribute": "computers",
                   "subattributes": [
                   "platform.name",
                   "number",
                   "status.name"]
                   }
               ]
})
servers = resp
#servers = resp['result'][0]['computers.number']
print servers['result']

#for server in servers.keys()
#    print server

#resp = client.query({"class": "Computer.Computer",
#                     "load_arg":"769254",
#                     "attributes": [
#                         "account",
#                          "datacenter",]
#                     })

#print resp

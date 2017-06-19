#!/usr/bin/env python

import xmlrpclib
import json
import os
import sys
from pprint import pprint

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

    def get_server_info(self, server_number):
        """
        Retrieves information about a server from CORE

        :param server_number: Core server number
        :param auth_token: Core Token

        :returns: A dictionary with server information and error code
        """
        
        try:
            server = xmlrpclib.ServerProxy('%s/Computer/::session_id::'
                                            % self.core_server + self.auth_token)
            server_details = server.getDetailsByComputers([server_number])

            if len(server_details):
                desired_keys = ['server', 'server_name', 'datacenter',
                                'customer', 'customer_name', 'team',
                                'segment', 'platform', 'status']
                server_picked_details = {}
                for key in desired_keys:
                    server_picked_details[key] = server_details[0][key]
                return server_picked_details               
        except:
            print "couldn't get details"

    
    def create_server_ticket(self, server_number, ticket_template):

        print ticket_template
        # Ticket Attributes
        # 2288:Hardware, 13503: Hard drive
        category_id = 2288
        subcategory_id = 13503
        severity_id = 2
        is_private = False
        private_first_message = False
        assignee = 0
        send_message_text = True
        status = 1
        contact_email_type = 1
        priority = 1
        recipients = []
        requester_id = 847350
        self.ticket_subject = ticket_template['subject']
        self.ticket_body = ticket_template['body']

        queue_ids = {'DFW1': {'name': 'DCOPS (DFW1)', 'id': 49},
                     'DFW2': {'name': 'DCOPS (DFW2/DFW3)', 'id': 475},
                     'DFW3': {'name': 'DCOPS (DFW2/DFW3)', 'id': 475},
                     'ORD1': {'name': 'DCOPS (ORD1)', 'id': 391},
                     'LON3': {'name': 'DCOPS (LON3)', 'id': 189},
                     'SYD2': {'name': 'DCOPS (SYD2)', 'id': 523},
                     'IAD3': {'name': 'DCOPS (IAD3)', 'id': 525},
                     'HKG1': {'name': 'DCOPS (HKG1)', 'id': 197},
                     'cloudfs_ops': {'name': 'Cloud Files Ops', 'id': 413},
                     'cloud_infra': {'name': 'CLOUD INFRASTRUCTURE', 'id': 360}}



        #try:
        ticket = xmlrpclib.ServerProxy('%s/Ticket/::session_id::'
                                             % self.core_server + self.auth_token)
         
        server_info = Core_xmlrpc.get_server_info(self, server_number)

        ticket_number = ticket.createTicket(
                #queue_ids[server_info['datacenter']]['id'],
                413,
                severity_id, subcategory_id, self.ticket_subject, self.ticket_body,
                is_private, private_first_message, recipients,
                requester_id, int(server_info['customer']),
                [server_number], assignee, send_message_text,
                status, contact_email_type, priority)
        return str(ticket_number)
        #except:
        #print 'unable to create ticket'

    def get_ticket_details(self, ticket_number):
        ticket = xmlrpclib.ServerProxy('%s/Ticket/::session_id::'
                                        % self.core_server + self.auth_token)
        ticket_info = ticket.getTicketInfo(str(ticket_number))
        return ticket_info

    def close_ticket(self, ticket_number, queue_id=413):
        #try:
        ticket = xmlrpclib.ServerProxy('%s/Ticket/::session_id::'
                                            % self.core_server + self.auth_token)

        ticket_info = ticket.closeTicket(str(ticket_number), 4834)
        return ticket_info 
        #except:
        #    print 'unable to close ticket'

    def get_queues(self):
        try:
            server = xmlrpclib.ServerProxy('%s/Ticket/::session_id::'
                                            % self.core_server + self.auth_token)
            ticket_queues = server.getQueues()
            return ticket_queues
        except:
            print "couldn't get details"


class Core_ctkapi(Core):
    pass

if __name__ == '__main__':
    #server = c.get_server_info('734937')
    #pprint(server)
    #message = {'subject': 'admintools 2.0 test',
    #           'body': 'This is an admintools 2.0 test message'}
    #ticket_number = c.create_server_ticket('734937', message)
    #print ticket_number
    ticket_details = c.get_ticket_details('170614-11055') 
    print ticket_details
    ticket_close = c.close_ticket('170614-11055')
    print ticket_close

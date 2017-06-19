#!/usr/bin/env python
from jinja2 import Environment, FileSystemLoader

class Ticket(object):
    def __init__(self, template_file, template_path='/Users/jbrown/personal/templates'):
        self.template_file = template_file
        self.template_path = template_path
        self.env = Environment(loader=FileSystemLoader(template_path))
    
    def render_template(self, context):
        template = self.env.get_template(self.template_file)
        ticket = template.render(context)
        return ticket 
    

if __name__ == '__main__':
    #env = jinja2.Environment(loader=jinja2.FileSystemLoader('/Users/jbrown/personal/templates'))
    #env.get_template('first_template.tpl')
    #template = env.get_template('first_template.tpl')
    #print template.render()
    
    t = Ticket('first_template.tpl')
    context = {'firstname': 'Jon', 
               'lastname': 'Brown'}
    print t.render_template(context)
    

    t = Ticket('hp380g9_sc847.tpl')
    context = {'firmware': 'mfaoaa70',
               'id': '0,60(60:0)',
               'model': 'hgst hus724040al',
               'serial': 'pn2334peh5687t',
               'size': '4.0 TB',
               'state': 'online',
               'device': 'c1u1',
               'slot': '4'}

    print t.render_template(context)

*** DCOPS - READ THE ACCOUNT MANAGEMENT GUIDELINES BEFORE WORKING ON THE TICKET ***

WARNING: CUSTOMER DATA IS AT INCREASED RISK WHILE THIS DRIVE IS DOWN REPLACE IT ASAP

PLEASE NOTE: 
- CloudFiles storage node drives do not use raid
- The "Cloud Files Ops" Queue is NOT A MONITORED queue
- If you need to ask anything about this ticket please call or email cfteam@lists.rackspace.com

Hello,

This server has a failed drive(s) to be replaced. This is the position:

- JBOD connected to Adaptec PMC 8885Q Controller on PCI Slot {{ slot }}
- Physical location:  {{ id }} 
- Virtual Disk Label: {{ device }}
- Product ID: {{ model }}
- Serial number: {{ serial }}
- Capacity : {{ size }}
- The indicator light has been turned on

Please remember that Slot Number is the PCI location of the *CONTROLLER* not the drive.

If you need more details, please check the link below if needed. At the bottom there is an ASCII diagram that shows how things are connected.

https://dcwiki.rackspace.com/wiki/Cloud_Files_storage_arrays#HP_DL380_G9

These drives are hot swappable and can be replaced at anytime without bringing the system down.

Please put this ticket back in the Cloud Files Ops queue when you're done.

Thanks,

CloudFiles Operations Team
OnCall HuntGroup: 700-5990 or 210-312-5990
Email: cfteam@lists.rackspace.com

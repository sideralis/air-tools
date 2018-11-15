#!/usr/local/bin/python2.7
# encoding: utf-8
'''
dev_manager -- Add new devices in IBM database

dev_manager is a tool used to add new device (mac and token) in IBM bluemix database

It defines classes_and_methods

@author:     Bernard Gautier

@copyright:  2018 Ochrin. All rights reserved.

@license:    None

@contact:    bernard.gautier@ochrin.com
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from cloudant import Cloudant
import json

__all__ = []
__version__ = 0.1
__date__ = '2018-11-15'
__updated__ = '2018-11-15'

TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Bernard Gautier on %s.
  Copyright 2018 Ochrin. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-m", "--mac", help="mac address of device")
        parser.add_argument("-t", "--token", help="token of device")

        # Process arguments
        args = parser.parse_args()

        mac = args.mac
        token = args.token

        print("Connecting to database...")
        db_name = 'air-device-db'
        client = None
        db = None
        mydir = os.path.dirname(os.path.realpath(__file__))
        
        if os.path.isfile(os.path.join(mydir,'vcap-local.json')):
            with open(os.path.join(mydir,'vcap-local.json')) as f:
                vcap = json.load(f)
                creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
                user = creds['username']
                password = creds['password']
                url = 'https://' + creds['host']
                client = Cloudant(user, password, url=url, connect=True)
                db = client.create_database(db_name, throw_on_exists=False)
        else:
            print("DB not found or created")
            print("%s", os.getcwd())
            print("%s", os.path.dirname(os.path.realpath(__file__)))
            return -1
        
        print("Connected.")
        
        if mac in db:
            print("Device already in db")
            print("END.")
            return 0

        print("Adding device with mac address = ", mac, " and token = ", token)

        data = {
            '_id':mac,
            'token':token,
            'owner_email':'',
            'date_reg':'',
            'place':''
        }
        if client:
            my_document = db.create_document(data)
            if my_document.exists():
                print("Device added")
                print("END.")

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0

if __name__ == "__main__":
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'dev_manager_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
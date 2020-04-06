## module beacon.admin_cli
 
import sqlite3
from sqlite3 import Error
#import beacon.common
#import beacon.database
#import pyvcf
#import sys #?
#import argparse

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-ct","--create_table", 
                    help="according to a given sql command it creates new table in database",
                    action="store_true")
parser.add_argument("-id","--insert_data", 
                    help="according to a given sql command it inserts data in database",
                    action="store_true")

args = parser.parse_args()
if args.create_table:
    print("create table is activated")
if args.insert_data:
    print("inserting data is activated")
    
def _main_(args):
    """ interacts with admin and connects function """
    pass
 
#nct: def export_db()
print("hier angekommen")


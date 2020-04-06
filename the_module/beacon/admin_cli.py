## module beacon.admin_cli
 
import sqlite3
from sqlite3 import Error
import admin_cli
import argparse
#import beacon.common
import database
import pyvcf
import argparse

def __main__(args):
    
    connectparser = argparse.ArgumentParser(prog='admin', fromfile_prefix_chars='@')
    parser.add_argument("-ct","--create_table", 
                        help="according to a given sql command it creates new table in database",
                        action="store_true", 
                        nargs=1
                        )
    parser.add_argument("-vcf","--insert_data", 
                        help="according to a given sql command it inserts data from a vcf file in database",
                        action="store_true", 
                        nargs='?', 
                        type=file,
                        required=True
                        )
    parser.add_argument("-fd","--find_dup", 
                        help="according to a given sql command it finds duplicated data in database",
                        action="store_true", 
                        nargs=1)
    parser.add_argument("-p","--print_db", 
                        help="according to a given sql command it prints the database",
                        action="store_true", 
                        nargs=1)
    parser.add_argument("-c","--count_variants", 
                        help="according to a given sql command it counts the variants in database",
                        action="store_true", 
                        nargs=1)
    parser.add_argument("-u","--update", 
                        help="according to a given sql command it finds duplicated data in database",
                        action="store_true", 
                        nargs=5) 
    parser.add_argument("-d","--delete", 
                        help="according to a given sql command it finds duplicated data in database",
                        action="store_true", 
                        nargs=1)



#environmental variable 
    connect = database.ConnectDatabase(os.environ.get("PATH_DATABASE"))

    args = parser.parse_args()

    if args.create_table:
        print("create table is activated")
        print(admin_tools.create_tables(connect))

    if args.insert_data: 
        print("inserting data is activated")
        infile = input("vcf file: ")
        print(parse_vcf(infile))

    if args.find_dup:
        print("create table is activated")
        print(admin_tools.find_dup(connect))

    if args.print_db:
        print("create table is activated")
        print(admin_tools.print_db(connect))
    
    if args.count_variants:
        print("create table is activated")
        print(admin_tools.count_variants(connect))

    if args.update: -u chr pos 
        print("create table is activated")
        variants = input("chr, pos, ref, alt, id: ")
        print(admin_tools.update(connect,variants))

    if args.delete:
        print("create table is activated")
        print(admin_tools.delete(connect,id)


    connect.connection.close()

# total changes von sql 



 
#nct: def export_db()
print("hier angekommen")

if __name__==if __name__ == "__main__":
    pass

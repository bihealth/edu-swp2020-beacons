## module beacon.admin_cli
 
import sqlite3
from sqlite3 import Error
#import admin_tools
from . import admin_tools
import argparse
#import database
from . import database
import vcf, sys, os 

# def parse_args(args):
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-ct","--create_table", 
#                         action = 'store_true',
#                         help="according to a given sql command it creates new table in database")
#     parser.add_argument("-vcf","--insert_data",
#                         help="according to a given sql command it inserts data from a vcf file in database",
#                         type=argparse.FileType('r'))
#     parser.add_argument("-fd","--find_dup",  
#                         action = 'store_true',
#                         help="according to a given sql command it finds duplicated data in database")
#     parser.add_argument("-p","--print_db",  
#                         action = 'store_true',
#                         help="according to a given sql command it prints the database")
#     parser.add_argument("-c","--count_variants",  
#                         action = 'store_true',
#                         help="according to a given sql command it counts the variants in database")
#     parser.add_argument("-u","--update", 
#                         help="according to a given sql command it update data in database",
#                         nargs = 5) 
#     parser.add_argument("-d","--delete",  
#                         help="according to a given sql command it deletes data in database")
#     return parser.parse_args(args)



def main(args):
    #db_path:input()
    connect = database.ConnectDatabase('/Users/leylanur/edu-swp2020-beacons/the_module/beacon/database.db') 
    od = admin_tools.OperateDatabase()
    if args.create_table:
        print("create table is activated")
        create = admin_tools.CreateDbCommand()
        return(create.create_tables(connect))
    elif args.insert_data:
        print("inserting data is activated")
        return(admin_tools.parse_vcf(args.insert_data, connect))
    elif args.find_dup:
        print("find_dup is activated")
        finddup = admin_tools.SearchDuplicatesCommand() 
        return(finddup.find_dup(connect))
    elif args.print_db:
        print("print_db is activated")
        return(od.print_db(connect))
    elif args.count_variants:
        print("count_variants is activated")
        return(od.count_variants(connect))
    elif args.update: 
        print("update is activated")  
        return(od.updating_data(connect,tuple(args.update)))
    elif args.delete:
        print("delete is activated")
        return(od.delete_data(connect,str(args.delete)))
    connect.connection.close()


    # parser = argparse.ArgumentParser()
    # parser.add_argument("-ct","--create_table", 
    #                     action = 'store_true',
    #                     help="according to a given sql command it creates new table in database")
    # parser.add_argument("-vcf","--insert_data",
    #                     help="according to a given sql command it inserts data from a vcf file in database",
    #                     type=argparse.FileType('r'))
    # parser.add_argument("-fd","--find_dup",  
    #                     action = 'store_true',
    #                     help="according to a given sql command it finds duplicated data in database")
    # parser.add_argument("-p","--print_db",  
    #                     action = 'store_true',
    #                     help="according to a given sql command it prints the database")
    # parser.add_argument("-c","--count_variants",  
    #                     action = 'store_true',
    #                     help="according to a given sql command it counts the variants in database")
    # parser.add_argument("-u","--update", 
    #                     help="according to a given sql command it update data in database",
    #                     nargs = 5) 
    # parser.add_argument("-d","--delete",  
    #                     help="according to a given sql command it deletes data in database")

    # #PATH_DATABASE = "/home/namuun/edu-swp2020-beacons/the_module/beacon/database.db"
    # #PATH_DATABASE = input('PATH_DATABASE: ')
    # connect = database.ConnectDatabase('/home/namuun/edu-swp2020-beacons/the_module/beacon/database.db') 
    # args = parser.parse_args()
    # od = admin_tools.OperateDatabase()
    # if args.create_table:
    #     print("create table is activated")
    #     create = admin_tools.CreateDbCommand()
    #     print(create.create_tables(connect))
    #     #print(admin_tools.create_tables(connect))
    # elif args.insert_data:
    #     print("inserting data is activated")
    #     print(admin_tools.parse_vcf(args.insert_data, connect))
    # elif args.find_dup:
    #     print("find_dup is activated")
    #     finddup = admin_tools.SearchDuplicatesCommand() 
    #     print(finddup.find_dup(connect))
    # elif args.print_db:
    #     print("print_db is activated")
    #     print(od.print_db(connect))
    # elif args.count_variants:
    #     print("count_variants is activated")
    #     print(od.count_variants(connect))
    # elif args.update: 
    #     print("update is activated")  
    #     print(od.updating_data(connect,tuple(args.update)))
    # elif args.delete: parser = argparse.ArgumentParser()
    # parser.add_argument("-ct","--create_table", 
    #                     action = 'store_true',
    #                     help="according to a given sql command it creates new table in database")
    # parser.add_argument("-vcf","--insert_data",
    #                     help="according to a given sql command it inserts data from a vcf file in database",
    #                     type=argparse.FileType('r'))
    # parser.add_argument("-fd","--find_dup",  
    #                     action = 'store_true',
    #                     help="according to a given sql command it finds duplicated data in database")
    # parser.add_argument("-p","--print_db",  
    #                     action = 'store_true',
    #                     help="according to a given sql command it prints the database")
    # parser.add_argument("-c","--count_variants",  
    #                     action = 'store_true',
    #                     help="according to a given sql command it counts the variants in database")
    # parser.add_argument("-u","--update", 
    #                     help="according to a given sql command it update data in database",
    #                     nargs = 5) 
    # parser.add_argument("-d","--delete",  
    #                     help="according to a given sql command it deletes data in database")

    # args = parser.parse_args()
    #     print("delete is activated")
    #     print(od.delete_data(connect,tuple(args.delete)))
    
    # connect.connection.close()
    # return parser.parse_args(args)

# print("hier in admin_client angekommen")
if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-ct","--create_table", 
                        action = 'store_true',
                        help="according to a given sql command it creates new table in database")
    parser.add_argument("-vcf","--insert_data",
                        help="according to a given sql command it inserts data from a vcf file in database",
                        type=argparse.FileType('r'))
    parser.add_argument("-fd","--find_dup",  
                        action = 'store_true',
                        help="according to a given sql command it finds duplicated data in database")
    parser.add_argument("-p","--print_db",  
                        action = 'store_true',
                        help="according to a given sql command it prints the database")
    parser.add_argument("-c","--count_variants",  
                        action = 'store_true',
                        help="according to a given sql command it counts the variants in database")
    parser.add_argument("-u","--update", 
                        help="according to a given sql command it update data in database",
                        nargs = 5) 
    parser.add_argument("-d","--delete",  
                        help="according to a given sql command it deletes data in database")

    args = parser.parse_args()
    print(main(args))

   # parser = parse_args(sys.argv[1:])
    #main(args)
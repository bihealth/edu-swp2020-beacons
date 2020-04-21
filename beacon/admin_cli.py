"""
...to maintain the database
"""

import sqlite3
from sqlite3 import Error
from . import admin_tools
import argparse
from . import database
import vcf, sys, os


def path():
    """
    Asks for a path to the database.db for maintaining the Database.

    :return: path 
    """
    db_path = input("DB Path: ")
    # db_path = '/Users/leylanur/edu-swp2020-beacons/the_module/beacon/database.db'
    return db_path


def parse_args(args):
    """
    Defines the flags.
    
    :param args: the flag which was entered in the command line
    :return: parser 
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-ct",
        "--create_table",
        action="store_true",
        help="according to a given sql command it creates new table in database",
    )
    parser.add_argument(
        "-vcf",
        "--insert_data",
        help="according to a given sql command it inserts data from a vcf file in database",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "-fd",
        "--find_dup",
        action="store_true",
        help="according to a given sql command it finds duplicated data in database",
    )
    parser.add_argument(
        "-p",
        "--print_db",
        action="store_true",
        help="according to a given sql command it prints the database",
    )
    parser.add_argument(
        "-c",
        "--count_variants",
        action="store_true",
        help="according to a given sql command it counts the variants in database",
    )
    parser.add_argument(
        "-u",
        "--update",
        help="according to a given sql command it update data in database",
        nargs=5,
    )
    parser.add_argument(
        "-d",
        "--delete",
        help="according to a given sql command it deletes data in database",
    )
    return parser.parse_args(args)


def main(pfad, args):
    """
    Maintaining the Database.
    
    :param pfad: the path to the database.db
    :param args: the flag which was entered in the command line
    :return: Whether the maintenance of the database was successful
    """
    connect = database.ConnectDatabase(pfad)
    od = admin_tools.OperateDatabase()
    if args.create_table:
        print("create table is activated")
        create = admin_tools.CreateDbCommand()
        return create.create_tables(connect)
    elif args.insert_data:
        print("inserting data is activated")
        return admin_tools.parse_vcf(args.insert_data, connect)
    elif args.find_dup:
        print("find_dup is activated")
        finddup = admin_tools.SearchDuplicatesCommand()
        return finddup.find_dup(connect)
    elif args.print_db:
        print("print_db is activated")
        return od.print_db(connect)
    elif args.count_variants:
        print("count_variants is activated")
        return od.count_variants(connect)
    elif args.update:
        print("update is activated")
        return od.updating_data(connect, tuple(args.update))
    elif args.delete:
        print("delete is activated")
        return od.delete_data(connect, str(args.delete))
    connect.connection.close()


if __name__ == "__main__":  # pragma: nocover
    pfad = path()
    args = parse_args(sys.argv[1:])
    sys.exit(print(main(pfad, args)))

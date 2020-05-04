"""
...to maintain the database
"""

from . import admin_tools
import argparse
from . import database
import sys  # vcf, sys, os


def path():
    """
    Asks for a path to the database.db for maintaining the Database.
    :return: path
    """
    db_path = input("DB Path: ")
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
        nargs=3,
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
        "-ua",
        "--update_allel",
        help="according to a given sql command it update data in database",
        nargs=9,
    )
    parser.add_argument(
        "-up",
        "--update_populations",
        help="according to a given sql command it update data in database",
        nargs=10,
    )
    parser.add_argument(
        "-upt",
        "--update_phenotype",
        help="according to a given sql command it update data in database",
        nargs=5,
    )
    parser.add_argument(
        "-da",
        "--delete_allel",
        help="according to a given sql command it deletes data in database",
    )
    parser.add_argument(
        "-dp",
        "--delete_populations",
        help="according to a given sql command it deletes data in database",
    )
    parser.add_argument(
        "-dpt",
        "--delete_phenotype",
        help="according to a given sql command it deletes data in database",
    )
    parser.add_argument(
        "-ctu",
        "--create_table_user",
        action="store_true",
        help="according to a given sql command it creates new table in 'user'-database",
    )
    parser.add_argument(
        "-add",
        "--insert_user_data",
        help="according to a given sql command it adds the user in the database",
        nargs=2
    )
    parser.add_argument(
        "-t",
        "--find_token",
        help="according to a given sql command it finds the token for the associated username in database",
    )
    parser.add_argument(
        "-pu",
        "--print_user_db",
        action="store_true",
        help="according to a given sql command it prints the database",
    )
    parser.add_argument(
        "-du",
        "--delete_user_db",
        help="according to a given sql command it prints the database"
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
    us = admin_tools.UserDB()
    if args.create_table:
        print("create table is activated")
        create = admin_tools.CreateDbCommand()
        output = create.create_tables(connect)
    elif args.insert_data:
        print("inserting data is activated")
        output = admin_tools.parse_vcf(args.insert_data, connect)
    elif args.print_db:
        print("print_db is activated")
        output = od.print_db(connect)
    elif args.count_variants:
        print("count_variants is activated")
        output = od.count_variants(connect)
    elif args.update_allel:
        print("update is activated")
        output = od.updating_allel(connect, args.update)
    elif args.update_populations:
        print("update is activated")
        output = od.updating_populations(connect, args.update)
    elif args.update_phenotype:
        print("update is activated")
        output = od.updating_phenotype(connect, args.update)
    elif args.delete_allel:
        print("delete is activated")
        output = od.delete_allel(connect, args.delete)
    elif args.delete_populations:
        print("delete is activated")
        output = od.delete_populations(connect, args.delete)
    elif args.delete_phenotype:
        print("delete is activated")
        output = od.delete_phenotype(connect, args.delete)
    elif args.create_table_user:
        print("create user table is activated")
        output = us.create_tables(connect)
    elif args.insert_user_data:
        print("inserting user data is activated")
        output = us.addusers(args.insert_user_data, connect)
    elif args.find_token:
        print("find_token is activated")
        output = us.find_user_token(connect, args.find_token)
    elif args.print_user_db:
        print("print_user_db is activated")
        output = us.print_db(connect)
    elif args.delete_user_db:
        print("delete_user_db is activated")
        output = us.delete_user(connect, args.delete_user_db)
    else:
        output = "Please enter a flag. To see which flags you can use, use -h or --help"
    connect.connection.close()  # pragma: nocover
    return output


if __name__ == "__main__":  # pragma: nocover
    pfad = path()
    args = parse_args(sys.argv[1:])
    sys.exit(print(main(pfad, args)))

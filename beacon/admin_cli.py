"""
...to maintain the database
"""

from . import admin_tools
import argparse
from . import database
import sys
import os


def path():
    """
    Asks for a path to the database.db for maintaining the Database.

    :return: bool if succeeded, path or error string
    """
    try:
        exist = False
        try_count = 0
        while exist is False:
            if try_count > 10:
                print("You tried more then ten times. Your session is quitted now.")
                return False, ""
            try_count = try_count + 1
            db = input("DB Name: ")
            path = os.path.dirname(__file__)
            if os.path.exists(os.path.join(path, db)) is True:
                return True, os.path.join(path, db)
            else:
                inp = input(
                    "Given database does not exist. Do you want to create a new one? [y/n]"
                )
                if inp == "y":
                    return True, os.path.join(path, db)
                elif inp == "n":
                    ex = input("Do you want to exit the process? [y/n]")
                    if ex == "y":
                        return False, ""
                    elif ex == "n":
                        print("The process is starting from the beginning.")
                    else:
                        print(
                            "Your input has the wrong format. The process is starting from the beginning."
                        )
                else:
                    print(
                        "Your input has the wrong format. The process is starting from the beginning."
                    )
    except Exception as e:  # pragma nocover
        return False, e


def parse_args(args):
    """
    Defines the flags.

    :param args: the flag which was entered in the command line
    :return: parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-ct",
        "--create_tables",
        action="store_true",
        help="Creating new tables in database.",
    )
    parser.add_argument(
        "-vcf",
        "--insert_data",
        help="Inserting data from a tsv and vcf file in database",
        nargs=1,
    )
    parser.add_argument(
        "-p", "--print_db", action="store_true", help="Printing the database",
    )
    parser.add_argument(
        "-c",
        "--count_variants",
        action="store_true",
        help="Counting the variants in database.",
    )
    parser.add_argument(
        "-ua", "--update_allel", help="Updating the allel data in database.", nargs=10,
    )
    parser.add_argument(
        "-up",
        "--update_populations",
        help="Updating the population data in database.",
        nargs=11,
    )
    parser.add_argument(
        "-upt",
        "--update_phenotype",
        help="Updating the phenotype data in database.",
        nargs=6,
    )
    parser.add_argument(
        "-da", "--delete_allel", help="Deleting allel data in database.",
    )
    parser.add_argument(
        "-dp", "--delete_populations", help="Deleting population data in database.",
    )
    parser.add_argument(
        "-dpt", "--delete_phenotype", help="Deleting phenotype data in database.",
    )
    parser.add_argument(
        "-ctu",
        "--create_tables_user",
        action="store_true",
        help="Creating two new tables in 'user'-database.",
    )
    parser.add_argument(
        "-add", "--insert_user", help="Adding an user in the database.", nargs=2,
    )
    parser.add_argument(
        "-t",
        "--find_user_token",
        help="Finding the token for the associated username in database.",
    )
    parser.add_argument(
        "-pu",
        "--print_db_user",
        action="store_true",
        help="Printing the user database.",
    )
    parser.add_argument(
        "-du", "--delete_user", help="Deleting the user database.",
    )
    parser.add_argument(
        "-pi", "--print_ip", action="store_true", help="Printing the ip database.",
    )
    parser.add_argument(
        "-di", "--delete_ip", help="Deleting the ip database.",
    )
    return parser.parse_args(args)


def main(argv):
    """
    Maintaining the Database.

    :param argv: the name to the database.db and the flag which was entered in the command line
    :return: Whether the maintenance of the database was successful
    """
    pfad_test = path()
    if pfad_test[0] is True:
        pfad = pfad_test[1]
    else:
        return pfad_test[1]  # pragma: nocover
    args = parse_args(sys.argv[1:])
    try:
        with database.ConnectDatabase(pfad) as connect:
            od = admin_tools.OperateDatabase()
            us = admin_tools.UserDB()
            if args.create_tables:
                print("create tables is activated")
                create = admin_tools.CreateDbCommand()
                output = create.create_tables(connect)
            elif args.insert_data:
                print("inserting data is activated")
                output = admin_tools.parse_vcf(args.insert_data[0], connect)
            elif args.print_db:
                print("print_db is activated")
                output = od.print_db(connect)
            elif args.count_variants:
                print("count_variants is activated")
                output = od.count_variants(connect)
            elif args.update_allel:
                print("update is activated")
                output = od.updating_allel(connect, args.update_allel)
            elif args.update_populations:
                print("update is activated")
                output = od.updating_populations(connect, args.update_populations)
            elif args.update_phenotype:
                print("update is activated")
                output = od.updating_phenotype(connect, args.update_phenotype)
            elif args.delete_allel:
                print("delete is activated")
                output = od.delete_allel(connect, args.delete_allel)
            elif args.delete_populations:
                print("delete is activated")
                output = od.delete_populations(connect, args.delete_populations)
            elif args.delete_phenotype:
                print("delete is activated")
                output = od.delete_phenotype(connect, args.delete_phenotype)
            elif args.create_tables_user:
                print("create user table is activated")
                output = us.create_tables_user(connect)
            elif args.insert_user:
                print("inserting user data is activated")
                output = us.insert_user(args.insert_user, connect)
            elif args.find_user_token:
                print("find_user_token is activated")
                output = us.find_user_token(connect, args.find_user_token)
            elif args.print_db_user:
                print("print_db_user is activated")
                output = us.print_db_user(connect)
            elif args.delete_user:
                print("delete_user is activated")
                output = us.delete_user(connect, args.delete_user)
            elif args.print_ip:
                print("print_ip is activated")
                output = us.print_ip(connect)
            elif args.delete_ip:
                print("delete_ip is activated")
                output = us.delete_ip(connect, args.delete_ip)
            else:
                output = "Please enter a flag. To see which flags you can use, use -h or --help"
        return output
    except Exception as e:  # pragma: nocover
        return "An error has occured: " + str(e)


if __name__ == "__main__":  # pragma: nocover
    main(sys.argv)

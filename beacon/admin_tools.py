"""
...that maintain the database
"""

import sqlite3
import vcf


def parse_vcf(infile, con):
    """
    Reads VCF file and inserts the data into a database.

    :param infile: a vcf file
    :param con: connection to the database
    :rtype: bool
    """
    vcf_reader = vcf.Reader(infile)
    for variant in vcf_reader:  # pragma: nocover
        # give to datenbank (sql_str)
        chr = variant.CHROM
        pos = str(variant.POS)
        ref = variant.REF
        alt = "".join(str(i or "") for i in variant.ALT)
        sql_str = "INSERT INTO variants (chr,pos,ref,alt) VALUES (?,?,?,?);"
        parameters = (chr, pos, ref, alt)
        output = con.parse_statement(sql_str, parameters)
        if type(output) != list:
            return output
    return True
    infile.close()  # pragma: nocover


class CreateDbCommand:
    """
    Creates variant table in database.
    """

    def __init__(self):
        self.data = []

    def create_tables(self, con):
        """
        Creates variant table in database.

        :param con: connection to the database
        :rtype: bool
        """
        sql_create_db_table = "CREATE TABLE IF NOT EXISTS variants ( id integer ?, chr text ?, pos integer ?, ref text ?, alt text ?;)"

        parameters = (
            "PRIMARY KEY AUTOINCREMENT",
            "NOT NULL",
            "NOT NULL",
            "NOT NULL",
            "NOT NULL",
        )
        output = con.parse_statement(sql_create_db_table, parameters)
        if type(output) == sqlite3.Error:  # pragma: nocover
            return output
        else:
            return True


class SearchDuplicatesCommand:
    """
    Looks for duplicates in the database and prints them.
    """

    def __init__(self):
        self.data = []

    def find_dup(self, con):
        """
        Looks for duplicates in the database and shows them.

        :param con: connection to the database
        :return: list with duplications
        :rtype: list
        """
        sql_find_dup = "SELECT id, chr, pos, COUNT(*) FROM variants GROUP BY chr, pos, ref, alt HAVING COUNT(*) > 1;"
        output = con.parse_statement(sql_find_dup, ())
        if type(output) != list:  # pragma: nocover
            return output
        return output


class OperateDatabase:
    """
    Provides tools to maintain the database.
    """

    def __init__(self):
        self.data = []

    def print_db(self, con):
        """
        Prints whole database.

        :param con: connection to the database
        :return: database
        """
        sql_print = "SELECT id, chr, pos, ref, alt FROM variants GROUP BY id, chr, pos, ref, alt"
        output = con.parse_statement(sql_print, ())
        if type(output) != list:  # pragma: nocover
            print(output)
            return False
        else:
            for out in output:
                print(out)
            return ""

    def count_variants(self, con):
        """
        Counts the existing number of (all) Variants.

        :param con: connection to the database
        :rtype: int
        """
        sql_count_var = "SELECT COUNT(*) FROM variants"
        output = con.parse_statement(sql_count_var, ())
        if type(output) != list:  # pragma: nocover
            print(output)
            return False
        else:
            return int(output[0][0])

    def updating_data(self, con, variants):
        """
        Updates a row in the database according to given id and input.

        :param con: connection to the database
        :param variant : chr, pos, ref, alt, id
        :rtype: bool
        """
        chr = variants[0]
        pos = variants[1]
        ref = variants[2]
        alt = variants[3]
        id = variants[4]
        sql_str = (
            "UPDATE variants SET chr = ?, pos = ?, ref = ?, alt = ? WHERE id = ? ;"
        )
        parameters = (chr, pos, ref, alt, id)
        output = con.parse_statement(sql_str, parameters)
        if type(output) != list:  # pragma: nocover
            print(output)
            return False
        else:
            print("rufe -p auf, um die Änderung zu sehen")
            return True

    def delete_data(self, con, id):
        """
        Deletes a row with given id in the database.

        :param con: connection to the database
        :param id: id
        :rtype: bool
        """

        sql_str = "DELETE FROM variants WHERE id= ?;"
        parameters = str(id)
        output = con.parse_statement(sql_str, parameters)
        if type(output) != list:
            print(output)
            return False
        else:
            print("rufe -p auf, um die Änderung zu sehen")
            return True


# nct: def export_db() + def print_row() + def count
# für version 2:
# - Kommas einlesen, bei alt in der funktion parse_vcf
# - ersetzen von database vcf
# - create table geht nicht in dieser form mit ????
# - update muss verbessert werden  id 100000 wird akzeptiert ?? -.-
# - bei der funktion find_dup -> automatisch löschen
# - 5 x updadte variablen benennen bei -h update -u U U U U U
# - in der funktion update und delete noch das ergebnis printen

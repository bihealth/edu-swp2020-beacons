"""
...that maintain the database
"""

import sqlite3
import vcf
import csv


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

        alt_homo = variant.num_hom_alt
        wildtype = variant.num_hom_ref
        alt_hetero = variant.num_het

        if chr == "Y":  # was ist mit der X chr von männlichen samples?
            hemi_ref = wildtype
            hemi_alt = alt_hetero
        else:
            hemi_alt = 0
            hemi_ref = 0

        sql_str = "INSERT INTO allel (chr,pos,ref,alt, wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt) VALUES (?,?,?,?,?,?,?,?,?);"
        parameters = (
            chr,
            pos,
            ref,
            alt,
            wildtype,
            alt_hetero,
            alt_homo,
            hemi_ref,
            hemi_alt,
        )
        output = con.parse_statement(sql_str, parameters)
        if type(output) != list:
            return output
    infile.close()  # pragma: nocover
    return True


def parse_tsv(infile, con):
    with open(infile) as tsv_file:
        # tsv_reader = csv.reader(tsv_file, delimiter="\t")
        tsv_reader = csv.DictReader(tsv_file, dialect="excel-tab")
        count = 0
        for row in tsv_reader:
            print(row["Sample name"])

            count = count + 1
            if count == 8:
                break

    tsv_file.close()
    return True


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
        sql_create_db_table_allel = """
            CREATE TABLE IF NOT EXISTS allel (
            id integer PRIMARY KEY AUTOINCREMENT,
            chr text NOT NULL,
            pos integer NOT NULL,
            ref text NOT NULL,
            alt text NOT NULL,
            wildtype integer NOT NULL,
            alt_hetero integer NOT NULL,
            alt_homo integer NOT NULL,
            hemi_ref integer NOT NULL,
            hemi_alt integer NOT NULL
        );"""
        sql_create_db_table_populations = """
            CREATE TABLE IF NOT EXISTS populations (
            id integer PRIMARY KEY AUTOINCREMENT,
            chr text NOT NULL,
            pos integer NOT NULL,
            ref text NOT NULL,
            alt text NOT NULL,
            wildtype integer NOT NULL,
            alt_hetero integer NOT NULL,
            alt_homo integer NOT NULL,
            hemi_ref integer NOT NULL,
            hemi_alt integer NOT NULL,
            population text NOT NULL
        );"""
        sql_create_db_table_phenotype = """
            CREATE TABLE IF NOT EXISTS phenotype (
            id integer PRIMARY KEY AUTOINCREMENT,
            chr text NOT NULL,
            pos integer NOT NULL,
            ref text NOT NULL,
            alt text NOT NULL,
            phenotype text
        );"""
        output1 = con.parse_statement(sql_create_db_table_allel, ())
        output2 = con.parse_statement(sql_create_db_table_populations, ())
        output3 = con.parse_statement(sql_create_db_table_phenotype, ())
        if isinstance(output1, sqlite3.Error):  # pragma: nocover
            raise Exception(output1.args[0])
        elif isinstance(output2, sqlite3.Error):  # pragma: nocover
            raise Exception(output2.args[0])
        elif isinstance(output3, sqlite3.Error):  # pragma: nocover
            raise Exception(output3.args[0])
        else:
            sql_idx_allel = "CREATE INDEX allel_idx ON allel(chr,pos,ref,alt);"
            sql_idx_population = "CREATE INDEX pop_idx ON populations(chr,pos,ref,alt);"
            sql_idx_phenotype = "CREATE INDEX phe_idx ON phenotype(chr,pos,ref,alt);"
            output1 = con.parse_statement(sql_idx_allel, ())
            output2 = con.parse_statement(sql_idx_population, ())
            output3 = con.parse_statement(sql_idx_phenotype, ())
            if isinstance(output1, sqlite3.Error):  # pragma: nocover
                raise Exception(output1.args[0])
            elif isinstance(output2, sqlite3.Error):  # pragma: nocover
                raise Exception(output2.args[0])
            elif isinstance(output3, sqlite3.Error):  # pragma: nocover
                raise Exception(output3.args[0])
            else:
                return True


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
        sql_print_allel = "SELECT id, chr, pos, ref, alt , wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt FROM allel GROUP BY id, chr, pos, ref, alt, wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt;"
        output_allel = con.parse_statement(sql_print_allel, ())
        sql_print_population = "SELECT id, chr, pos, ref, alt , wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt, population FROM populations GROUP BY id, chr, pos, ref, alt, wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt, population;"
        output_population = con.parse_statement(sql_print_population, ())
        sql_print_phenotype = "SELECT id, chr, pos, ref, alt , phenotype FROM phenotype GROUP BY id, chr, pos, ref, alt, phenotype;"
        output_phenotype = con.parse_statement(sql_print_phenotype, ())
        if isinstance(output_allel, list) is False:  # pragma: nocover
            print(output_allel)
            return False
        elif isinstance(output_population, list) is False:  # pragma: nocover
            print(output_population)
            return False
        elif isinstance(output_phenotype, list) is False:  # pragma: nocover
            print(output_phenotype)
            return False
        else:
            print("TABLE allel: \n")
            for out in output_allel:
                print(out)
            print("\nTABLE populations: \n")
            for out in output_population:
                print(out)
            print("\nTABLE phenotype: \n")
            for out in output_phenotype:
                print(out)

    def count_variants(self, con):
        """
        Counts the existing number of (all) Variants.

        :param con: connection to the database
        :rtype: int
        """
        sql_count_var = "SELECT COUNT(*) FROM allel"
        output = con.parse_statement(sql_count_var, ())
        if type(output) != list:  # pragma: nocover
            print(output)
            return False
        else:
            return output[0][0]

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

## module beacon.database
"""
..."communicates" with database
"""
import sqlite3
from . import common


class ConnectDatabase:
    """
    includes functions for creating the ConnectDatabase Object and connects to database.

    """

    def __init__(self, database):
        """
        Creates ConnectDatabase Object and connects to database.

        :param database: path to database
        """
        self.connection = sqlite3.connect(database)

    def parse_statement(self, sql_str, parameters, annV_bool=False):
        """
        Creates cursor object and requests database and gives “answer” back.

        :param sql_str: sql command
        :param parameters: input parameters
        :param annV_bool: bool if variant request
        :return: cursor_ouput or Error
        """
        try:
            c = self.connection.cursor()
            c.execute(sql_str, parameters)
            self.connection.commit()
            output = c.fetchall()
            if annV_bool:
                if len(output) != 0:
                    return True
                else:
                    return False
            else:
                return output
        except sqlite3.Error as e:
            return e

    def handle_request(self, variant, authorization=False):
        """
        Gets an variant object and parses request to database and gets an AnnVar or Info as an output.

        :param variant: Variant Object
        :return: AnnVar or Info Object
        """
        sql_str = "SELECT id FROM variants WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
        parameters = (variant.chr, variant.pos, variant.ref, variant.alt)
        occ = self.parse_statement(sql_str, parameters, True)
        annVar = common.AnnVar(variant.chr, variant.pos, variant.ref, variant.alt, occ)
        if authorization is False:
            return annVar
        else:
            sql_varCount = "SELECT COUNT(*) FROM allel WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
            varCount = self.parse_statement(sql_varCount, parameters)
            sql_population = "SELECT population FROM populations WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
            population = self.parse_statement(sql_population, parameters)
            sql_countAll = "SELECT SUM(allel_homo)+SUM(allel_hetero) FROM allel WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
            countAll = self.parse_statement(sql_countAll, parameters)
            print("count_All: ", countAll)
            sql_countAlt = "SELECT SUM(alt_count) FROM allel WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
            countAlt = self.parse_statement(sql_countAlt, parameters)
            print("count_Alt: ", countAlt)
            frequency = countAll #/ countAlt
            sql_phenotype = "SELECT phenotype FROM populations WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
            phenotype = self.parse_statement(sql_phenotype, parameters)
            return common.Info(annVar.chr, annVar.pos, annVar.ref, annVar.alt, annVar.occ, varCount, population, None, frequency, phenotype)

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
            c.close()
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
        # checks if variant exists in database and creates annVar object
        sql_str = (
            "SELECT id FROM allel WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
        )
        parameters = (variant.chr, variant.pos, variant.ref, variant.alt)
        occ = self.parse_statement(sql_str, parameters, True)
        annVar = common.AnnVar(variant.chr, variant.pos, variant.ref, variant.alt, occ)
        # if authorization is False or no occ (no extra information availible) return Annvar
        if authorization is False or annVar.occ is False:
            return annVar
        # else create Info object
        else:
            # count allel in database for variant and sum it n VarCount
            sql_alt_hetero = "SELECT SUM(alt_hetero) FROM allel WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
            sql_alt_homo = "SELECT SUM(alt_homo) FROM allel WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
            sql_hemi_alt = "SELECT SUM(hemi_alt) FROM allel WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
            alt_hetero = self.parse_statement(sql_alt_hetero, parameters)[0][0]
            alt_homo = self.parse_statement(sql_alt_homo, parameters)[0][0]
            hemi_alt = self.parse_statement(sql_hemi_alt, parameters)[0][0]
            varCount = alt_hetero + 2 * alt_homo + hemi_alt
            # select populations of variant
            sql_population = "SELECT population FROM populations WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
            population = list(
                dict.fromkeys(self.parse_statement(sql_population, parameters))
            )
            # create dic for population output
            pop_dic = {}
            # for each population count allel = popCount and add to output population dic
            for p in population:
                sql_alt_hetero = "SELECT SUM(alt_hetero) FROM populations WHERE chr = ? AND pos = ? AND ref = ? AND alt = ? AND population = ?;"
                sql_alt_homo = "SELECT SUM(alt_homo) FROM populations WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ? AND population = ?;"
                sql_hemi_alt = "SELECT SUM(hemi_alt) FROM populations WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ? AND population = ?;"
                alt_hetero = self.parse_statement(
                    sql_alt_hetero,
                    (annVar.chr, annVar.pos, annVar.ref, annVar.alt, p[0]),
                )[0][0]
                alt_homo = self.parse_statement(
                    sql_alt_homo, (annVar.chr, annVar.pos, annVar.ref, annVar.alt, p[0])
                )[0][0]
                hemi_alt = self.parse_statement(
                    sql_hemi_alt, (annVar.chr, annVar.pos, annVar.ref, annVar.alt, p[0])
                )[0][0]
                popCount = alt_hetero + 2 * alt_homo + hemi_alt
                pop_dic[p[0]] = popCount
            # select count of general allel information
            sql_wildtype = "SELECT SUM(wildtype) FROM allel WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
            sql_hemi_ref = "SELECT SUM(hemi_ref) FROM allel WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
            wildtype = self.parse_statement(sql_wildtype, parameters)[0][0]
            hemi_ref = self.parse_statement(sql_hemi_ref, parameters)[0][0]
            # calculate frequency out of it (#variant_allel/#locus_information_allel)
            frequency = varCount / (
                2 * (wildtype + alt_hetero + alt_homo) + hemi_alt + hemi_ref
            )
            # get list of phenotypes associated with variant
            sql_phenotype = "SELECT phenotype FROM phenotype WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
            phenotype = map(
                lambda x: x[0], self.parse_statement(sql_phenotype, parameters)
            )
            # returns Info object
            return common.Info(
                annVar.chr,
                annVar.pos,
                annVar.ref,
                annVar.alt,
                annVar.occ,
                varCount,
                pop_dic,
                None,
                frequency,
                list(phenotype),
            )

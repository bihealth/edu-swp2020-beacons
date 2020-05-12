## module beacon.database
"""
..."communicates" with database
"""
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
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

    def close(self):
        """
        Closes connection to database of ConnectDatabase Object.

        :return: True if succeeded else False
        """
        try:
            self.connection.close()
            return True
        except sqlite3.Error:
            return False

    def parse_statement(self, sql_str, parameters, annV_bool=False):
        """
        Creates cursor object and requests database and gives “answer” back.

        :param sql_str: sql command
        :param parameters: input parameters
        :param annV_bool: bool if variant request
        :return: cursor_ouput or Error
        """
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

    def handle_request(self, variant, authorization=1):
        """
        Gets an variant object and parses request to database and gets an AnnVar or Info as an output.

        :param variant: Variant Object
        :return: AnnVar or Info Object
        """
        try:
            # checks if variant exists in database and creates annVar object
            sql_str = "SELECT id FROM allel WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
            parameters = (variant.chr, variant.pos, variant.ref, variant.alt)
            occ = self.parse_statement(sql_str, parameters, True)
            annVar = common.AnnVar(
                variant.chr, variant.pos, variant.ref, variant.alt, occ
            )
            # if authorization is False or no occ (no extra information availible) return Annvar
            if authorization == 1 or annVar.occ is False:
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
                # select count of general allel information
                sql_wildtype = "SELECT SUM(wildtype) FROM allel WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
                sql_hemi_ref = "SELECT SUM(hemi_ref) FROM allel WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
                wildtype = self.parse_statement(sql_wildtype, parameters)[0][0]
                hemi_ref = self.parse_statement(sql_hemi_ref, parameters)[0][0]
                # calculate frequency out of it (#variant_allel/#locus_information_allel)
                frequency = varCount / (
                    2 * (wildtype + alt_hetero + alt_homo) + hemi_alt + hemi_ref
                )
                # returns information about varCount and frequency
                if authorization == 2:
                    return common.Info(
                        annVar.chr,
                        annVar.pos,
                        annVar.ref,
                        annVar.alt,
                        annVar.occ,
                        annVar.error,
                        varCount,
                        None,
                        None,
                        frequency,
                        None,
                    )
                # select populations of variant and converts them into string list
                sql_population = "SELECT population FROM populations WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
                population = list(
                    map(
                        lambda x: x[0],
                        dict.fromkeys(self.parse_statement(sql_population, parameters)),
                    )
                )
                # create dic for population output
                pop_dic = {}
                sta_data = []
                # for each population count allel = popCount and add to output population dic
                for p in population:
                    sql_pop_alt_hetero = "SELECT SUM(alt_hetero) FROM populations WHERE chr = ? AND pos = ? AND ref = ? AND alt = ? AND population = ?;"
                    sql_pop_alt_homo = "SELECT SUM(alt_homo) FROM populations WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ? AND population = ?;"
                    sql_pop_hemi_alt = "SELECT SUM(hemi_alt) FROM populations WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ? AND population = ?;"
                    pop_alt_hetero = self.parse_statement(
                        sql_pop_alt_hetero,
                        (annVar.chr, annVar.pos, annVar.ref, annVar.alt, p),
                    )[0][0]
                    pop_alt_homo = self.parse_statement(
                        sql_pop_alt_homo,
                        (annVar.chr, annVar.pos, annVar.ref, annVar.alt, p),
                    )[0][0]
                    pop_hemi_alt = self.parse_statement(
                        sql_pop_hemi_alt,
                        (annVar.chr, annVar.pos, annVar.ref, annVar.alt, p),
                    )[0][0]
                    popCount = pop_alt_hetero + 2 * pop_alt_homo + pop_hemi_alt
                    pop_dic[p] = popCount
                    sql_pop_wildtype = "SELECT SUM(wildtype) FROM populations WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ? AND population = ?;"
                    sql_pop_hemi_ref = "SELECT SUM(hemi_ref) FROM populations WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ? AND population = ?;"
                    pop_wildtype = self.parse_statement(
                        sql_pop_wildtype,
                        (annVar.chr, annVar.pos, annVar.ref, annVar.alt, p),
                    )[0][0]
                    pop_hemi_ref = self.parse_statement(
                        sql_pop_hemi_ref,
                        (annVar.chr, annVar.pos, annVar.ref, annVar.alt, p),
                    )[0][0]
                    sta_data.append(
                        [
                            pop_wildtype,
                            pop_alt_hetero,
                            pop_alt_homo,
                            pop_hemi_alt,
                            pop_hemi_ref,
                        ]
                    )
                # create statistics
                statistic = self._create_statistics(population, sta_data)
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
                    annVar.error,
                    varCount,
                    pop_dic,
                    statistic,
                    frequency,
                    list(phenotype),
                )
        except sqlite3.Error as e:
            return common.AnnVar(
                variant.chr, variant.pos, variant.ref, variant.alt, None, e
            )

    def _create_statistics(self, populations, data):
        """
        Creates a barplot showing the genotypes per population.

        :param populations: a list of the population names
        :param data: a list of list where per population the count per wildtype, alt_hetero, alt_homo, alt_hemi and alt_ref
        :return: matplolib plot object
        """
        # calculates proportions and turns rows into columns
        data = list(map(lambda d: [(s / sum(d)) * 100 for s in d], data))
        tdata = list(zip(*data))
        # legend and colors
        legend = [
            "wildtype",
            "alt_heterozygote",
            "alt_homozygote",
            "alt_hemizygote",
            "ref_hemizygote",
        ]
        colors = plt.cm.autumn(np.linspace(0.2, 1.1, len(legend)))
        width = 0.35  # the width of the bars
        fig, ax = plt.subplots()
        # creates barplot
        y_offset = np.zeros(len(populations))
        for l in range(5):
            ax.bar(
                populations,
                tdata[l],
                width,
                bottom=y_offset,
                label=legend[l],
                color=colors[l],
            )
            y_offset = y_offset + tdata[l]
        # adds legend, label and title
        ax.legend()
        ax.set_ylabel("Proportion in percent")
        ax.set_title("Genotypes per population")
        return ax

## module beacon.database
"""
..."communicates" with database
"""
import sqlite3


class ConnectDatabase:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)

    def parse_statement(self, sql_str, parameters, annV_bool=False):
        """
        Creates cursor object and requests database and gives “answer” back.

        :param args: sql command, input parameters, bool if variant request
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

    def handle_variant(self, variant):
        """
        Gets an variant object and parses request to database and gets an bool or Error as an output.

        :param args: Variant Object
        :return: bool or Error Object
        """
        sql_str = "SELECT id FROM variants WHERE chr = ? AND pos = ? AND ref = ?  AND alt = ?;"
        parameters = (variant.chr, variant.pos, variant.ref, variant.alt)
        occ = self.parse_statement(sql_str, parameters, True)
        return occ

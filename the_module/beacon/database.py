## module beacon.database

import sqlite3
from . import common as cm

class ConnectDatabase:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)


    def parse_statement(self, sql_str, annV_bool = False):
        """ Input: sql_string
        Output: cursor_ouput, AnnotatedVariant
        function creates cursor object and requests database, gives “answer” back """
        try:
            c = self.connection.cursor()
            print(sql_str)
            c.execute(sql_str[0], sql_str[1])
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
            return False

    def handle_variant(self,variant):
        """Input: Variant Object
      	   Output: AnnotatedVariant(bool)
     	   Gets an variant object from flask handle and parses request to database and gets an  Annotated as an output """
        try:
            sql_str = "SELECT id FROM variants WHERE chr = (?) AND pos = (?)AND res = (?)AND alt = (?);", (variant.chr,variant.pos, variant.res, variant.alt)
            occ = self.parse_statement(sql_str, True)
            return occ
        except sqlite3.Error as e:
            return e

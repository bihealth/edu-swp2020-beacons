## module beacon.database

import sqlite3
import common


class Database:

    def __init__(self, path_str):
        self.database = path_str

class OperateDatabase:

    def handle_variant(variant, database):
        """Input: Variant Object
      	   Output: AnnotatedVariant(bool)
     	   Gets an variant object from flask handle and parses request to database and gets an  Annotated as an output """
        try:
            connectDb = ConnectDatabase.connect(database)
            sql_str = "select id from variants where chr = '" + cm.Variant.chr + "', pos = '" + str(cm.Variant.pos) +"' , res = '" + cm.Variant.res + "' , alt = '" + cm.Variant.alt
            occ = ConnectDatabase.parse_statement(sql_str, connectDb, True)
            #ann_v = cm.AnnotatedVariant(variant.chr, variant.pos, variant.res, variant.alt, occ)
            ConnectDatabase.disconnect(connectDb)
            #return ann_v
            return occ
        except sqlite3.Error as e:
            return e



class ConnectDatabase:

    def __init__(self,con):
        self.connection = con

    def connect(database):
        """Input: path_to_db
        Output: con
        function provides connection to given database """
        try:
            connectDb = ConnectDatabase(sqlite3.connect(database))
            return connectDb.connection
        except sqlite3.Error as e:
            return e



    def parse_statement(sql_str, con, annV_bool = False):
        """ Input: sql_string
        Output: cursor_ouput, AnnotatedVariant
        function creates cursor object and requests database, gives “answer” back """
        try:
            c = con.cursor()
            c.execute(sql_str)
            output = c.fetchall()
            con.commit()
            if annV_bool:
                if len(output) != 0:
                    return True
            else:
                return output
        except sqlite3.Error as e:
            return e


    def disconnect(con):
        """closes connection and commits and connection con.comm and con.close """
        try:
            con.close()
        except sqlite3.Error as e:
            return e

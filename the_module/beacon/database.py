## module beacon.database

import sqlite3
import beacon.common as cm


class Database:

    def __init__(self, path_str):
        self.database = path_str

class OperateDatabase:

    def handle_variant(cm.Variant):
        """Input: Variant Object
      	   Output: AnnotatedVariant(bool)
     	   Gets an variant object from flask handle and parses request to database and gets an  Annotated as an output """
        pass

class ConnectDatabase:

    def __init__(self,con):
        self.connection = con

    def connect(database):
        """Input: path_to_db
        Output: con
        function provides connection to given database """
        pass


    def parse_statement(sql_str):
        """ Input: sql_string
        Output: cursor_ouput, AnnotatedVariant
        function creates cursor object and requests database, gives “answer” back """
        pass


    def disconnect(connection):
        """closes connection and commits and connection con.comm and con.close """
        pass

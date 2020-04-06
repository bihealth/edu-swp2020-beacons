import sqlite3
from sqlite3 import Error
#import beacon.common
import database
import pyvcf
import os

#db_connection = DatabaseConnection(path=os.environ.get("/database.db"))
#wann wollen wir datenbank path festlegen? bei jeder neuen datenbank automatisch oder separiert durch den admint?
#error handling


def parse_vcf(infile, con):
    vcfdata= open(infile,"r")
    vcf_reader = vcf.Reader(vcfdata)
    try: 
        for variable  in vcf_reader:
            """give to datenbank (sql_str)"""
            chr = record.CHROM
            pos = record.POS
            ref = record.REF
            alt = record.ALT
            con.parse_statement("INSERT INTO variants (id,chr,pos,ref,alt) VALUES (?,?,?,?,?)",(id,chr,pos,ref,alt)) 
            con.connection.close()
    except sqlite3.Error as e:
        print(e)
    infile.close()
    return True

class CreateDbCommand:
    def __init__(self):
        self.data = []
 
    def create_tables(self, con):
        """ Input: Variant
        Output: bool
        creates variant table in database """
        try:
            sql_create_db_table = """ CREATE TABLE IF NOT EXISTS  (
                                        id integer PRIMARY KEY,
                                        chr text NOT NULL,
                                        pos integer NOT NULL,
                                        ref text NOT NULL,
                                        alt text NOT NULL
                                    ); """                         
            output = con.parse_statement(sql_create_db_table)
        except sqlite3.Error as e:
            print(e)
        return True
        

class SearchDuplicatesCommand:
    def __init__(self):
        self.data = []

    def find_dup(self, con):
        """ Input: database
        Output: bool
        looks for duplicates"""
        try:
            sql_find_dup = "SELECT id, chr, pos, COUNT(*) FROM variants GROUP BY chr, pos, ref, alt HAVING COUNT(*) > 1"                         
            output = con.parse_statement(sql_find_dup)
            for out in output:
                print(out + "\n")
        except sqlite3.Error as e:
            print(e)
        return True
 
class OperateDatabase:
    def __init__(self):
        self.data = []
        
    def print_db(self, con):
        """prints whole Database"""
        try:
            sql_print = "SELECT id, chr, pos, ref, alt FROM variants GROUP BY id, chr, pos, ref, alt"                         
            output = con.parse_statement(sql_print)
            for out in output:
                print(out + "\n")
        except sqlite3.Error as e:
            print(e)
        return True
 
    def count_variants(self, con):
        """ counts the existing number of (all) Variants """
        try:
            sql_count_var = "SELECT COUNT(*) FROM variants"                         
            output = con.parse_statement(sql_count_var)
            for out in output:
                print(out + "\n")
        except sqlite3.Error as e:
            print(e)
        return True
	
    def updating_data(self, con, variants):
        """Input:variants
        Output:bool
        function access the database using connect() and updates."""
        try:
            sql = ''' UPDATE variants
                    SET chr = ? ,
                        pos = ? ,
                        ref = ? ,
                        alt = ? 
                    WHERE id = ? '''  
            forparse = (sql, variants)                      
            output = con.parse_statement(sql)
        except sqlite3.Error as e:
            print(e)
        return True


    def delete_data(self, con, id):
        """ Input: Variant, Database
        Output: bool
        function deletes given Variant in db and gives bool if succeeded back"""
        try: 
            sql = 'DELETE FROM variants WHERE id=?'
            forparse = (sql, (id,))
            output = con.parse_statement(forparse)
            return True
        except sqlite3.Error as e:
            print(e)
        return True
 
#nct: def export_db() + def print_row() + def count
print("hier angekommen")
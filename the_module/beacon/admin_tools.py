import sqlite3
from sqlite3 import Error
#import beacon.common
import database
import vcf
import os

#db_connection = DatabaseConnection(path=os.environ.get("/database.db"))
#wann wollen wir datenbank path festlegen? bei jeder neuen datenbank automatisch oder separiert durch den admint?
#error handling

def parse_vcf(infile, con):
    vcf_reader = vcf.Reader(infile)
    try: 
        for variant in vcf_reader:
            """give to datenbank (sql_str)"""
            chr = variant.CHROM
            pos = str(variant.POS)
            res = variant.REF
            alt = "".join(str(i or '') for i in variant.ALT)
            #print(alt)
            sql_str = "INSERT INTO variants (chr,pos,ref,alt) VALUES ("+chr+","+pos+",'"+res+"','"+alt+"');"
            #print(sql_str)
            con.parse_statement(sql_str)
        return True
    except sqlite3.Error as e:
        return e
    infile.close()   

class CreateDbCommand:
    def __init__(self):
        self.data = [] 
 
    def create_tables(self, con):
        """ Input: Variant
       Output: bool
       creates variant table in database """
        try:
            sql_create_db_table = """ CREATE TABLE IF NOT EXISTS variants (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        chr text NOT NULL,
                                        pos integer NOT NULL,
                                        ref text NOT NULL,
                                        alt text NOT NULL
                                    ); """        
            output = con.parse_statement(sql_create_db_table) 
            return True
        except sqlite3.Error as e:
            return e
        
class SearchDuplicatesCommand:
    def __init__(self):
        self.data = []

    def find_dup(self, con):
        """ Input: database
        Output: list of duplicates
        looks for duplicates"""
        try:
            #sql_find_dup = "SELECT DISTINCT chr, pos, ref, alt FROM variants ORDER BY chr;"  
            sql_find_dup = "SELECT id, chr, pos, COUNT(*) FROM variants GROUP BY chr, pos, ref, alt HAVING COUNT(*) > 1;"
            output = con.parse_statement(sql_find_dup)
            for out in output:
                print(out)
            return ""
        except sqlite3.Error as e:
            return e

class OperateDatabase:
    def __init__(self):
        self.data = []
       
    def print_db(self, con):
        """prints whole Database"""
        try:
            sql_print = "SELECT id, chr, pos, ref, alt FROM variants GROUP BY id, chr, pos, ref, alt"                         
            output = con.parse_statement(sql_print)
            for out in output:
                print(out)
            return ""
        except sqlite3.Error as e:
            return e
 
    def count_variants(self, con):
        """ counts the existing number of (all) Variants """
        try:
            sql_count_var = "SELECT COUNT(*) FROM variants"                         
            output = con.parse_statement(sql_count_var)
            return (int(output[0][0]))
        except sqlite3.Error as e:
            return e

    def updating_data(self, con, variants):
        """Input:variants
        Output:bool
        function access the database using connect() and updates."""
        try:
            chr = variants[0]
            pos = str(variants[1])
            res = variants[2]
            alt = "".join(str(i or '') for i in variants[3]) 
            id = variants[4]  
            sql_str = "UPDATE variants SET chr = "+chr+", pos = "+pos+" , ref = '"+res+"' , alt = '"+alt+"' WHERE id = "+id+""                         
            output = con.parse_statement(sql_str)
            #print_db(con)
            return "rufe -p auf, um die Änderung zu sehen"
        except sqlite3.Error as e:
            return e

    def delete_data(self, con, id):
        """ Input: Variant, Database
        Output: bool
        function deletes given Variant in db and gives bool if succeeded back"""
        try: 
            id = id[0]
            sql_str = "DELETE FROM variants WHERE id= "+id+""
            output = con.parse_statement(sql_str)
            return "rufe -p auf, um die Änderung zu sehen"
        except sqlite3.Error as e:
            return e
 
#nct: def export_db() + def print_row() + def count
# für version 2:
# - Kommas einlesen, bei alt in der funktion parse_vcf 
# - bei der funktion find_dup -> automatisch löschen 
# - 5 x updadte variablen benennen bei -h update -u U U U U U
# - in der funktion update und delete noch das ergebnis printen
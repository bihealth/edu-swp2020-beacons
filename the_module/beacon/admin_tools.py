import sqlite3
from sqlite3 import Error
#import beacon.common
#import beacon.database
#import pyvcf
#import sys #?


class ImportVcfCommand:
    def __init__(self):
        self.data = []
    
    def parse_vcf_variant(self, vcf_file):
        """Input: vcf_file
        Output: list of Variant Objects
        function reads vcf_file and converts them to variant objects"""
        pass
 
class CreateDbCommand:
    def __init__(self):
        self.data = []
 
    def create_tables(self,Variant,Database):
        """ Input: Variant
        Output: bool
        creates variant table in database """
        pass
    
    def insert_data(self,Variant,Database):
        """ Input: Variant
        Output: bool
        inserts rows into a table in the database"""
        pass
 
class SearchDuplicatesCommand:
    def __init__(self):
        self.data = []

    def find_dup(self, Database):
        """ Input: database
        Output: bool
        looks for duplicates"""
        pass
 
class OperateDatabase:
    def __init__(self):
        self.data = []
        
    def print_db(self, Database):
        """prints whole Database or specific rows"""
        pass
 
    def count_variants(self):
        """ counts the existing number of (all) Variants """
        pass
	
    def updating_data(self, Variants):
        """Input:variants
        Output:bool
        function access the database using connect() and updates."""
        pass

    def delete_data(self, Variant, Database):
        """ Input: Variant, Database
        Output: bool
        function deletes given Variant in db and gives bool if succeeded back"""
        pass
 
#nct: def export_db()
print("hier angekommen")
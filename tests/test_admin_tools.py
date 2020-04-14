from the_module.beacon import admin_tools
from the_module.beacon import database
import pytest
import sqlite3


def test_parse_vcf(demo_vcf_file,demo_db_path):#,empty_vcf_file
    con = database.ConnectDatabase(demo_db_path)
    inflie = open(demo_vcf_file,'r')
    out = admin_tools.parse_vcf(inflie, con)
    assert out is not None
    assert out is True

def test_create_tables(demo_db_path):
    con = database.ConnectDatabase(demo_db_path)
    data = admin_tools.CreateDbCommand()
    out = data.create_tables(con)
    assert out is not None
    assert out is True
    
def test_find_dup(demo_db_path):
    con = database.ConnectDatabase(demo_db_path)
    sd = admin_tools.SearchDuplicatesCommand()
    out = sd.find_dup(con)
    assert out is not None
    assert out is ""

def test_print_db(demo_db_path):
    con = database.ConnectDatabase(demo_db_path)
    od = admin_tools.OperateDatabase()
    out = od.print_db(con)
    assert out is not None
    assert out is ""

def test_count_variants(demo_db_path):
    con = database.ConnectDatabase(demo_db_path)
    od = admin_tools.OperateDatabase()
    out = od.count_variants(con)
    assert out is not None
    assert out == 3

def test_updating_data(demo_db_path):
    con = database.ConnectDatabase(demo_db_path)
    od = admin_tools.OperateDatabase()
    variants = (1, 1, 'A', 'T', 3)
    out = od.updating_data(con, variants)
    assert out is not None
    assert out is True

def test_delete_data(demo_db_path):
    con = database.ConnectDatabase(demo_db_path)
    od = admin_tools.OperateDatabase()
    id = (2,)
    out = od.delete_data(con, id)
    assert out is not None
    assert out is True 
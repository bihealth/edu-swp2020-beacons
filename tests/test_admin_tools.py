from the_module.beacon import admin_tools
from the_module.beacon import database
import pytest
import sqlite3


def test_parse_vcf(demo_vcf_file,demo_db_path):
    con = database.ConnectDatabase(demo_db_path)
    out = admin_tools.parse_vcf(demo_vcf_file, con)
    assert out is True


def test_create_tables(demo_db_path):
    data = admin_tools.CreateDbCommand
    con = database.ConnectDatabase(demo_db_path)
    assert data.create_tables(con) is True


def test_print_db(demo_db_path):
    od = admin_tools.OperateDatabase
    assert od.print_db(demo_db_path) is ""

def test_count_variants(demo_db_path):
    od = admin_tools.OperateDatabase
    con = database.ConnectDatabase(demo_db_path)
    out = od.count_variants(con)
    assert out == 4

def test_updating_data(demo_db_path):
    od = admin_tools.OperateDatabase
    con = database.ConnectDatabase(demo_db_path)
    out = od.updating_data(con, (1, 1, 'A', 'T', 3))
    assert out is "rufe -p auf, um die Änderung zu sehen"

def test_delete_data(demo_db_path):
    od = admin_tools.OperateDatabase
    #id = (2,)
    con = database.ConnectDatabase(demo_db_path)
    out = od.delete_data(con, (2,))
    assert out is "rufe -p auf, um die Änderung zu sehen"
    



#pytest -s 
    
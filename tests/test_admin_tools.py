from beacon import admin_tools
from beacon import database
import pytest  # noqa


def test_parse_vcf(demo_vcf_file, demo_db_path):
    con = database.ConnectDatabase(demo_db_path)
    inflie = open(demo_vcf_file, "r")
    out = admin_tools.parse_vcf(inflie, con)
    assert out is not None
    assert out is True


def test_create_tables(tmpdir):
    path_db = str(tmpdir.join("test.sqlite3"))
    con = database.ConnectDatabase(path_db)
    data = admin_tools.CreateDbCommand()
    out = data.create_tables(con)
    out_allel = con.parse_statement("SELECT * FROM allel",())
    out_populations = con.parse_statement("SELECT * FROM populations",())
    out_phenotype = con.parse_statement("SELECT * FROM phenotype",())
    assert out is True
    assert out_allel == []
    assert out_populations == []
    assert out_phenotype == []


def test_print_db(demo_db_path, capsys):
    conn = database.ConnectDatabase(demo_db_path)
    od = admin_tools.OperateDatabase()
    od.print_db(conn)
    out = capsys.readouterr()
    assert "TABLE allel:" in out[0]
    assert "(1, '1', 1000000, 'C', 'G', 3, 0, 5, 0, 0)" in out[0]
    assert "TABLE populations:" in out[0]
    assert "(1, '1', 1000000, 'C', 'G', 3, 0, 5, 0, 0, 'GBR')" in out[0]
    assert "TABLE phenotype:" in out[0]
    assert "(2, '1', 1000001, 'G', 'A', 'muskulär')" in out[0]


def test_count_variants(demo_db_path):
    con = database.ConnectDatabase(demo_db_path)
    od = admin_tools.OperateDatabase()
    out = od.count_variants(con)
    assert out is not None
    assert out == 3


def test_updating_data(demo_db_path):
    con = database.ConnectDatabase(demo_db_path)
    od = admin_tools.OperateDatabase()
    variants = (1, 1, "A", "T", 3)
    out = od.updating_data(con, variants)
    assert out is not None
    assert out is True


def test_delete_data(demo_db_path):
    con = database.ConnectDatabase(demo_db_path)
    od = admin_tools.OperateDatabase()
    id = 1
    out = od.delete_data(con, id)
    assert out is not None
    assert out is True
    errorid = 10000
    eo = od.delete_data(con, errorid)
    print(eo)
    assert eo is False

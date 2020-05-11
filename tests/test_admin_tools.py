from beacon import admin_tools
from beacon import database
import pytest  # noqa


#def test_parse_vcf(demo_vcf_file, demo_db_path):
#    con = database.ConnectDatabase(demo_db_path)
#    inflie = open(demo_vcf_file, "r")
#    out = admin_tools.parse_vcf(inflie, con)
#    assert out is not None
#    assert out is True


def test_create_tables(tmpdir):
    path_db = str(tmpdir.join("test.sqlite3"))
    con = database.ConnectDatabase(path_db)
    data = admin_tools.CreateDbCommand()
    out = data.create_tables(con)
    out_allel = con.parse_statement("SELECT * FROM allel", ())
    out_populations = con.parse_statement("SELECT * FROM populations", ())
    out_phenotype = con.parse_statement("SELECT * FROM phenotype", ())
    assert out is True
    assert out_allel == []
    assert out_populations == []
    assert out_phenotype == []


def test_create_tables_error(tmpdir):
    path_db = str(tmpdir.join("test.sqlite3"))
    con = database.ConnectDatabase(path_db)
    sql_create_db_table_allel = """
            CREATE TABLE IF NOT EXISTS allel (
            id integer PRIMARY KEY AUTOINCREMENT,
            chr text NOT NULL,
            pos integer NOT NULL,
            ref text NOT NULL,
            alt text NOT NULL,
            wildtype integer NOT NULL,
            alt_hetero integer NOT NULL,
            alt_homo integer NOT NULL,
            hemi_ref integer NOT NULL,
            hemi_alt integer NOT NULL
        );"""
    sql_idx_allel = "CREATE INDEX allel_idx ON allel(chr,pos,ref,alt);"
    con.parse_statement(sql_create_db_table_allel, ())
    con.parse_statement(sql_idx_allel, ())
    data = admin_tools.CreateDbCommand()
    out = data.create_tables(con)
    assert "An error has occured:" in out


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


def test_print_db_error(tmpdir):
    path_db = str(tmpdir.join("test.sqlite3"))
    conn = database.ConnectDatabase(path_db)
    od = admin_tools.OperateDatabase()
    out = od.print_db(conn)
    assert "An error has occured:" in out


def test_count_variants(demo_db_path):
    con = database.ConnectDatabase(demo_db_path)
    od = admin_tools.OperateDatabase()
    out = od.count_variants(con)
    assert out is not None
    assert out == 3


def test_count_variants_error(tmpdir):
    path_db = str(tmpdir.join("test.sqlite3"))
    con = database.ConnectDatabase(path_db)
    od = admin_tools.OperateDatabase()
    out = od.count_variants(con)
    assert "An error has occured:" in out


def test_updating_allel(demo_db_path, capsys):
    con = database.ConnectDatabase(demo_db_path)
    od = admin_tools.OperateDatabase()
    allel = (1, 1, "A", "T", 4, 3, 4, 0, 0, 3)
    out = od.updating_allel(con, allel)
    assert "The table allel has been updated. Call -p to see the changes." in out


def test_updating_allel_error(tmpdir):
    allel = (1, 1, "A", "T", 4, 3, 4, 0, 0, 3)
    path_db = str(tmpdir.join("test.sqlite3"))
    con = database.ConnectDatabase(path_db)
    od = admin_tools.OperateDatabase()
    out = od.updating_allel(con, allel)
    assert "An error has occured:" in out


def test_updating_populations(demo_db_path, capsys):
    con = database.ConnectDatabase(demo_db_path)
    od = admin_tools.OperateDatabase()
    populations = (1, 1, "A", "T", 4, 3, 4, 0, 0, 3, "GER", 1)
    out = od.updating_populations(con, populations)
    assert (
        "The table populations has been updated. Call -p to see the changes." in out
    )


def test_updating_populations_error(tmpdir):
    populations = (1, 1, "A", "T", 4, 3, 4, 0, 0, 3, "GER", 1)
    path_db = str(tmpdir.join("test.sqlite3"))
    con = database.ConnectDatabase(path_db)
    od = admin_tools.OperateDatabase()
    out = od.updating_populations(con, populations)
    assert "An error has occured:" in out


def test_updating_phenotype(demo_db_path):
    con = database.ConnectDatabase(demo_db_path)
    od = admin_tools.OperateDatabase()
    phenotype = (1, 1, "A", "T", "synaptical", 1)
    out = od.updating_phenotype(con, phenotype)
    assert "The table phenotype has been updated. Call -p to see the changes." in out


def test_updating_phenotype_error(tmpdir):
    phenotype = (1, 1, "A", "T", "synaptical", 1)
    path_db = str(tmpdir.join("test.sqlite3"))
    con = database.ConnectDatabase(path_db)
    od = admin_tools.OperateDatabase()
    out = od.updating_phenotype(con, phenotype)
    assert "An error has occured:" in out


def test_create_tables_user(tmpdir):
    path_db = str(tmpdir.join("test.sqlite3"))
    con = database.ConnectDatabase(path_db)
    user_data = admin_tools.UserDB()
    out = user_data.create_tables_user(con)
    out_ip = con.parse_statement("SELECT * FROM ip", ())
    out_login = con.parse_statement("SELECT * FROM login", ())
    assert out is True
    assert out_ip == []
    assert out_login == []


def test_insert_user(demo_db_path):
    con = database.ConnectDatabase(demo_db_path)
    user_data = admin_tools.UserDB()
    out = user_data.create_tables_user(con)


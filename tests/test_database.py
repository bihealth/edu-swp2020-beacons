from beacon import database
from beacon import common
import pytest  # noqa


def test_connect_empty(tmpdir):
    path_db = str(tmpdir.join("test.sqlite3"))
    conn = database.ConnectDatabase(path_db)
    assert conn.connection is not None


def test_connect_demo(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    assert conn.connection is not None


def test_connect_demoXXX(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    assert conn.connection is not None


def test_parse_statement_none(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    output = conn.parse_statement("")
    assert output is not bool


def test_parse_statement_admin(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    output = conn.parse_statement("SELECT chr, pos, ref, alt FROM variants;")
    assert output is not None


def test_parse_statement_user(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    output0 = conn.parse_statement(
        "SELECT chr, pos, ref, alt FROM variants WHERE chr = '1' AND pos = 10000000 AND ref = 'C' AND pos = 'G';"
    )
    output1 = conn.parse_statement(
        "SELECT chr, pos, ref, alt FROM variants WHERE chr = 'X' AND pos = 10000000 AND ref = 'C' AND pos = 'G';"
    )
    assert output0 is not None
    assert len(output1) is 0


def test_handle_variant(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    variant0 = common.Variant("1", 1000000, "C", "G")
    variant1 = common.Variant("X", 10000000, "C", "G")
    output0 = conn.handle_variant(variant0)
    output1 = conn.handle_variant(variant1)
    assert output0 is True
    assert output1 is False


def test_handle_variant_connection_error():
    conn = database.ConnectDatabase("")
    variant = common.Variant("1", 1000000, "C", "G")
    output = conn.handle_variant(variant)
    assert output is not bool

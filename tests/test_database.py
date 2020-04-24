from beacon import database
from beacon import common
import pytest  # noqa
import sqlite3


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


def test_parse_statement_admin(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    output = conn.parse_statement("SELECT chr, pos, ref, alt FROM variants;", ())
    assert output is not None


def test_parse_statement_user(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    parameters0 = ("1", 1000000, "C", "G")
    output0 = conn.parse_statement(
        "SELECT chr, pos, ref, alt FROM variants WHERE chr = ? AND pos = ? AND ref = ? AND pos = ?;",
        parameters0,
    )
    parameters1 = ("X", 10000000, "C", "G")
    output1 = conn.parse_statement(
        "SELECT chr, pos, ref, alt FROM variants WHERE chr = ? AND pos = ? AND ref = ? AND pos = ?;",
        parameters1,
    )
    assert output0 is not None
    assert len(output1) == 0


def test_handle_request_Var(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    variant0 = common.Variant("1", 1000000, "C", "G")
    variant1 = common.Variant("X", 10000000, "C", "G")
    output0 = conn.handle_request(variant0)
    output1 = conn.handle_request(variant1)
    assert output0.occ is True
    assert output1.occ is False


def test_handle_request_connection_error():
    conn = database.ConnectDatabase("")
    variant = common.Variant("1", 1000000, "C", "G")
    output = conn.handle_request(variant)
    assert isinstance(output.occ, sqlite3.Error)

def test_handle_request_Info(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    variant0 = common.Variant("1", 1000000, "C", "G")
    variant1 = common.Variant("X", 10000000, "C", "G")
    output0 = conn.handle_request(variant0, True)
    output1 = conn.handle_request(variant1, True)
    print(output0.varCount, output0.population[0], output0.phenotype, output0.frequency)
    assert output0.occ is True
    assert output1.occ is False

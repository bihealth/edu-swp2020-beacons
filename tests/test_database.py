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


def test_with_connection(demo_db_path):
    with database.ConnectDatabase(demo_db_path) as conn:
        parameters = ("X", 10000000, "C", "G")
        output = conn.parse_statement(
            "SELECT chr, pos, ref, alt FROM allel WHERE chr = ? AND pos = ? AND ref = ? AND pos = ?;",
            parameters,
        )
    assert output is not None
    assert isinstance(conn, database.ConnectDatabase)


def test_with_connection_catch(demo_db_path, capsys):
    try:
        error = False
        with database.ConnectDatabase(demo_db_path) as conn:
            parameters = ("X", 10000000, "C", "G")
            output = conn.parse_statement(
                "SELECT chr, pos, ref, alt FROM hello WHERE chr = ? AND pos = ? AND ref = ? AND pos = ?;",
                parameters,
            )
            assert output is not None
    except Exception:
        error = True
    assert error is True


def test_close_connection(demo_db_path, capsys):
    with database.ConnectDatabase(demo_db_path) as conn:
        error = False
    try:
        parameters = ("X", 10000000, "C", "G")
        output = conn.parse_statement(
            "SELECT chr, pos, ref, alt FROM allel WHERE chr = ? AND pos = ? AND ref = ? AND pos = ?;",
            parameters,
        )
        assert output is not None
    except sqlite3.Error:
        error = True
    assert error is True


def test_parse_statement_admin(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    output = conn.parse_statement("SELECT chr, pos, ref, alt FROM allel;", ())
    assert output is not None


def test_parse_statement_user(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    parameters0 = ("1", 1000000, "C", "G")
    output0 = conn.parse_statement(
        "SELECT chr, pos, ref, alt FROM allel WHERE chr = ? AND pos = ? AND ref = ? AND pos = ?;",
        parameters0,
    )
    parameters1 = ("X", 10000000, "C", "G")
    output1 = conn.parse_statement(
        "SELECT chr, pos, ref, alt FROM allel WHERE chr = ? AND pos = ? AND ref = ? AND pos = ?;",
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
    output0 = conn.handle_request(variant)
    output1 = conn.handle_request(variant, 2)
    output2 = conn.handle_request(variant, 3)
    assert isinstance(output0.error, sqlite3.Error)
    assert isinstance(output0, common.AnnVar)
    assert isinstance(output1.error, sqlite3.Error)
    assert isinstance(output1, common.AnnVar)
    assert isinstance(output2.error, sqlite3.Error)
    assert isinstance(output2, common.AnnVar)


def test_handle_request_Info_2(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    variant0 = common.Variant("1", 1000000, "C", "G")
    variant1 = common.Variant("X", 10000000, "C", "G")
    output0 = conn.handle_request(variant0, 2)
    output1 = conn.handle_request(variant1, 2)
    assert isinstance(output0, common.Info)
    assert output0.occ is True
    assert output0.varCount == 10
    assert output0.population is None
    assert output0.phenotype is None
    assert output0.frequency == 0.625
    assert isinstance(output1, common.AnnVar)
    assert output1.occ is False


def test_handle_request_Info_3(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    variant0 = common.Variant("1", 1000000, "C", "G")
    variant1 = common.Variant("X", 10000000, "C", "G")
    output0 = conn.handle_request(variant0, 3)
    output1 = conn.handle_request(variant1, 3)
    assert isinstance(output0, common.Info)
    assert output0.occ is True
    assert output0.varCount == 10
    assert isinstance(output0.population, dict)
    assert isinstance(output0.phenotype, list)
    assert output0.frequency == 0.625
    assert isinstance(output0.statistic.plot(), list)
    assert isinstance(output1, common.AnnVar)
    assert output1.occ is False

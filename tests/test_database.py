import pytest  # noqa

from the_module.beacon import database


def test_connect_empty(tmpdir):
    path_db = tmpdir.join("test.sqlite3")
    conn = database.ConnectDatabase(path_db)
    assert conn.connection is not None


def test_connect_demo(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    assert conn.connection is not None


def test_connect_demoXXX(demo_db_path):
    conn = database.ConnectDatabase(demo_db_path)
    assert conn.connection is not None

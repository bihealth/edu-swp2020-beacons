import sqlite3

import pytest


SQL_CREATE = r"""
CREATE TABLE IF NOT EXISTS variants (
    id integer PRIMARY KEY AUTOINCREMENT,
    chr text NOT NULL,
    pos integer NOT NULL,
    ref text NOT NULL,
    alt text NOT NULL
);
"""

SQL_INSERT = r"""
INSERT INTO variants (chr, pos, ref, alt)
VALUES (?, ?, ?, ?);
"""


@pytest.fixture
def demo_db_path(tmpdir):
    path_db = str(tmpdir.join("test.sqlite3"))
    conn = sqlite3.connect(path_db)

    with conn:
        # Create table.
        conn.execute(SQL_CREATE)
        # Insert values into table.
        for i in range(3):
            conn.execute(
                SQL_INSERT,
                ("1", 1_000_000 + i, "CGAT"[i % 4], "CGAT"[(i + 1) % 4])
            )

    return path_db

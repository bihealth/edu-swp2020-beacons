import sqlite3
import vcf
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

@pytest.fixture
def demo_vcf_file(tmpdir):
#create and write vcf file
    vcf_file = tmpdir.join("demo.vcf")
    vcf_writer = vcf.Writer(open(vcf_file, 'w'))
    vcf_writer.write_record(Record(CHROM=20, POS=14370, REF=G, ALT=[A]))
    return vcf_file
    
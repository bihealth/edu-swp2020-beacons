import sqlite3
import vcf
import pytest
import os
import tempfile
import requests
import flask
from the_module.beacon import flask_app

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
    #create vcf file
    vcf_file = tmpdir.join("demo.vcf")
    vcf_file.write("##fileformat=VCFv4.3\n")
    vcf_file.write("##fileDate=20090805\n")
    vcf_file.write("##source=myImputationProgramV3.1\n")
    vcf_file.write("##reference=file:///seq/references/1000GenomesPilot-NCBI36.fasta\n")
    vcf_file.write('##contig=<ID=20,length=62435964,assembly=B36,md5=f126cdf8a6e0c7f379d618ff66beb2da,species="Homo sapiens",taxonomy=x>\n')
    vcf_file.write("##phasing=partial\n")
    vcf_file.write('##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of Samples With Data">\n')
    vcf_file.write('##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">\n')
    vcf_file.write('##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">\n')
    vcf_file.write('##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">\n')
    vcf_file.write('##INFO=<ID=DB,Number=0,Type=Flag,Description="dbSNP membership, build 129">\n')
    vcf_file.write('##INFO=<ID=H2,Number=0,Type=Flag,Description="HapMap2 membership">\n')
    vcf_file.write('##FILTER=<ID=q10,Description="Quality below 10">\n')
    vcf_file.write('##FILTER=<ID=s50,Description="Less than 50% of samples have data">\n')
    vcf_file.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
    vcf_file.write('##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">\n')
    vcf_file.write('##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">\n')
    vcf_file.write('##FORMAT=<ID=HQ,Number=2,Type=Integer,Description="Haplotype Quality">\n')
    vcf_file.write("#CHROM POS      ID         REF   ALT    QUAL  FILTER   INFO                             FORMAT       NA00001         NA00002          NA00003\n")
    vcf_file.write("20     14370    rs6054257  G     A      29    PASS    NS=3;DP=14;AF=0.5;DB;H2           GT:GQ:DP:HQ  0|0:48:1:51,51  1|0:48:8:51,51   1/1:43:5:.,.\n")
    vcf_file.write("20     17330    .          T     A      3     q10     NS=3;DP=11;AF=0.017               GT:GQ:DP:HQ  0|0:49:3:58,50  0|1:3:5:65,3     0/0:41:3\n")
    vcf_file.write("20     1110696  rs6040355  A     G,T    67    PASS    NS=2;DP=10;AF=0.333,0.667;AA=T;DB GT:GQ:DP:HQ  1|2:21:6:23,27  2|1:2:0:18,2     2/2:35:4\n")
    vcf_file.write("20     1230237  .          T     .      47    PASS    NS=3;DP=13;AA=T                   GT:GQ:DP:HQ  0|0:54:7:56,60  0|0:48:4:51,51   0/0:61:2\n")
    vcf_file.write("20     1234567  microsat1  GTC   G,GTCT 50    PASS    NS=3;DP=9;AA=G                    GT:GQ:DP     0/1:35:4        0/2:17:2         1/1:40:3")
    return vcf_file

@pytest.fixture
def client():
   # flask_app.app.config['TESTING'] = True
    return flask_app.app.test_client() 

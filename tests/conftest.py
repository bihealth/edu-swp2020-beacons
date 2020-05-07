import sqlite3
import pytest
from beacon import flask_app
import csv


SQL_CREATE1 = r"""
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
);
"""

SQL_CREATE2 = r"""
CREATE TABLE IF NOT EXISTS populations (
    id integer PRIMARY KEY AUTOINCREMENT,
    chr text NOT NULL,
    pos integer NOT NULL,
    ref text NOT NULL,
    alt text NOT NULL,
    wildtype integer NOT NULL,
    alt_hetero integer NOT NULL,
    alt_homo integer NOT NULL,
    hemi_ref integer NOT NULL,
    hemi_alt integer NOT NULL,
    population text NOT NULL
);
"""

SQL_CREATE3 = r"""
CREATE TABLE IF NOT EXISTS phenotype (
    id integer PRIMARY KEY AUTOINCREMENT,
    chr text NOT NULL,
    pos integer NOT NULL,
    ref text NOT NULL,
    alt text NOT NULL,
    phenotype text
);
"""

SQL_IDX1 = r"""
CREATE INDEX allel_idx ON allel(chr,pos,ref,alt);
"""

SQL_IDX2 = r"""
CREATE INDEX population_idx ON populations(chr,pos,ref,alt);
"""

SQL_IDX3 = r"""
CREATE INDEX pheno_idx ON phenotype(chr,pos,ref,alt);
"""

SQL_INSERT_ALLEL = r"""
INSERT INTO allel (chr, pos, ref, alt, wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

SQL_INSERT_POP = r"""
INSERT INTO populations (chr, pos, ref, alt, wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt, population)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""
SQL_INSERT_PHE = r"""
INSERT INTO phenotype (chr, pos, ref, alt, phenotype)
VALUES (?, ?, ?, ?, ?);
"""

@pytest.fixture
def demo_empty_db(tmpdir):
    path_db = str(tmpdir.join("test.sqlite3"))
    conn = sqlite3.connect(path_db)
    with conn:
        # Creates tables.
        c = conn.cursor()
        c.execute(SQL_CREATE1)
        c.execute(SQL_CREATE2)
        c.execute(SQL_CREATE3)
        c.execute(SQL_IDX1)
        c.execute(SQL_IDX2)
        c.execute(SQL_IDX3)
        conn.commit()
        c.close()
    conn.close()
    return path_db

@pytest.fixture
def demo_db_path(tmpdir):
    path_db = str(tmpdir.join("test.sqlite3"))
    conn = sqlite3.connect(path_db)
    with conn:
        # Creates tables.
        c = conn.cursor()
        c.execute(SQL_CREATE1)
        c.execute(SQL_CREATE2)
        c.execute(SQL_CREATE3)
        c.execute(SQL_IDX1)
        c.execute(SQL_IDX2)
        c.execute(SQL_IDX3)
        # Insert values into table.
        for i in range(3):
            c.execute(
                SQL_INSERT_ALLEL,
                (
                    "1",
                    1_000_000 + i,
                    "CGAT"[i % 4],
                    "CGAT"[(i + 1) % 4],
                    i + 3,
                    i,
                    i + 5,
                    0,
                    0,
                ),
            )
        for i in range(3):
            c.execute(
                SQL_INSERT_POP,
                (
                    "1",
                    1_000_000 + i,
                    "CGAT"[i % 4],
                    "CGAT"[(i + 1) % 4],
                    i + 3,
                    i,
                    i + 5,
                    0,
                    0,
                    ["GBR", "GBR", "PER", "KEN"][(i + 1) % 4],
                ),
            )
        for i in range(3):
            c.execute(
                SQL_INSERT_PHE,
                (
                    "1",
                    1_000_000 + i,
                    "CGAT"[i % 4],
                    "CGAT"[(i + 1) % 4],
                    ["neuronal", "epidermis", "muskulär", None][(i + 1) % 4],
                ),
            )
        conn.commit()
        c.close()
    conn.close()
    return path_db


@pytest.fixture
def demo_vcf_file(tmpdir):
    # create vcf file
    tmpdir.join("demo.vcf")
    with open("demo2.vcf",'w') as vcf_file:

        vcf_file.write("##fileformat=VCFv4.3\n")
        vcf_file.write("##fileDate=20090805\n")
        vcf_file.write("##source=myImputationProgramV3.1\n")
        vcf_file.write("##reference=file:///seq/references/1000GenomesPilot-NCBI36.fasta\n")
        vcf_file.write(
            '##contig=<ID=20,length=62435964,assembly=B36,md5=f126cdf8a6e0c7f379d618ff66beb2da,species="Homo sapiens",taxonomy=x>\n'
        )
        vcf_file.write("##phasing=partial\n")
        vcf_file.write(
            '##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of Samples With Data">\n'
        )
        vcf_file.write('##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">\n')
        vcf_file.write(
            '##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">\n'
        )
        vcf_file.write(
            '##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">\n'
        )
        vcf_file.write(
            '##INFO=<ID=DB,Number=0,Type=Flag,Description="dbSNP membership, build 129">\n'
        )
        vcf_file.write(
            '##INFO=<ID=H2,Number=0,Type=Flag,Description="HapMap2 membership">\n'
        )
        vcf_file.write('##FILTER=<ID=q10,Description="Quality below 10">\n')
        vcf_file.write(
            '##FILTER=<ID=s50,Description="Less than 50% of samples have data">\n'
        )
        vcf_file.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
        vcf_file.write(
            '##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">\n'
        )
        vcf_file.write('##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">\n')
        vcf_file.write(
            '##FORMAT=<ID=HQ,Number=2,Type=Integer,Description="Haplotype Quality">\n'
        )
        vcf_file.write(
            "#CHROM POS      ID         REF   ALT    QUAL  FILTER   INFO                             FORMAT       HG00174         HG00179          HG00148\n"
        )
        vcf_file.write(
            "20     14370    rs6054257  G     A      29    PASS    NS=3;DP=14;AF=0.5;DB;H2           GT:GQ:DP:HQ  0|0:48:1:51,51  1|0:48:8:51,51   1/1:43:5:.,.\n"
        )
        vcf_file.write(
            "20     17330    .          T     A      3     q10     NS=3;DP=11;AF=0.017               GT:GQ:DP:HQ  0|0:49:3:58,50  0|1:3:5:65,3     0/0:41:3\n"
        )
        vcf_file.write(
            "X     1110696  rs6040355  A     G,T    67    PASS    NS=2;DP=10;AF=0.333,0.667;AA=T;DB GT:GQ:DP:HQ  1|2:21:6:23,27  2|1:2:0:18,2     2/2:35:4\n"
        )
    return 'demo2.vcf'

@pytest.fixture
def client():
    # flask_app.app.config['TESTING'] = True
    return flask_app.app.test_client()


@pytest.fixture
def demo_pop_file(tmpdir):
    # create pop file
    tmpdir.join("demo_pop.tsv")
    pop_file = open("demo_pop.tsv", 'w')
    with pop_file as pf:
        fnames = ['Sample name', 'Sex', 'Population code']
        writer = csv.DictWriter(pf, fieldnames=fnames, delimiter='\t')
        writer.writeheader()
        writer.writerow({'Sample name':'HG00174', 'Sex':'female', 'Population code':'FIN'})
        writer.writerow({'Sample name':'HG00179', 'Sex':'female', 'Population code':'FIN'})
        writer.writerow({'Sample name':'HG00148', 'Sex':'male', 'Population code':'GBR'})
    return 'demo_pop.tsv'

@pytest.fixture
def demo_pheno_file(tmpdir):
    # create pop file
    tmpdir.join("demo_pheno.tsv")
    pheno_file = open("demo_pheno.tsv", 'w')
    with pheno_file as pf:
        fnames = ['entrez-gene-id','entrez-gene-symbol','HPO-Term-ID','HPO-Term-Name']
        writer = csv.DictWriter(pf, fieldnames=fnames, delimiter='\t')
        writer.writeheader()
        writer.writerow({'entrez-gene-id':'8192', 'entrez-gene-symbol':'CLPP', 'HPO-Term-ID':'HP:0004322', 'HPO-Term-Name':'Short stature'})
        writer.writerow({'entrez-gene-id':'8192', 'entrez-gene-symbol':'CLPP', 'HPO-Term-ID':'HP:0000007', 'HPO-Term-Name':'Autosomal recessive inheritance'})
        writer.writerow({'entrez-gene-id':'8192', 'entrez-gene-symbol':'CLPP', 'HPO-Term-ID':'HP:0000013', 'HPO-Term-Name':'Hypoplasia of the uterus'})
    return 'demo_pheno.tsv'
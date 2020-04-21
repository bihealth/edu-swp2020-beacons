from beacon import admin_cli
import pytest  # noqa


def test_path():
    admin_cli.input = lambda input: "demo_db_path"
    out = admin_cli.path()
    assert out is not None
    assert out == admin_cli.input("")


def test_parser(demo_vcf_file):
    parser = admin_cli.parse_args(
        [
            "-ct",
            "-vcf",
            str(demo_vcf_file),
            "-fd",
            "-p",
            "-c",
            "-u",
            "1",
            "1",
            "A",
            "A",
            "1",
            "-d",
            "1",
        ]
    )

    ct = parser.create_table
    vcf = parser.insert_data
    fd = parser.find_dup
    p = parser.print_db
    c = parser.count_variants
    u = parser.update
    d = parser.delete

    assert ct is True
    assert vcf is not None
    assert fd is True
    assert p is True
    assert c is True
    assert u is not None
    assert d is not None


def test_main(demo_db_path, demo_vcf_file):
    parser = admin_cli.parse_args(
        [
            "-ct",
            "-vcf",
            str(demo_vcf_file),
            "-fd",
            "-p",
            "-c",
            "-u",
            "1",
            "1",
            "A",
            "A",
            "1",
            "-d",
            "1",
        ]
    )
    out = admin_cli.main(demo_db_path, parser)
    assert out is not None
    assert out is True

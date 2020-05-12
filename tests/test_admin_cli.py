from beacon import admin_cli
import pytest  # noqa
import sys


def test_path_exist(monkeypatch, demo_db_path):
    def mock_input(x):
        if x == "DB Name: ":
            return "test.sqlite3"

    monkeypatch.setattr("builtins.input", mock_input)
    monkeypatch.setattr(
        "os.path.dirname", lambda x: demo_db_path[: len(demo_db_path) - 12]
    )
    out = admin_cli.path()
    assert out[0] is True
    assert out[1] == demo_db_path


def test_path_not_exist_create(monkeypatch, tmpdir):
    def mock_input(x):
        if x == "DB Name: ":
            return "test.sqlite3"
        else:
            return "y"

    monkeypatch.setattr("builtins.input", mock_input)
    monkeypatch.setattr("os.path.dirname", lambda x: tmpdir)
    out = admin_cli.path()
    assert out[0] is True
    assert out[1] == str(tmpdir.join("test.sqlite3"))


def test_path_not_exist_exit(monkeypatch):
    def mock_input(x):
        if x == "DB Name: ":
            return "test.sqlite3"
        elif (
            x == "Given database does not exist. Do you want to create a new one? [y/n]"
        ):
            return "n"
        else:
            return "y"

    monkeypatch.setattr("builtins.input", mock_input)
    out = admin_cli.path()
    assert out[0] is False
    assert out[1] == ""


def test_path_not_exist_x(monkeypatch):
    def mock_input(x):
        if x == "DB Name: ":
            return "test.sqlite3"
        else:
            return "x"

    monkeypatch.setattr("builtins.input", mock_input)
    out = admin_cli.path()
    assert out[0] is False
    assert out[1] == ""


def test_path_not_exist_continue(monkeypatch, capsys):
    def mock_input(x):
        if x == "DB Name: ":
            return "test.sqlite3"
        elif (
            x == "Given database does not exist. Do you want to create a new one? [y/n]"
        ):
            return "n"
        else:
            return "n"

    monkeypatch.setattr("builtins.input", mock_input)
    out = admin_cli.path()
    print_out = capsys.readouterr()
    assert out[0] is False
    assert out[1] == ""
    assert "The process is starting from the beginning." in print_out[0]


def test_path_not_exist_wrong_input(monkeypatch, capsys):
    def mock_input(x):
        if x == "DB Name: ":
            return "test.sqlite3"
        elif (
            x == "Given database does not exist. Do you want to create a new one? [y/n]"
        ):
            return "n"
        else:
            return "x"

    monkeypatch.setattr("builtins.input", mock_input)
    out = admin_cli.path()
    print_out = capsys.readouterr()
    assert out[0] is False
    assert out[1] == ""
    assert (
        "Your input has the wrong format. The process is starting from the beginning."
        in print_out[0]
    )


def test_parse_args(demo_vcf_file, demo_pop_file, demo_pheno_file):
    parser = admin_cli.parse_args(
        [
            "-ct",
            "-vcf",
            str([demo_vcf_file, demo_pop_file, demo_pheno_file]),
            "-p",
            "-c",
            "-ua",
            "1",
            "1",
            "A",
            "A",
            "1",
            "2",
            "3",
            "0",
            "0",
            "0",
            "-up",
            "1",
            "1",
            "A",
            "A",
            "1",
            "2",
            "3",
            "0",
            "0",
            "0",
            "PER",
            "-upt",
            "1",
            "1",
            "A",
            "A",
            "1",
            "muscle",
            "-da",
            "1",
            "-dp",
            "1",
            "-dpt",
            "1",
            "-ctu",
            "-add",
            "Julia",
            "1",
            "-t",
            "Julia",
            "-pu",
            "-du",
            "1",
            "-pi",
            "-di",
            "1",
        ]
    )
    ct = parser.create_tables
    vcf = parser.insert_data
    p = parser.print_db
    c = parser.count_variants
    ua = parser.update_allel
    up = parser.update_populations
    upt = parser.update_phenotype
    da = parser.delete_allel
    dp = parser.delete_populations
    dpt = parser.delete_phenotype
    ctu = parser.create_tables_user
    add = parser.insert_user
    t = parser.find_user_token
    pu = parser.print_db_user
    du = parser.delete_user
    pi = parser.print_ip
    di = parser.delete_ip
    assert ct is True
    assert isinstance(vcf, list)
    assert p is True
    assert isinstance(c, int)
    assert isinstance(ua, list)
    assert isinstance(up, list)
    assert isinstance(upt, list)
    assert da == "1"
    assert dp == "1"
    assert dpt == "1"
    assert ctu is True
    assert isinstance(add, list)
    assert isinstance(t, str)
    assert pu is True
    assert du == "1"
    assert pi is True
    assert di == "1"


def test_main(demo_db_path, demo_vcf_file, demo_pop_file, demo_pheno_file, monkeypatch):
    def mock_input(x):
        if x == "DB Name: ":
            return "test.sqlite3"

    monkeypatch.setattr("builtins.input", mock_input)
    monkeypatch.setattr(
        "os.path.dirname", lambda x: demo_db_path[: len(demo_db_path) - 12]
    )
    sys.argv = []
    sys.argv.append("f")
    sys.argv.append("-ct")
    out = admin_cli.main(sys.argv)
    assert isinstance(out, str)

    sys.argv = []
    sys.argv.append("f")
    sys.argv.append("-vcf")
    sys.argv.append([str(demo_vcf_file), str(demo_pop_file), str(demo_pheno_file)])
    out = admin_cli.main(sys.argv)
    assert out is True

    sys.argv = []
    sys.argv.append("f")
    sys.argv.append("-p")
    out = admin_cli.main(sys.argv)
    assert out == ""

    sys.argv = []
    sys.argv.append("f")
    sys.argv.append("-c")
    out = admin_cli.main(sys.argv)
    assert isinstance(out, int)

    sys.argv = ["f", "-ua", "1", "1", "A", "A", "1", "2", "3", "0", "0", "0"]
    out = admin_cli.main(sys.argv)
    assert isinstance(out, str)

    sys.argv = ["f", "-up", "1", "1", "A", "A", "1", "2", "3", "0", "0", "0", "PER"]
    out = admin_cli.main(sys.argv)
    assert isinstance(out, str)

    sys.argv = ["f", "-upt", "1", "1", "A", "A", "1", "muscle"]
    out = admin_cli.main(sys.argv)
    assert isinstance(out, str)

    sys.argv = ["f", "-da", "1"]
    out = admin_cli.main(sys.argv)
    assert isinstance(out, str)

    sys.argv = ["f", "-dp", "1"]
    out = admin_cli.main(sys.argv)
    assert isinstance(out, str)

    sys.argv = ["f", "-dpt", "1"]
    out = admin_cli.main(sys.argv)
    assert isinstance(out, str)

    sys.argv = ["f", "-dpt", "1"]
    out = admin_cli.main(sys.argv)
    assert isinstance(out, str)

    sys.argv = ["f", "-ctu"]
    out = admin_cli.main(sys.argv)
    assert out is True

    sys.argv = ["f", "-add", "Julia", "1"]
    out = admin_cli.main(sys.argv)
    assert out is True

    sys.argv = ["f", "-t", "Julia"]
    out = admin_cli.main(sys.argv)
    assert isinstance(out, str)

    sys.argv = ["f", "-pu"]
    out = admin_cli.main(sys.argv)
    assert out == ""

    sys.argv = ["f", "-du", "1"]
    out = admin_cli.main(sys.argv)
    assert isinstance(out, str)

    sys.argv = ["f", "-pi"]
    out = admin_cli.main(sys.argv)
    assert out == ""

    sys.argv = ["f", "-di", "1"]
    out = admin_cli.main(sys.argv)
    assert isinstance(out, str)

    sys.argv = ["f"]
    out = admin_cli.main(sys.argv)
    assert (
        "Please enter a flag. To see which flags you can use, use -h or --help" in out
    )

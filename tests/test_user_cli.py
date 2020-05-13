import pytest  # noqa
from beacon import user_cli
import requests_mock
from . import test_image
import requests

input_check_input = [("1-1-A-A", True), ("3-4-X-T", False), ("1.1.A.T.", False)]
inputs2 = [
    (
        "1-1-A-A",
        "q",
        [
            "Welcome to our project beacon software!",
            "",
            "The result of your request is:",
            "1 - 1 - A - A - True ",
            "",
            "Thank you for using our tool.",
            "",
        ],
    ),
    (
        "3-4-X-T",
        "q",
        [
            "Welcome to our project beacon software!",
            "",
            "Your input has the wrong format. For futher information tipp --help.",
            "Thank you for using our tool.",
            "",
        ],
    ),
    (
        "1.1.A.T.",
        "x",
        [
            "Welcome to our project beacon software!",
            "",
            "Your input has the wrong format. For futher information tipp --help.",
            "You did not choose an understandible input. Your session is quited now.",
            "Thank you for using our tool.",
            "",
        ],
    ),
]


@pytest.mark.parametrize("var,sig,output", inputs2)
@requests_mock.Mocker(kw="mock")
def test_init(var, sig, output, monkeypatch, capsys, **kwargs):
    monkeypatch.setattr(user_cli, "_check_input", lambda x: True)
    monkeypatch.setattr(
        user_cli, "verify_token",
    )
    monkeypatch.settattr(
        user_cli, "string_to_dict",
    )
    monkeypatch.settattr(
        user_cli, "query_request",
    )
    monkeypatch.settattr(
        user_cli, "print_results",
    )

    def mock_input(x):
        if (
            x
            == "Please ebter your secret token or enter nothing to continue as not registered user: "
        ):
            return token
        elif x == "Please enter your variant (chr-pos-ref-alt):\n":
            return var
        else:
            return sig

    monkeypatch.setattr("builtins.input", mock_input)
    user_cli.main()

    captured = capsys.readouterr().out.split("\n")
    for i in range(len(output)):
        assert captured[i] == output[i]


input_verify_token = [
    ("wild_card", True, "Bob", None, "", (True, "Bob")),
    ("wild_card", False, None, None, "This is not a valid token.\n", (False, None)),
    ("wild_card", None, None, "An error occured.", "", (None, "An error occured.")),
]


@pytest.mark.parametrize("inp,ver,user,err,pri,out", input_verify_token)
@requests_mock.Mocker(kw="mock")
def test_verify_token(inp, ver, user, err, pri, out, capsys, **kwargs):
    kwargs["mock"].post(
        "http://localhost:5000/api/verify",
        json={"verified": ver, "user": user, "error": err},
    )
    assert user_cli.verify_token(inp) == out
    captured = capsys.readouterr().out
    assert captured == pri


@pytest.mark.parametrize("inp,val", input_check_input)
def test__check_input(inp, val):
    assert user_cli._check_input(inp) == val


input_query_request = [
    (
        "1-1-A-A",
        "valid_token",
        {"alt": "A", "chr": "1", "error": None, "occ": False, "pos": "1", "ref": "A"},
        True,
    ),
    ("1-1-A-A", "valid_token", None, False),
]


@pytest.mark.parametrize("inp,token,outp,server", input_query_request)
@requests_mock.Mocker(kw="mock")
def test_query_request(inp, token, outp, server, capsys, **kwargs):
    if server:
        kwargs["mock"].post("http://localhost:5000/query", json=outp)
    else:
        kwargs["mock"].post(
            "http://localhost:5000/query", exc=requests.exceptions.ConnectionError
        )

    assert user_cli.query_request(inp, token) == (server, outp)


def test_string_to_dict():
    assert user_cli.string_to_dict("1-1-A-A") == {
        "alt": "A",
        "chr": "1",
        "pos": "1",
        "ref": "A",
    }


inputs_print_results = [
    (
        {"alt": "A", "chr": "1", "error": None, "occ": False, "pos": "1", "ref": "A"},
        [
            "The result of your request is:",
            "{'alt': 'A', 'chr': '1', 'error': None, 'occ': False, 'pos': '1', 'ref': 'A'}",
        ],
    ),
    (
        {
            "alt": "A",
            "chr": "20",
            "error": None,
            "occ": True,
            "pos": "14370",
            "ref": "G",
        },
        [
            "The result of your request is:",
            "{'alt': 'A', 'chr': '20', 'error': None, 'occ': True, 'pos': '14370', 'ref': 'G'}",
        ],
    ),
    (
        {
            "alt": "A",
            "chr": "20",
            "error": None,
            "frequency": 0.5,
            "occ": True,
            "phenotype": ["", ""],
            "population": {"FIN": 1, "GBR": 2},
            "pos": "14370",
            "ref": "G",
            "statistic": test_image.IMG_B64,
            "varCount": 6,
        },
        [
            "The result of your request is:",
            "{'alt': 'A', 'chr': '20', 'error': None, 'frequency': 0.5, 'occ': True, 'phenotype': ['', ''], 'population': {'FIN': 1, 'GBR': 2}, 'pos': '14370', 'ref': 'G', 'varCount': 6}",
        ],
    ),
    (
        {"alt": "A", "chr": "1", "error": None, "occ": None, "pos": "1", "ref": "A"},
        ["You are not allowed to make more requests from this IP-address."],
    ),
    (
        {
            "alt": "A",
            "chr": "1",
            "error": "no such table: allel",
            "occ": None,
            "pos": "1",
            "ref": "A",
        },
        [
            "We have troubles with the database, please ask your admin for help.",
            "The occuring error is: ' no such table: allel '",
        ],
    ),
]


@pytest.mark.parametrize("inp,val", inputs_print_results)
def test_print_results(inp, val, capsys):

    user_cli.print_results(inp)
    captured = capsys.readouterr().out.split("\n")

    for i in range(len(val)):
        assert captured[i] == val[i]

    # with capsys.disabled():
    #   print(captured)

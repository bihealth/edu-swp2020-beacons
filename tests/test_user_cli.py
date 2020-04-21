import pytest
from beacon import user_cli
import requests_mock

inputs = [("1-1-A-A", True), ("3-4-X-T", False), ("1.1.A.T.", False)]
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
    kwargs["mock"].get(
        "http://localhost:5000/api/1-1-A-A",
        json={"results": ["1", "1", "A", "A", True]},
    )
    # monkeypatch.setattr(user_cli, '_check_input', lambda x: True)
    def mock_input(x):
        if x == "Please enter your variant (chr-pos-ref-alt):\n":
            return var
        else:
            return sig

    monkeypatch.setattr("builtins.input", mock_input)
    user_cli.main()

    captured = capsys.readouterr().out.split("\n")
    for i in range(len(output)):
        assert captured[i] == output[i]


@pytest.mark.parametrize("inp,val", inputs)
def test__check_input(inp, val):
    assert user_cli._check_input(inp) == val

from . import test_image
import requests_mock
import pytest  # noqa
import re


def test_home(client):
    rv = client.get("http://localhost:4000/")
    b_true_chr = re.search(rv.data.decode("utf-8")[726:760], "1")
    b_true_pos = re.search(rv.data.decode("utf-8")[889:892], "1")
    b_true_ref = re.search(rv.data.decode("utf-8")[1010:1017], "A")
    b_true_alt = re.search(rv.data.decode("utf-8")[1137:1144], "A")

    b_false_chr = re.search(rv.data.decode("utf-8")[726:760], "Z")
    b_false_ref = re.search(rv.data.decode("utf-8")[1010:1017], "Z")
    b_false_alt = re.search(rv.data.decode("utf-8")[1137:1144], "Z")

    assert b_true_chr
    assert b_true_pos
    assert b_true_ref
    assert b_true_alt

    assert b_false_chr is None
    assert b_false_ref is None
    assert b_false_alt is None

    assert "Beacon" in rv.data.decode("utf-8")
    assert "SWP" in rv.data.decode("utf-8")
    assert "Submit" in rv.data.decode("utf-8")
    assert rv.status_code == 200


input_handle_correct = [
    ({"chr": "1", "pos": "1", "ref": "A", "alt": "A", "occ": True, "error": None}),
    ({"chr": "1", "pos": "1", "ref": "A", "alt": "A", "occ": False, "error": None}),
    ({"chr": "1", "pos": "1", "ref": "A", "alt": "A", "occ": None, "error": None}),
    (
        {
            "chr": "1",
            "pos": "1",
            "ref": "A",
            "alt": "A",
            "occ": True,
            "error": None,
            "statistic": test_image.IMG_B64,
        }
    ),
    (
        {
            "chr": "1",
            "pos": "1",
            "ref": "A",
            "alt": "A",
            "occ": True,
            "error": None,
            "statistic": None,
        }
    ),
]


@pytest.mark.parametrize("outdic", input_handle_correct)
@requests_mock.Mocker(kw="mock")
def test_handle_correct(outdic, client, monkeypatch, demo_db_path, **kwargs):
    kwargs["mock"].post("http://localhost:5000/query", json=outdic)

    rv = client.post(
        "http://localhost:4000/results",
        data={"token": "", "chr": "1", "pos": "1", "ref": "A", "alt": "A"},
        follow_redirects=True,
    )
    assert rv.status_code == 200
    assert b"Results" in rv.data
    assert (
        b"Your variant 1-1-A-A was found."
        or b"Your variant 1-1-A-A was not found."
        or b"An Error has occured: no such table: variants" in rv.data
    )
    assert b"go Home" in rv.data

    rt = client.post(
        "/results",
        data={"token": "ValidToken", "chr": "1", "pos": "1", "ref": "A", "alt": "A"},
    )
    assert b"Results" in rt.data
    assert (
        b"Your variant 1-1-A-A was found."
        or b"Your variant 1-1-A-A was not found."
        or b"An Error has occured: no such table: variants" in rt.data
    )
    assert b"go Home" in rt.data
    assert rt.status_code == 200


input_login = [
    ("Valid", "ValidToken", True, None),
    (None, "NoneValidToken", False, None),
    (None, "ErrorToken", None, "Error"),
    (None, None, None, "Error"),
]


@pytest.mark.parametrize("username,token,valid,error", input_login)
@requests_mock.Mocker(kw="mock")
def test_login(username, token, valid, error, client, **kwargs):
    kwargs["mock"].post(
        "http://localhost:5000/api/verify",
        json={"verified": valid, "user": username, "error": error},
    )
    rv = client.post("/login", data=dict(token=token), follow_redirects=True)
    assert rv.status_code == 200
    assert b"SWP" in rv.data
    assert b"Beacon" in rv.data
    assert b"Login" in rv.data

    rg = client.get("/login")
    assert rg.status_code == 200
    assert b"SWP" in rg.data
    assert b"Beacon" in rg.data
    assert b"Login" in rg.data
    assert b"Cancel" in rg.data

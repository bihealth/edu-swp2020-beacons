from beacon import web_ui
from beacon import database
from beacon import settings
import requests
import requests_mock
import pytest  # noqa
import re
import json


def test_home(client):
    rv = client.get("http://localhost:4000/")
    b_true_chr = re.search(rv.data.decode("utf-8")[909:943], "1")
    b_true_pos = re.search(rv.data.decode("utf-8")[1072:1075], "1")
    b_true_ref = re.search(rv.data.decode("utf-8")[1193:1200], "A")
    b_true_alt = re.search(rv.data.decode("utf-8")[1320:1327], "A")

    b_false_chr = re.search(rv.data.decode("utf-8")[909:943], "Z")
    b_false_ref = re.search(rv.data.decode("utf-8")[1193:1200], "Z")
    b_false_alt = re.search(rv.data.decode("utf-8")[1320:1327], "Z")

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


# @requests_mock.Mocker(kw = "mock")
def test_handle_correct(client, monkeypatch, demo_db_path, **kwargs):

    monkeypatch.setattr(settings, "PATH_LOGIN", demo_db_path)
    # assert b"Results" in rg.data

    # rv = client.post("http://localhost:4000/results", data = {"token": "", "chr": "1", "pos": "1", "ref": "A", "alt": "A"}) # follow_redirects = True
    # assert rv.status_code == 200
    # kwargs["mock"].post(requests_mock.ANY, json={'chr': "1", 'pos': "1", "ref": "A", "alt": "A", "occ": True, "error": None})

    # print(json.loads(rv.data.decode("utf-8")))
    # print(rv.data)
    # assert True == False
    # assert b"Results" in rv.data
    # assert (
    #     b"Your variant 1-1-A-A was found."
    #     or b"Your variant 1-1-A-A was not found."
    #     or b"An Error has occured: no such table: variants" in rv.data
    # )
    # assert b"go Home" in rv.data

    # rt = client.post("/results", data={"token":"doggy", "chr": "1", "pos": "1", "ref": "A", "alt": "A"})
    # assert b"Results" in rt.data
    # assert (
    #     b"Your variant 1-1-A-A was found."
    #     or b"Your variant 1-1-A-A was not found."
    #     or b"An Error has occured: no such table: variants" in rt.data
    # )
    # assert b"go Home" in rt.data
    # assert rt.status_code == 200


input_login = [("Peter", "pete"), ("Lilly", "lil"), ("UndercoverDog", "doggy")]


@pytest.mark.parametrize("username,token", input_login)
@requests_mock.Mocker(kw="mock")
def test_login(username, token, client, **kwargs):
    rg = client.get("/login")
    assert rg.status_code == 200
    assert b"SWP" in rg.data
    assert b"Beacon" in rg.data
    assert b"Login" in rg.data
    assert b"Login" in rg.data
    assert b"Cancel" in rg.data

    rv = client.post("/login", data=dict(token=token), follow_redirects=True)
    resp = kwargs["mock"].post(
        "http://localhost:5000/api/verify",
        json={"verified": True, "user": username, "error": None},
    )
    assert rv.status_code == 200

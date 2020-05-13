import pytest  # noqa
from beacon import rest_api
from beacon import settings
import json


def test_get_api(monkeypatch, demo_db_path):

    monkeypatch.setattr(settings, "PATH_DATABASE", demo_db_path)
    monkeypatch.setattr(settings, "PATH_LOGIN", demo_db_path)

    inp_dict = {
        "chr": 1,
        "pos": 1000000,
        "ref": "C",
        "alt": "G",
    }

    resp = rest_api.app.test_client().post(
        "http://localhost:5000/query", json=inp_dict, headers={"token": ""}
    )
    out0 = resp.json["occ"]
    out = json.loads(resp.data.decode("utf-8"))
    resp1 = rest_api.app.test_client().post(
        "http://localhost:5000/query", json=inp_dict, headers={"token": "johnny"}
    )
    out1 = resp1.json["statistic"]

    for i in range(21):
        resp2 = rest_api.app.test_client().post(
            "http://localhost:5000/query", json=inp_dict, headers={"token": ""}
        )

    out2 = resp2.json["occ"]

    assert out0 is True
    assert out == {
        "alt": "G",
        "chr": 1,
        "error": None,
        "occ": True,
        "pos": 1000000,
        "ref": "C",
    }
    assert out1 is not None
    assert out2 is None


def test_error_get_api(monkeypatch, demo_empty_db):

    inp_dict = {
        "chr": 1,
        "pos": 1000000,
        "ref": "C",
        "alt": "G",
    }

    monkeypatch.setattr(settings, "PATH_DATABASE", demo_empty_db)
    monkeypatch.setattr(settings, "PATH_LOGIN", demo_empty_db)
    rest_api.app.test_client().post(
        "http://localhost:5000/query", json=inp_dict, headers={"token": ""}
    )

    assert "no such table: ip"


def test_request_permission(monkeypatch, demo_db_path):

    monkeypatch.setattr(settings, "PATH_LOGIN", demo_db_path)

    out1 = rest_api.request_permission("192.0.2.40", "")
    out2 = rest_api.request_permission("197.0.3.1", "pete")
    out3 = rest_api.request_permission("192.0.2.41", "lil")
    out5 = rest_api.request_permission("192.0.2.41", "doggy")

    for i in range(21):
        out4 = rest_api.request_permission("192.0.2.40", "")

    assert out1 == (1, None)
    assert out2 == (0, None)
    assert out3 == (1, None)
    assert out4 == (0, None)
    assert out5 == (2, None)


def test_verify_user(monkeypatch, demo_db_path):

    monkeypatch.setattr(settings, "PATH_LOGIN", demo_db_path)

    resp = rest_api.app.test_client().post(
        "http://localhost:5000/api/verify", headers={"token": "non existent"}
    )
    out = json.loads(resp.data.decode("utf-8"))
    out0 = resp.json["verified"]
    resp1 = rest_api.app.test_client().post(
        "http://localhost:5000/api/verify", headers={"token": "pete"}
    )
    out1 = resp1.json["verified"]
    out2 = json.loads(resp1.data.decode("utf-8"))

    assert out0 is False
    assert out == {"error": None, "user": None, "verified": False}
    assert out1 is True
    assert out2 == {"error": None, "user": "Peter", "verified": True}


def test_error_request_permission(monkeypatch, demo_empty_db):

    monkeypatch.setattr(settings, "PATH_LOGIN", demo_empty_db)
    out = rest_api.request_permission("192.0.2.40", "")

    assert out[0] is None


def test_error_verify_user(monkeypatch, demo_empty_db):

    monkeypatch.setattr(settings, "PATH_LOGIN", demo_empty_db)
    rest_api.app.test_client().post(
        "http://localhost:5000/api/verify", headers={"token": None}
    )

    assert "no such table: login"

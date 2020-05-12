import pytest  # noqa
import flask
#from flask import request
from beacon import rest_api
from beacon import common
from beacon import admin_tools
from beacon import admin_cli
from beacon import database
from beacon import settings
import json


# def test_get_api(monkeypatch, demo_db_path):

#     monkeypatch.setattr(settings, "PATH_LOGIN", demo_db_path)
#     #monkeypatch.setattr("flask.request.remote_addr", "192.0.2.40" )

#     con = database.ConnectDatabase(demo_db_path)
#     od = admin_tools.OperateDatabase()
#     od.print_db(con)

#     # con = database.ConnectDatabase(demo_db_path)
#     udb = admin_tools.UserDB()
#     udb.print_ip(con)

#     inp_dict = {
#         "chr": '1',
#         "pos": 1000000,
#         "ref": 'C',
#         "alt": 'G',
#     }

#     resp = rest_api.app.test_client().post("http://localhost:5000/query", json=inp_dict, headers={"token": None})
#     #out = json.loads(resp.data.decode("utf-8"))
#     out = resp.json['error']
#     print(out)
#     # out = json.dumps(resp)
#     assert out is True


def test_request_permission(monkeypatch, demo_db_path):

    monkeypatch.setattr(settings, "PATH_LOGIN", demo_db_path)

    out1 = rest_api.request_permission('192.0.2.40',None)
    out2 = rest_api.request_permission('197.0.3.1','pete')
    out3 = rest_api.request_permission('192.0.2.41','lil')

    for i in range(51):
        out4 = rest_api.request_permission('192.0.2.40',None)

    assert out1 == (1, None)
    assert out2 == (0, None)
    assert out3 == (1, None)
    assert out4 == (0, None)

def test_verify_user(monkeypatch, demo_db_path):

    monkeypatch.setattr(settings, "PATH_LOGIN", demo_db_path)

    # con = database.ConnectDatabase(demo_db_path)
    # udb = admin_tools.UserDB()
    # udb.print_db_user(con)

    resp = rest_api.app.test_client().post("/api/verify", headers={"token": 'non existent'})
    out = json.loads(resp.data.decode("utf-8"))
    out0 = resp.json['verified']
    resp1 = rest_api.app.test_client().post("/api/verify", headers={"token": 'pete'})
    out1 = resp1.json['verified']
    out2 = json.loads(resp1.data.decode("utf-8"))

    assert out0 is False
    assert out == {'error': None, 'user': None, 'verified': False}
    assert out1 is True
    assert out2 == {'error': None, 'user': 'Peter', 'verified': True}

# def test_error_verify_user(monkeypatch, demo_empty_db):
#     monkeypatch.setattr(settings, "PATH_LOGIN", demo_empty_db)
#     resp = rest_api.app.test_client().post("/api/verify", headers={"token": 'non existent'})
#     out = resp.json['verified']

#     assert out == 1
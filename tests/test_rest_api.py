import pytest

from beacon import rest_api
from beacon import common
import json

def test_annVar_ls():
    variant = common.Variant('1','1','A','A')
    occ1 = True
    occ2 = Exception("Error")
    output1 = rest_api.annVar_ls(variant, occ1)
    output2 = rest_api.annVar_ls(variant, occ2)
    assert output1[0] is '1'
    assert output1[1] is '1'
    assert output1[2] is 'A'
    assert output1[3] is 'A'
    assert output1[4] 
    assert type(output2[4]) is str


def test_get_api():
    response = rest_api.app.test_client().get("/api/1-1-A-A")
    out = json.loads(response.data.decode('utf-8')) 
    assert out["results"][0] is '1'
    assert response.status_code == 200
   
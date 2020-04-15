import pytest
from the_module.beacon import user_cli
import requests_mock
inputs = [("1-1-A-A",True), ("3-4-X-T",False),("1.1.A.T.",False)]
inputs2 = [("c", ""),("q",""),("x","")]
#
#@pytest.fixture
#def testserver():
#    from flask import Flask
#    app = Flask(__name__)
#    @app.route("/api/<var_str>", methods = ['GET'])
#    def get_api(var_str):
#        var = common.parse_var(var_str)
#        occ = True
#        return(jsonify(results=annVar_ls,o
#    


@requests_mock.Mocker(kw='mock')
def test_init(monkeypatch, capsys, **kwargs):
    kwargs['mock'].get('http://localhost:5000/api/1-1-A-A', json = {'results':['1','1','A','A','True']})
    monkeypatch.setattr(user_cli, '_check_input', lambda x: True)
    monkeypatch.setattr('builtins.input', lambda x: '1-1-A-A')
    user_cli.main()

    captured = capsys.readouterr()
    with capsys.disabled():
        print(captured.out)

@pytest.mark.parametrize("inp,val",inputs)
def test__check_input(inp,val):
    assert user_cli._check_input(inp) == val
    

import pytest
from the_module.beacon import user_cli as cli

inputs = ["1-1-A-A", "c","3-4-X-T","q"]


@pytest.fixture
def testserver():
    from flask import Flask
    app = Flask(__name__)
    @app.route("/api/<var_str>", methods = ['GET'])
    def get_api(var_str):
        var = common.parse_var(var_str)
        occ = True
        return(jsonify(results=annVar_ls,o
    


#@pytest.mark.parametrize("
def test_init(monkeypatch, capsys):
    monkeypatch.setattr('cli._check_input', labda x: True)
    monkeypatch.setattr('requests.get', lambda x: jsonify(results= [x.split('-')[1],x.split('-')[2],x.split('-')[3],x.split('-')[4], True]
    monkeypatch.setattr('builtins.input', lambda x: 19)
    cli.main()
    print("blubblub")
    print("keine ahnung wie es geht...")
    captured = capsys.readouterr()
    with capsys.disabled():
        print(captured.out.split("\n")[1])
    #captured = capsys.readouterr()


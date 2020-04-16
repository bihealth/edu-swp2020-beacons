import pytest
from the_module.beacon import user_cli
import requests_mock

inputs = [("1-1-A-A",True), ("3-4-X-T",False),("1.1.A.T.",False)]
inputs2 = [("1-1-A-A","q"),("3-4-X-T","q"),("1.1.A.T.","x")]



@pytest.mark.parametrize("var,sig", inputs2)
@requests_mock.Mocker(kw='mock')
def test_init(var,sig, monkeypatch, capsys, **kwargs):
    kwargs['mock'].get('http://localhost:5000/api/1-1-A-A', json = {'results':['1','1','A','A','True']})
    #monkeypatch.setattr(user_cli, '_check_input', lambda x: True)
    def mock_input(x):
        if x == "Please enter your variant (chr-pos-ref-alt):\n":
            return var
        else:
            return sig

    monkeypatch.setattr('builtins.input', mock_input)
    user_cli.main()

    captured = capsys.readouterr()
    with capsys.disabled():
        print(captured.out)

@pytest.mark.parametrize("inp,val",inputs)
def test__check_input(inp,val):
    assert user_cli._check_input(inp) == val
    

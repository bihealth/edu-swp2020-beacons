import pytest  # noqa
from beacon import common


def test_parse_var():
    input_str = "X-1-A-A"
    output = common.parse_var(input_str)
    assert isinstance(output, common.Variant) is True


def test_create_variant():
    variant = common.Variant("X", 1, "A", "A")
    assert isinstance(variant, common.Variant) is True


def test_create_annVar():
    annVar = common.AnnVar("X", 1, "A", "A", False)
    assert isinstance(annVar, common.AnnVar) is True


def test_create_Info():
    info = common.Info("X", 1, "A", "A", True, 10, {"GRB": 11}, None, 0.7, [None])
    assert isinstance(info, common.AnnVar) is True
    assert isinstance(info, common.Info) is True

import pytest  # noqa
from beacon import common


def test_parse_var():
    input_str = "X-1-A-A"
    output = common.parse_var(input_str)
    assert isinstance(output, common.Variant) is True

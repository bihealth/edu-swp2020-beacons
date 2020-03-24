import pytest  # noqa

from the_module import sub


def test_f():
    assert int(sub.f(2)) == 4

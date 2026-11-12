import pytest
from operations import power, square_root


def test_power():
    assert power(2, 4) == 16.0
    assert power(2, 3) == 8


def test_square_root():
    assert square_root(16) == 4.0
    assert square_root(0) == 0.0


def test_square_root_negative():
    with pytest.raises(ValueError):
        square_root(-9)

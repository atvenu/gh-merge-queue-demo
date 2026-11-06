import pytest
from operations import power, square_root


def test_power():
    assert power(2, 4) == 16.0


def test_square_root():
    assert square_root(25) == 5.0


def test_square_root_negative():
    with pytest.raises(ValueError):
        square_root(-9)

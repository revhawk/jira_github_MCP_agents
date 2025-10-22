import pytest
from modules.input_validation import divide

def test_divide_positive_numbers():
    assert divide(10.0, 2.0) == 5.0

def test_divide_negative_numerator():
    assert divide(-10.0, 2.0) == -5.0

def test_divide_negative_denominator():
    assert divide(10.0, -2.0) == -5.0

def test_divide_both_negative():
    assert divide(-10.0, -2.0) == 5.0

def test_divide_floats():
    assert divide(7.5, 2.5) == 3.0

def test_divide_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError):
        divide(10.0, 0.0)

def test_divide_zero_numerator():
    assert divide(0.0, 5.0) == 0.0

def test_divide_large_numbers():
    assert divide(1e308, 1e308) == 1.0

def test_divide_small_numbers():
    assert divide(1e-308, 1e-308) == 1.0

def test_divide_large_by_small():
    assert divide(1e308, 1e-308) == 1e616

def test_divide_small_by_large():
    assert divide(1e-308, 1e308) == 0.0

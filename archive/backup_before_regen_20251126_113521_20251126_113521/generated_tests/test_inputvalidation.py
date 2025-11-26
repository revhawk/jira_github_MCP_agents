import pytest
from modules.inputvalidation import divide, percentage_conversion

# Tests for divide function
def test_divide_normal():
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

def test_divide_very_small_values():
    assert divide(1e-10, 1e-5) == pytest.approx(1e-5)

def test_divide_very_large_values():
    assert divide(1e10, 1e5) == 1e5

# Tests for percentage_conversion function
def test_percentage_conversion_normal():
    assert percentage_conversion(50.0) == 0.5

def test_percentage_conversion_zero():
    assert percentage_conversion(0.0) == 0.0

def test_percentage_conversion_negative():
    assert percentage_conversion(-50.0) == -0.5

def test_percentage_conversion_very_small_value():
    assert percentage_conversion(1e-10) == 1e-12

def test_percentage_conversion_very_large_value():
    assert percentage_conversion(1e10) == 1e8

import pytest
from modules.calculator import add, subtract, multiply, divide, negate, percentage_conversion

# Tests for add function
def test_add_positive():
    assert add(2.5, 3.1) == pytest.approx(5.6)

def test_add_negative():
    assert add(-2, -3) == -5

def test_add_mixed():
    assert add(-2, 3) == 1

def test_add_zero():
    assert add(0, 0) == 0

def test_add_float_precision():
    assert add(0.1, 0.2) == pytest.approx(0.3)

# Tests for subtract function
def test_subtract_positive():
    assert subtract(5, 3) == 2

def test_subtract_negative():
    assert subtract(-5, -3) == -2

def test_subtract_mixed():
    assert subtract(5, -3) == 8

def test_subtract_to_negative():
    assert subtract(3, 5) == -2

def test_subtract_zero():
    assert subtract(0, 0) == 0

# Tests for multiply function
def test_multiply_positive():
    assert multiply(3, 4) == 12

def test_multiply_negative():
    assert multiply(-3, -4) == 12

def test_multiply_mixed():
    assert multiply(-3, 4) == -12

def test_multiply_zero():
    assert multiply(3, 0) == 0

def test_multiply_large_numbers():
    assert multiply(1e10, 1e10) == 1e20

# Tests for divide function
def test_divide_positive():
    assert divide(10, 5) == 2

def test_divide_negative():
    assert divide(-10, -5) == 2

def test_divide_mixed():
    assert divide(-10, 5) == -2

def test_divide_float_precision():
    assert divide(1, 3) == pytest.approx(0.3333333)

def test_divide_zero_division():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

# Tests for negate function
def test_negate_positive():
    assert negate(5) == -5

def test_negate_negative():
    assert negate(-3) == 3

def test_negate_zero():
    assert negate(0) == 0

# Tests for percentage_conversion function
def test_percentage_conversion_positive():
    assert percentage_conversion(50) == pytest.approx(0.5)

def test_percentage_conversion_negative():
    assert percentage_conversion(-50) == pytest.approx(-0.5)

def test_percentage_conversion_zero():
    assert percentage_conversion(0) == 0

def test_percentage_conversion_float():
    assert percentage_conversion(12.5) == pytest.approx(0.125)

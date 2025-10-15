import pytest
from modules.arithmetic_operations import add, subtract, multiply, divide, negate, percentage_conversion

def test_add_positive():
    assert add(2.0, 3.0) == 5.0

def test_add_negative():
    assert add(-1.0, -2.0) == -3.0

def test_add_mixed():
    assert add(1.5, -2.5) == -1.0

def test_add_large_numbers():
    assert add(1e10, 1e10) == 2e10

def test_add_float_precision():
    assert add(0.1, 0.2) == pytest.approx(0.3)

def test_subtract_positive():
    assert subtract(5.0, 3.0) == 2.0

def test_subtract_negative_result():
    assert subtract(3.0, 5.0) == -2.0

def test_subtract_float_precision():
    assert subtract(0.3, 0.1) == pytest.approx(0.2)

def test_subtract_large_numbers():
    assert subtract(1e10, 1e9) == 9e9

def test_multiply_positive():
    assert multiply(2.0, 3.0) == 6.0

def test_multiply_negative():
    assert multiply(-2.0, 3.0) == -6.0

def test_multiply_large_numbers():
    assert multiply(1e10, 1e10) == 1e20

def test_multiply_float_precision():
    assert multiply(0.1, 0.2) == pytest.approx(0.02)

def test_divide_positive():
    assert divide(6.0, 3.0) == 2.0

def test_divide_negative():
    assert divide(-6.0, 3.0) == -2.0

def test_divide_float_precision():
    assert divide(1.0, 3.0) == pytest.approx(0.3333333333)

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(5.0, 0.0)

def test_negate_positive():
    assert negate(3.0) == -3.0

def test_negate_negative():
    assert negate(-3.0) == 3.0

def test_negate_zero():
    assert negate(0.0) == 0.0

def test_percentage_conversion():
    assert percentage_conversion(200.0) == 2.0

def test_percentage_conversion_float_precision():
    assert percentage_conversion(0.5) == pytest.approx(0.005)
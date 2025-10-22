import pytest
from modules.calculator import (
    add,
    subtract,
    multiply,
    divide,
    negate,
    percentage_conversion,
    square_root,
    to_binary
)

# Tests for add function
def test_add_positive_numbers():
    assert add(2.0, 3.0) == 5.0

def test_add_negative_numbers():
    assert add(-2.0, -3.0) == -5.0

def test_add_mixed_signs():
    assert add(-2.0, 3.0) == 1.0
    assert add(2.0, -3.0) == -1.0

def test_add_with_zero():
    assert add(0.0, 5.0) == 5.0
    assert add(5.0, 0.0) == 5.0

def test_add_float_precision():
    assert add(0.1, 0.2) == pytest.approx(0.3)

# Tests for subtract function
def test_subtract_positive_numbers():
    assert subtract(5.0, 3.0) == 2.0

def test_subtract_negative_numbers():
    assert subtract(-5.0, -3.0) == -2.0

def test_subtract_mixed_signs():
    assert subtract(-5.0, 3.0) == -8.0
    assert subtract(5.0, -3.0) == 8.0

def test_subtract_with_zero():
    assert subtract(0.0, 5.0) == -5.0
    assert subtract(5.0, 0.0) == 5.0

def test_subtract_float_precision():
    assert subtract(0.3, 0.1) == pytest.approx(0.2)

# Tests for multiply function
def test_multiply_positive_numbers():
    assert multiply(3.0, 4.0) == 12.0

def test_multiply_negative_numbers():
    assert multiply(-3.0, 4.0) == -12.0

def test_multiply_mixed_signs():
    assert multiply(-3.0, -4.0) == 12.0

def test_multiply_with_zero():
    assert multiply(5.0, 0.0) == 0.0
    assert multiply(0.0, 5.0) == 0.0

def test_multiply_float_precision():
    assert multiply(0.1, 0.2) == pytest.approx(0.02)

# Tests for divide function
def test_divide_normal():
    assert divide(10.0, 2.0) == 5.0

def test_divide_negative():
    assert divide(-10.0, 2.0) == -5.0

def test_divide_by_negative():
    assert divide(10.0, -2.0) == -5.0

def test_divide_floats():
    assert divide(7.5, 2.5) == 3.0

def test_divide_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError):
        divide(10.0, 0.0)

def test_divide_zero_by_number():
    assert divide(0.0, 5.0) == 0.0

def test_divide_float_precision():
    assert divide(1.0, 3.0) == pytest.approx(0.3333333333333333, rel=1e-6)

# Tests for negate function
def test_negate_positive():
    assert negate(5.0) == -5.0

def test_negate_negative():
    assert negate(-5.0) == 5.0

def test_negate_zero():
    assert negate(0.0) == 0.0

# Tests for percentage_conversion function
def test_percentage_conversion_normal():
    assert percentage_conversion(0.5) == 50.0

def test_percentage_conversion_zero():
    assert percentage_conversion(0.0) == 0.0

def test_percentage_conversion_negative():
    assert percentage_conversion(-0.5) == -50.0

def test_percentage_conversion_float_precision():
    assert percentage_conversion(0.333333) == pytest.approx(33.3333)

# Tests for square_root function
def test_square_root_positive():
    assert square_root(4.0) == 2.0

def test_square_root_zero():
    assert square_root(0.0) == 0.0

def test_square_root_negative_raises_error():
    with pytest.raises(ValueError):
        square_root(-4.0)

# Tests for to_binary function
def test_to_binary_positive():
    assert to_binary(5) == '0b101'

def test_to_binary_zero():
    assert to_binary(0) == '0b0'

def test_to_binary_negative():
    assert to_binary(-5) == '-0b101'

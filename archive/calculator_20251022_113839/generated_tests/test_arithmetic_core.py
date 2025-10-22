import pytest
from modules.arithmetic_core import add, subtract, multiply, divide, negate, percentage_conversion

# Tests for add function
def test_add_positive():
    assert add(1.2, 2.5) == pytest.approx(3.7)

def test_add_negative():
    assert add(-1.2, -2.5) == pytest.approx(-3.7)

def test_add_mixed_signs():
    assert add(1.2, -2.5) == pytest.approx(-1.3)

def test_add_zero():
    assert add(0, 5) == pytest.approx(5)

# Tests for subtract function
def test_subtract_positive():
    assert subtract(2, 5) == pytest.approx(-3)

def test_subtract_negative():
    assert subtract(-5, -2) == pytest.approx(-3)

def test_subtract_mixed_signs():
    assert subtract(5, -2) == pytest.approx(7)

def test_subtract_zero():
    assert subtract(0, 5) == pytest.approx(-5)

# Tests for multiply function
def test_multiply_positive():
    assert multiply(1.5, 2) == pytest.approx(3.0)

def test_multiply_negative():
    assert multiply(-1.5, -2) == pytest.approx(3.0)

def test_multiply_mixed_signs():
    assert multiply(1.5, -2) == pytest.approx(-3.0)

def test_multiply_large_numbers():
    assert multiply(1e10, 1e10) == pytest.approx(1e20)

# Tests for divide function
def test_divide_positive():
    assert divide(4, 2) == pytest.approx(2.0)

def test_divide_negative():
    assert divide(-4, -2) == pytest.approx(2.0)

def test_divide_mixed_signs():
    assert divide(4, -2) == pytest.approx(-2.0)

def test_divide_zero_division():
    with pytest.raises(ZeroDivisionError):
        divide(4, 0)

def test_divide_large_numbers():
    assert divide(1e10, 2) == pytest.approx(5e9)

# Tests for negate function
def test_negate_positive():
    assert negate(5) == pytest.approx(-5)

def test_negate_negative():
    assert negate(-3) == pytest.approx(3)

def test_negate_zero():
    assert negate(0) == pytest.approx(0)

# Tests for percentage_conversion function
def test_percentage_conversion_positive():
    assert percentage_conversion(25) == pytest.approx(0.25)

def test_percentage_conversion_negative():
    assert percentage_conversion(-25) == pytest.approx(-0.25)

def test_percentage_conversion_zero():
    assert percentage_conversion(0) == pytest.approx(0)

def test_percentage_conversion_large_number():
    assert percentage_conversion(1e6) == pytest.approx(1e4)

import pytest
from modules.arithmetic import add, subtract, multiply, divide

# Tests for the add function
def test_add_positive():
    assert add(1.5, 2.5) == pytest.approx(4.0)

def test_add_negative():
    assert add(-1.5, -2.5) == pytest.approx(-4.0)

def test_add_mixed():
    assert add(1.5, -2.5) == pytest.approx(-1.0)

def test_add_large_numbers():
    assert add(1e10, 1e10) == pytest.approx(2e10)

def test_add_small_numbers():
    assert add(1e-10, 1e-10) == pytest.approx(2e-10)

# Tests for the subtract function
def test_subtract_positive():
    assert subtract(5.0, 3.0) == pytest.approx(2.0)

def test_subtract_negative():
    assert subtract(-5.0, -3.0) == pytest.approx(-2.0)

def test_subtract_mixed():
    assert subtract(5.0, -3.0) == pytest.approx(8.0)

def test_subtract_large_numbers():
    assert subtract(1e10, 1e5) == pytest.approx(9999900000.0)

def test_subtract_small_numbers():
    assert subtract(1e-10, 1e-10) == pytest.approx(0.0)

# Tests for the multiply function
def test_multiply_positive():
    assert multiply(2.0, 3.0) == pytest.approx(6.0)

def test_multiply_negative():
    assert multiply(-2.0, -3.0) == pytest.approx(6.0)

def test_multiply_mixed():
    assert multiply(2.0, -3.0) == pytest.approx(-6.0)

def test_multiply_large_numbers():
    assert multiply(1e10, 1e5) == pytest.approx(1e15)

def test_multiply_small_numbers():
    assert multiply(1e-10, 1e-10) == pytest.approx(1e-20)

# Tests for the divide function
def test_divide_positive():
    assert divide(6.0, 2.0) == pytest.approx(3.0)

def test_divide_negative():
    assert divide(-6.0, -2.0) == pytest.approx(3.0)

def test_divide_mixed():
    assert divide(6.0, -2.0) == pytest.approx(-3.0)

def test_divide_large_numbers():
    assert divide(1e10, 1e5) == pytest.approx(1e5)

def test_divide_small_numbers():
    assert divide(1e-10, 1e-5) == pytest.approx(1e-5)

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(3.0, 0.0)

import pytest
from modules.ui import calculate_discount, format_price

def test_calculate_discount_normal():
    assert calculate_discount(100, 10) == 90

def test_calculate_discount_zero_discount():
    assert calculate_discount(100, 0) == 100

def test_calculate_discount_full_discount():
    assert calculate_discount(100, 100) == 0

def test_calculate_discount_over_discount():
    with pytest.raises(ValueError):
        calculate_discount(100, 110)

def test_calculate_discount_negative_price():
    with pytest.raises(ValueError):
        calculate_discount(-100, 10)

def test_format_price_normal():
    assert format_price(100) == "$100.00"

def test_format_price_float():
    assert format_price(99.99) == "$99.99"

def test_format_price_large_number():
    assert format_price(1000000) == "$1,000,000.00"

def test_format_price_negative():
    with pytest.raises(ValueError):
        format_price(-100)

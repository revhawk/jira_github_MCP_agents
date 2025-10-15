import pytest
from modules.memory_management import memory_clear, memory_add, memory_subtract, memory_recall

def test_memory_clear():
    memory_clear()
    assert memory_recall() == pytest.approx(0.0)

def test_memory_add_positive():
    memory_clear()
    memory_add(5.0)
    assert memory_recall() == pytest.approx(5.0)

def test_memory_add_zero():
    memory_clear()
    memory_add(0.0)
    assert memory_recall() == pytest.approx(0.0)

def test_memory_add_negative():
    memory_clear()
    memory_add(-3.0)
    assert memory_recall() == pytest.approx(-3.0)

def test_memory_subtract_positive():
    memory_clear()
    memory_add(10.0)
    memory_subtract(3.0)
    assert memory_recall() == pytest.approx(7.0)

def test_memory_subtract_zero():
    memory_clear()
    memory_add(5.0)
    memory_subtract(0.0)
    assert memory_recall() == pytest.approx(5.0)

def test_memory_subtract_negative():
    memory_clear()
    memory_add(5.0)
    memory_subtract(-2.0)
    assert memory_recall() == pytest.approx(7.0)

def test_memory_recall_empty():
    memory_clear()
    assert memory_recall() == pytest.approx(0.0)

def test_memory_recall_after_operations():
    memory_clear()
    memory_add(4.0)
    memory_subtract(1.0)
    assert memory_recall() == pytest.approx(3.0)
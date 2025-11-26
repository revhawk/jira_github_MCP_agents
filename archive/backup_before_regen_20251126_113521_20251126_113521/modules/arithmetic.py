"""Arithmetic module for basic math operations with zero-division handling."""

def add(a: float, b: float) -> float:
    """Perform addition ensuring float precision and handling mixed positive/negative inputs."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Perform subtraction ensuring correct handling of negative results and float precision."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Perform multiplication while accurately handling large numbers and float precision."""
    return a * b

def divide(a: float, b: float) -> float:
    """Perform division and raise ZeroDivisionError when denominator is zero, maintaining float precision."""
    if b == 0.0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b

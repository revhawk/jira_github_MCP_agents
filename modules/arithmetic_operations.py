"""Arithmetic operations module for basic math calculations."""

def add(a: float, b: float) -> float:
    """Add two numbers, ensuring float precision and handling mixed positive/negative inputs."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract b from a, handling negative results and float precision."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers, accurately handling large numbers and maintaining float precision."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divide a by b, raising a ZeroDivisionError when b is zero and maintaining high float precision otherwise."""
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b

def negate(n: float) -> float:
    """Flip the sign of the input number, ensuring positive becomes negative, negative becomes positive, and zero remains zero."""
    return -n

def percentage_conversion(n: float) -> float:
    """Convert the input number to its decimal percentage value (n/100)."""
    return n / 100.0
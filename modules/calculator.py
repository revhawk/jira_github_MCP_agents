"""Calculator module for basic math operations."""

def add(a: float, b: float) -> float:
    """Perform addition of two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Perform subtraction of b from a."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Perform multiplication of two numbers."""
    return a * b

def divide(a: float, b: float) -> float:
    """Perform division and raise ZeroDivisionError if b=0."""
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b

def negate(n: float) -> float:
    """Flip the sign of the input number."""
    return -n

def percentage_conversion(n: float) -> float:
    """Convert a number to its decimal percentage (n/100)."""
    return n / 100

"""arithmetic_core module for basic math operations."""

def add(a: float, b: float) -> float:
    """Perform addition with correct float precision and handle mixed signs."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Perform subtraction with correct float precision and handle negative results."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Perform multiplication, maintaining precision and handling large numbers."""
    return a * b

def divide(a: float, b: float) -> float:
    """Perform division, raising ZeroDivisionError if denominator is zero and maintaining float precision."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b

def negate(n: float) -> float:
    """Flip the sign of a number, ensuring zero remains zero."""
    return -n

def percentage_conversion(n: float) -> float:
    """Convert a number to its decimal percentage (n/100)."""
    return n / 100

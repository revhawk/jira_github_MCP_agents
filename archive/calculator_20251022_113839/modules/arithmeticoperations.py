def add(a: float, b: float) -> float:
    """Adds two numbers, ensuring float precision and handling mixed positive/negative inputs."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtracts the second number from the first, ensuring float precision and handling negative results."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiplies two numbers, ensuring accuracy with large numbers and maintaining float precision."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divides the first number by the second, raising a ZeroDivisionError if the denominator is zero, and maintaining high float precision."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b

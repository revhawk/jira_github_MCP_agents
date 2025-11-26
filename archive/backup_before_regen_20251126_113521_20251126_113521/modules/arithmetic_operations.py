def add(a: float, b: float) -> float:
    """Adds two numbers, ensuring float precision and handling mixed positive/negative inputs."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtracts the second number from the first, ensuring float precision and handling negative results."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiplies two numbers, accurately handling large numbers and maintaining float precision."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divides the first number by the second, raising a ZeroDivisionError if the denominator is zero, and maintaining high float precision."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def negate(n: float) -> float:
    """Flips the sign of the given number, ensuring positive becomes negative, negative becomes positive, and zero remains zero."""
    return -n

def percentage_conversion(n: float) -> float:
    """Converts a number to its decimal percentage value by dividing by 100."""
    return n / 100

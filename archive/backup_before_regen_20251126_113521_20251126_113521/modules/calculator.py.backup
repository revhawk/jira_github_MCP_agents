import math

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
    """Divides the first number by the second, raising a ZeroDivisionError if the denominator is zero and maintaining high float precision."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def square_root(a: float) -> float:
    """Returns the square root of a number. Raises ValueError for negative numbers."""
    if a < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(a)

def negate(n: float) -> float:
    """Negates the number, flipping its sign."""
    return -n

def percentage_conversion(n: float) -> float:
    """Converts a number to its percentage value."""
    return n * 100

def to_binary(n: int) -> str:
    """Converts a number to its binary representation."""
    if n < 0:
        return '-0b' + bin(n)[3:]  # Two's complement representation for negative numbers
    return '0b' + bin(n)[2:]

def convertToBinary(decimalNumber: int) -> str:
    """Converts a decimal number to its binary representation."""
    if not isinstance(decimalNumber, int):
        raise TypeError("Input must be an integer")
    if decimalNumber < 0:
        return '-' + bin(decimalNumber)[3:]  # Two's complement representation for negative numbers
    return bin(decimalNumber)[2:]  # Remove '0b' prefix

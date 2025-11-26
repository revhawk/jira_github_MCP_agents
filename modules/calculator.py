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

def addHexNumbers(hexNumber1: str, hexNumber2: str) -> str:
    """Adds two hexadecimal numbers and returns the result in hexadecimal format."""
    try:
        decimal1 = int(hexNumber1, 16)
        decimal2 = int(hexNumber2, 16)
    except ValueError:
        raise ValueError("Invalid hexadecimal input")
    result = decimal1 + decimal2
    return hex(result)

def convertToHex(decimalNumber: int) -> str:
    """Converts a decimal number to its hexadecimal representation."""
    if not isinstance(decimalNumber, int):
        raise TypeError("Input must be an integer")
    return hex(decimalNumber)

def convertToDecimalFromHex(hexNumber: str) -> int:
    """Converts a hexadecimal number to its decimal representation."""
    try:
        return int(hexNumber, 16)
    except ValueError:
        raise ValueError("Invalid hexadecimal input")

def convertFromHex(hexNumber: str, outputFormat: str) -> str:
    """Converts a hexadecimal number to decimal or binary format.
    
    Args:
        hexNumber: The hexadecimal number as a string.
        outputFormat: The desired output format, either 'decimal' or 'binary'.
    
    Returns:
        The converted number as a string in the specified format.
    
    Raises:
        ValueError: If the hexNumber is invalid or the outputFormat is not recognized.
    """
    try:
        decimal_value = int(hexNumber, 16)
    except ValueError:
        raise ValueError("Invalid hexadecimal input")
    
    if outputFormat == 'decimal':
        return str(decimal_value)
    elif outputFormat == 'binary':
        return bin(decimal_value)
    else:
        raise ValueError("Output format must be 'decimal' or 'binary'")

def calculate_square_root(number: float) -> float:
    """Calculates the square root of a given number.
    
    Args:
        number: The number to calculate the square root of.
    
    Returns:
        The square root of the number.
    
    Raises:
        ValueError: If the number is negative.
    """
    if number < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(number)

def add_hex_numbers(hex1: str, hex2: str) -> str:
    """Adds two hexadecimal numbers and returns the result in hexadecimal.
    
    Args:
        hex1: The first hexadecimal number as a string.
        hex2: The second hexadecimal number as a string.
    
    Returns:
        The sum of the two hexadecimal numbers as a hexadecimal string.
    
    Raises:
        ValueError: If either input is not a valid hexadecimal number.
    """
    try:
        decimal1 = int(hex1, 16)
        decimal2 = int(hex2, 16)
    except ValueError:
        raise ValueError("Invalid hexadecimal input")
    result = decimal1 + decimal2
    return hex(result)

def convert_to_hex(decimal_number: int) -> str:
    """Converts a decimal number to hexadecimal.
    
    Args:
        decimal_number: The decimal number to convert.
    
    Returns:
        The hexadecimal representation of the decimal number.
    
    Raises:
        TypeError: If the input is not an integer.
    """
    if not isinstance(decimal_number, int):
        raise TypeError("Input must be an integer")
    return hex(decimal_number)

def convert_to_binary(decimal_number: int) -> str:
    """Converts a decimal number to binary.
    
    Args:
        decimal_number: The decimal number to convert.
    
    Returns:
        The binary representation of the decimal number.
    
    Raises:
        TypeError: If the input is not an integer.
    """
    if not isinstance(decimal_number, int):
        raise TypeError("Input must be an integer")
    return bin(decimal_number)

def convert_to_decimal(number: str, base: int) -> int:
    """Converts a hexadecimal or binary number to decimal.
    
    Args:
        number: The number to convert as a string.
        base: The base of the number (16 for hexadecimal, 2 for binary).
    
    Returns:
        The decimal representation of the number.
    
    Raises:
        ValueError: If the number is not valid for the given base.
    """
    try:
        return int(number, base)
    except ValueError:
        raise ValueError("Invalid number for the specified base")
def divide(a: float, b: float) -> float:
    """Performs division of two numbers, raising a ZeroDivisionError if the denominator is zero.
    
    Args:
        a (float): The numerator of the division.
        b (float): The denominator of the division.
    
    Returns:
        float: The result of the division a / b.
    
    Raises:
        ZeroDivisionError: If b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def percentage_conversion(n: float) -> float:
    """Converts a number to its decimal percentage value.
    
    Args:
        n (float): The number to be converted to a percentage.
    
    Returns:
        float: The decimal percentage value of n (n/100).
    """
    return n / 100.0

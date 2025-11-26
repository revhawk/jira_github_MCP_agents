def divide(a: float, b: float) -> float:
    """Performs division of two numbers, raising a ZeroDivisionError if the denominator is zero.
    
    Args:
        a (float): The numerator of the division.
        b (float): The denominator of the division.
    
    Returns:
        float: The result of the division of a by b.
    
    Raises:
        ZeroDivisionError: If b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

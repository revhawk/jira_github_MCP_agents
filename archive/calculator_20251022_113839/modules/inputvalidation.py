def divide(a: float, b: float) -> float:
    """Performs division of two numbers, raising a ZeroDivisionError if the denominator is zero,
    while maintaining high float precision."""
    if b == 0:
        raise ZeroDivisionError("The denominator cannot be zero.")
    return a / b

"""UI module for handling price calculations and formatting."""

def calculate_discount(price: float, discount: float) -> float:
    """Calculate the discounted price.
    
    Args:
        price (float): The original price.
        discount (float): The discount percentage to apply.

    Returns:
        float: The price after applying the discount.

    Raises:
        ValueError: If the discount is greater than 100 or price is negative.
    """
    if price < 0:
        raise ValueError("Price cannot be negative.")
    if discount < 0 or discount > 100:
        raise ValueError("Discount must be between 0 and 100.")
    return price * (1 - discount / 100)

def format_price(price: float) -> str:
    """Format the price as a string with a dollar sign and two decimal places.
    
    Args:
        price (float): The price to format.

    Returns:
        str: The formatted price string.

    Raises:
        ValueError: If the price is negative.
    """
    if price < 0:
        raise ValueError("Price cannot be negative.")
    return "${:,.2f}".format(price)

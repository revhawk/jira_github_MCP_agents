"""Input processing module for handling user input and validation."""

current_display = "0"
decimal_added = False

def process_digit(d: int) -> str:
    """Accumulate consecutive digits and display correctly, handling leading zero suppression."""
    global current_display
    if current_display == "0":
        current_display = str(d)
    else:
        current_display += str(d)
    return current_display

def process_decimal() -> str:
    """Add a decimal point to the current number, ensuring it can only be added once."""
    global current_display, decimal_added
    if not decimal_added:
        current_display += '.'
        decimal_added = True
    return current_display

def process_negate() -> str:
    """Change the sign of the current number and update the display."""
    global current_display
    if current_display != "0":
        if current_display.startswith('-'):
            current_display = current_display[1:]
        else:
            current_display = '-' + current_display
    return current_display

def process_percent() -> str:
    """Apply the percentage function to the current display number."""
    global current_display
    if current_display != "0":
        current_display = str(float(current_display) / 100)
    return current_display
"""Memory management module for managing a persistent memory value."""

memory_value: float = 0.0

def memory_clear() -> None:
    """Reset the internal memory_value to 0.0."""
    global memory_value
    memory_value = 0.0

def memory_add(v: float) -> None:
    """Add the input value v to the persistent memory_value."""
    global memory_value
    memory_value += v

def memory_subtract(v: float) -> None:
    """Subtract the input value v from the persistent memory_value."""
    global memory_value
    memory_value -= v

def memory_recall() -> float:
    """Retrieve the stored memory_value."""
    return memory_value
"""Module to manage UI interactions and state transitions."""

class State:
    """Class to manage the state of the calculator."""
    def __init__(self):
        self.current_display = '0'
        self.running_total = 0
        self.pending_operator = None
        self.error_state = False

    def reset(self):
        """Reset the state to initial values."""
        self.current_display = '0'
        self.running_total = 0
        self.pending_operator = None
        self.error_state = False

# Initialize a global state instance
state = State()

def process_operator(op: str) -> None:
    """Handle operator button presses, replacing the pending operator or executing the current calculation."""
    global state
    if state.current_display != '0':
        state.pending_operator = op
    else:
        state.pending_operator = op  # Allow replacing operator even if no second number is entered

def process_equals() -> None:
    """Execute the current pending operation and save it for repeated execution."""
    global state
    if state.pending_operator and state.current_display != '0':
        if state.pending_operator == '+':
            state.running_total += float(state.current_display)
        elif state.pending_operator == '-':
            state.running_total -= float(state.current_display)
        elif state.pending_operator == '*':
            state.running_total *= float(state.current_display)
        elif state.pending_operator == '/':
            try:
                state.running_total /= float(state.current_display)
            except ZeroDivisionError as e:
                handle_error(e)
                return
        state.current_display = str(state.running_total)

def process_clear_entry() -> None:
    """Reset the current display to '0', preserving the running total and pending operation."""
    global state
    state.current_display = '0'

def process_all_clear() -> None:
    """Fully reset the state manager to its initial state, clearing all operands and operators."""
    global state
    state.reset()

def handle_error(error: Exception) -> None:
    """Transition to an ERROR state and display an error message when exceptions occur."""
    global state
    if isinstance(error, ZeroDivisionError):
        state.error_state = True

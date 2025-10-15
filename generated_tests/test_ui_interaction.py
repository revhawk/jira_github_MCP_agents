import pytest
from modules.ui_interaction import process_operator, process_equals, process_clear_entry, process_all_clear, handle_error

# Mock state for testing
class MockState:
    def __init__(self):
        self.current_display = '0'
        self.running_total = 0
        self.pending_operator = None
        self.error_state = False

    def reset(self):
        self.current_display = '0'
        self.running_total = 0
        self.pending_operator = None
        self.error_state = False

state = MockState()

def test_process_operator():
    global state
    state.current_display = '5'
    process_operator('+')
    assert state.pending_operator == '+'
    
    process_operator('-')
    assert state.pending_operator == '-'
    
    # Edge case: pressing an operator without a second number
    state.current_display = '0'
    process_operator('*')
    assert state.pending_operator == '*'

def test_process_equals():
    global state
    state.running_total = 10
    state.pending_operator = '+'
    state.current_display = '5'
    process_equals()
    assert state.running_total == 15
    
    # Edge case: consecutive equals presses
    process_equals()
    assert state.running_total == 20

def test_process_clear_entry():
    global state
    state.current_display = '5'
    process_clear_entry()
    assert state.current_display == '0'
    assert state.running_total == 0  # Ensure running total is preserved

def test_process_all_clear():
    global state
    state.current_display = '5'
    state.running_total = 10
    state.pending_operator = '+'
    state.error_state = True
    process_all_clear()
    assert state.current_display == '0'
    assert state.running_total == 0
    assert state.pending_operator is None
    assert not state.error_state

def test_handle_error():
    global state
    try:
        1 / 0  # This will raise a ZeroDivisionError
    except ZeroDivisionError as e:
        handle_error(e)
    assert state.error_state == True

    # Ensure that the error message is set appropriately (if applicable)
    # Assuming there's a method to get the error message
    # assert state.error_message == "Division by zero error"  # Example assertion if such a message exists

def test_handle_error_non_zero_division():
    global state
    try:
        1 / 1  # This should not raise an error
    except Exception as e:
        handle_error(e)
    assert state.error_state == False  # Ensure error state is not set on valid operation
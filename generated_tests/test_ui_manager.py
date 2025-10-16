import pytest
from modules.ui_manager import (
    handle_digit_input,
    handle_operator_input,
    handle_clear_entry,
    handle_all_clear,
    handle_equals
)

# Mocking the session state for testing purposes
class MockSessionState:
    def __init__(self):
        self.state = {}

    def __getitem__(self, key):
        return self.state.get(key, None)

    def __setitem__(self, key, value):
        self.state[key] = value

    def clear(self):
        self.state.clear()

@pytest.fixture
def mock_session_state():
    return MockSessionState()

def test_handle_digit_input_single_digit(mock_session_state):
    mock_session_state['display'] = ''
    handle_digit_input('5', mock_session_state)
    assert mock_session_state['display'] == '5'

def test_handle_digit_input_multiple_digits(mock_session_state):
    mock_session_state['display'] = '12'
    handle_digit_input('3', mock_session_state)
    assert mock_session_state['display'] == '123'

def test_handle_operator_input_addition(mock_session_state):
    mock_session_state['display'] = '5'
    mock_session_state['operator'] = None
    handle_operator_input('+', mock_session_state)
    assert mock_session_state['operator'] == '+'
    assert mock_session_state['display'] == '5'

def test_handle_operator_input_replacement(mock_session_state):
    mock_session_state['display'] = '5'
    mock_session_state['operator'] = '+'
    handle_operator_input('-', mock_session_state)
    assert mock_session_state['operator'] == '-'
    assert mock_session_state['display'] == '5'

def test_handle_clear_entry(mock_session_state):
    mock_session_state['display'] = '123'
    handle_clear_entry(mock_session_state)
    assert mock_session_state['display'] == ''

def test_handle_all_clear(mock_session_state):
    mock_session_state['display'] = '123'
    mock_session_state['operator'] = '+'
    handle_all_clear(mock_session_state)
    assert mock_session_state['display'] == ''
    assert mock_session_state['operator'] is None

def test_handle_equals_basic_addition(mock_session_state):
    mock_session_state['display'] = '5'
    mock_session_state['operator'] = '+'
    mock_session_state['operand'] = '3'
    handle_equals(mock_session_state)
    assert mock_session_state['display'] == '8'

def test_handle_equals_no_operation(mock_session_state):
    mock_session_state['display'] = '5'
    mock_session_state['operator'] = None
    handle_equals(mock_session_state)
    assert mock_session_state['display'] == '5'

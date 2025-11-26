import pytest
from modules.userinterface import (
    main_app_entry,
    render_display_component,
    setup_button_grid,
    bind_digit_and_decimal_buttons,
    bind_operator_buttons
)

class MockFSM:
    def __init__(self, current_display=""):
        self.current_display = current_display
        self.state = "initialized"

    def is_valid(self):
        return isinstance(self.current_display, str)

    def process_digit(self, digit):
        pass

    def process_operator(self, operator):
        pass

# Test main_app_entry
def test_main_app_entry_with_valid_fsm():
    fsm = MockFSM()
    main_app_entry(fsm)
    assert fsm.state == "initialized"

def test_main_app_entry_with_invalid_fsm():
    fsm = None
    with pytest.raises(AttributeError):
        main_app_entry(fsm)

# Test render_display_component
def test_render_display_component_with_valid_display():
    fsm = MockFSM(current_display="123")
    render_display_component(fsm)
    assert fsm.is_valid()

def test_render_display_component_with_invalid_display():
    fsm = MockFSM(current_display=None)
    with pytest.raises(TypeError):
        render_display_component(fsm)

# Test setup_button_grid
def test_setup_button_grid():
    # Since setup_button_grid does not return anything, we can only test that it runs without error
    setup_button_grid()

# Test bind_digit_and_decimal_buttons
def test_bind_digit_and_decimal_buttons_with_valid_fsm():
    fsm = MockFSM()
    bind_digit_and_decimal_buttons(fsm)
    assert fsm.state == "initialized"

def test_bind_digit_and_decimal_buttons_with_invalid_fsm():
    fsm = None
    with pytest.raises(AttributeError):
        bind_digit_and_decimal_buttons(fsm)

# Test bind_operator_buttons
def test_bind_operator_buttons_with_valid_fsm():
    fsm = MockFSM()
    bind_operator_buttons(fsm)
    assert fsm.state == "initialized"

def test_bind_operator_buttons_with_invalid_fsm():
    fsm = None
    with pytest.raises(AttributeError):
        bind_operator_buttons(fsm)

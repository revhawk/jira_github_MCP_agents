import pytest
from modules.app_setup import (
    initialize_app,
    render_layout,
    render_display,
    create_button_grid,
    bind_digit_buttons,
    bind_operator_buttons,
    bind_control_keys,
    bind_memory_keys,
    apply_custom_css
)

def test_initialize_app():
    # Test that the app initializes the CalculatorFSM once per session
    initialize_app()
    assert 'CalculatorFSM' in st.session_state

def test_initialize_app_edge_case():
    # Test session state not initialized
    st.session_state.clear()
    initialize_app()
    assert 'CalculatorFSM' in st.session_state

def test_render_layout():
    # Test that the layout is rendered correctly
    render_layout()
    assert st.session_state.layout_rendered is True

def test_render_display():
    # Test that the current display value is shown correctly
    st.session_state.current_display = "5"
    render_display()
    assert st.session_state.display_value == "5"

def test_create_button_grid():
    # Test that the button grid is created in a 4-column layout
    create_button_grid()
    assert st.session_state.button_grid_columns == 4

def test_bind_digit_buttons():
    # Test that digit buttons are bound correctly
    bind_digit_buttons()
    assert st.session_state.digit_buttons_bound is True

def test_bind_operator_buttons():
    # Test that operator buttons are bound correctly
    bind_operator_buttons()
    assert st.session_state.operator_buttons_bound is True

def test_bind_control_keys():
    # Test that control keys invoke the correct FSM methods
    bind_control_keys()
    assert st.session_state.control_keys_bound is True

def test_bind_memory_keys():
    # Test that memory keys invoke the correct FSM methods
    bind_memory_keys()
    assert st.session_state.memory_keys_bound is True

def test_apply_custom_css():
    # Test that custom CSS is applied correctly
    apply_custom_css()
    assert st.session_state.css_applied is True

def test_render_display_edge_case():
    # Test rendering errors in UI
    st.session_state.current_display = None
    with pytest.raises(ValueError):
        render_display()
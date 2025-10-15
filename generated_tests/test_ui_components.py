import pytest
from modules.ui_components import (
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
    # Normal case
    initialize_app()
    assert 'calculator_fsm' in st.session_state

    # Edge case: session state not initialized
    st.session_state.clear()
    initialize_app()
    assert 'calculator_fsm' in st.session_state

def test_render_layout():
    # Normal case
    try:
        render_layout()
    except Exception as e:
        pytest.fail(f"render_layout raised an exception: {e}")

def test_render_display():
    # Normal case
    st.session_state.calculator_fsm.current_display = "5"
    render_display()
    assert st.session_state.display_output == "5"

    # Edge case: error message
    st.session_state.calculator_fsm.current_display = "Error"
    render_display()
    assert st.session_state.display_output == "Error"

def test_create_button_grid():
    # Normal case
    create_button_grid()
    assert len(st.session_state.button_grid) == 4  # Assuming 4 columns

def test_bind_digit_buttons():
    # Normal case
    bind_digit_buttons()
    assert st.session_state.fsm.process_digit.called

    # Edge case: button click during calculation
    st.session_state.calculator_fsm.is_calculating = True
    bind_digit_buttons()
    assert not st.session_state.fsm.process_digit.called

def test_bind_operator_buttons():
    # Normal case
    bind_operator_buttons()
    assert st.session_state.fsm.process_operator.called

def test_bind_control_keys():
    # Normal case
    bind_control_keys()
    assert st.session_state.fsm.process_control.called

def test_bind_memory_keys():
    # Normal case
    bind_memory_keys()
    assert st.session_state.fsm.process_memory.called

def test_apply_custom_css():
    # Normal case
    apply_custom_css()
    assert st.session_state.css_applied is True

    # Edge case: CSS not loading correctly
    st.session_state.css_applied = False
    apply_custom_css()
    assert st.session_state.css_applied is True  # Should attempt to apply again
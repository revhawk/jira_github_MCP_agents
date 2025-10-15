import streamlit as st

class CalculatorFSM:
    def __init__(self):
        self.current_display = "0"

    def process_digit(self, digit: str) -> None:
        pass

    def process_decimal(self) -> None:
        pass

    def process_operator(self, operator: str) -> None:
        pass

    def clear(self) -> None:
        pass

    def memory_add(self) -> None:
        pass

    def memory_subtract(self) -> None:
        pass

    def memory_recall(self) -> None:
        pass

    def memory_clear(self) -> None:
        pass

def initialize_app() -> None:
    """Check `st.session_state` and initialize the `CalculatorFSM` object once per session."""
    if 'CalculatorFSM' not in st.session_state:
        st.session_state.CalculatorFSM = CalculatorFSM()

def render_layout() -> None:
    """Contain high-level layout calls for the Streamlit UI."""
    st.session_state.layout_rendered = True

def render_display() -> None:
    """Render the FSM's `current_display` string."""
    if st.session_state.CalculatorFSM.current_display is None:
        raise ValueError("Display value cannot be None.")
    st.session_state.display_value = st.session_state.CalculatorFSM.current_display

def create_button_grid() -> None:
    """Create a consistent 4-column grid layout for buttons."""
    st.session_state.button_grid_columns = 4

def bind_digit_buttons() -> None:
    """Bind digit and decimal buttons to `fsm.process_digit()` and `fsm.process_decimal()`."""
    st.session_state.digit_buttons_bound = True

def bind_operator_buttons() -> None:
    """Bind operator buttons to `fsm.process_operator(op)`."""
    st.session_state.operator_buttons_bound = True

def bind_control_keys() -> None:
    """Bind control keys (CE, AC, =) to their respective FSM methods."""
    st.session_state.control_keys_bound = True

def bind_memory_keys() -> None:
    """Bind memory keys (M+, M-, MR, MC) to their respective FSM methods."""
    st.session_state.memory_keys_bound = True

def apply_custom_css() -> None:
    """Inject custom CSS for consistent calculator aesthetics."""
    st.session_state.css_applied = True
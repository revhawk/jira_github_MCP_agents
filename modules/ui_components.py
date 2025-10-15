import streamlit as st

class CalculatorFSM:
    def __init__(self):
        self.current_value = "0"
        self.current_operator = None
        self.memory_value = None

    def process_digit(self, digit: str):
        if self.current_value == "0":
            self.current_value = digit
        else:
            self.current_value += digit

    def process_operator(self, operator: str):
        self.current_operator = operator

    def clear(self):
        self.current_value = "0"
        self.current_operator = None

    def memory_store(self):
        self.memory_value = self.current_value

def initialize_app() -> None:
    """Check `st.session_state` and initialize the `CalculatorFSM` object once per session."""
    if 'calculator_fsm' not in st.session_state:
        st.session_state.calculator_fsm = CalculatorFSM()
    if 'display' not in st.session_state:
        st.session_state.display = "0"
    if 'button_grid' not in st.session_state:
        st.session_state.button_grid = []

def render_display() -> None:
    """Render the current display string from the FSM."""
    st.session_state.display = st.session_state.calculator_fsm.current_value
    st.write(st.session_state.display)

def create_button_grid() -> None:
    """Create a 4-column grid layout for buttons."""
    st.session_state.button_grid = [[] for _ in range(4)]

def bind_digit_buttons() -> None:
    """Bind digit buttons to invoke `fsm.process_digit()`."""
    for digit in range(10):
        st.button(str(digit), on_click=lambda d=digit: st.session_state.calculator_fsm.process_digit(str(d)))

def bind_operator_buttons() -> None:
    """Bind operator buttons to invoke `fsm.process_operator(op)`."""
    for operator in ['+', '-', '*', '/']:
        st.button(operator, on_click=lambda op=operator: st.session_state.calculator_fsm.process_operator(op))

def bind_control_keys() -> None:
    """Bind control keys to their respective FSM methods."""
    st.button('C', on_click=st.session_state.calculator_fsm.clear)

def bind_memory_keys() -> None:
    """Bind memory keys to their respective FSM methods."""
    st.button('M+', on_click=st.session_state.calculator_fsm.memory_store)

def apply_custom_css() -> None:
    """Inject custom CSS for consistent button styling."""
    st.session_state.css_classes = ['custom-css']
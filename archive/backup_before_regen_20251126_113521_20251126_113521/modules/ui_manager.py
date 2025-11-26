"""UI Manager module for Streamlit calculator layout and logic."""

from typing import List
import streamlit as st

def initialize_calculator_state() -> None:
    """Check st.session_state and initialize the CalculatorFSM object once per session."""
    if 'display' not in st.session_state:
        st.session_state['display'] = ''
    if 'operator' not in st.session_state:
        st.session_state['operator'] = None
    if 'operand' not in st.session_state:
        st.session_state['operand'] = None

def render_main_app_layout() -> None:
    """Provide the primary Streamlit layout structure."""
    st.title("Calculator")
    render_display(st.session_state['display'])
    button_labels = ['7', '8', '9', '/',
                     '4', '5', '6', '*',
                     '1', '2', '3', '-',
                     '0', '.', '=', '+',
                     'C', 'AC']
    render_button_grid(button_labels)

def render_display(display_value: str) -> None:
    """Display the current calculator output text."""
    st.text_input("Display", value=display_value, key='display', disabled=True)

def render_button_grid(button_labels: List[str]) -> None:
    """Create a 4-column grid of calculator buttons."""
    cols = st.columns(4)
    for i, label in enumerate(button_labels):
        with cols[i % 4]:
            if st.button(label):
                if label.isdigit():
                    handle_digit_input(label)
                elif label == '.':
                    handle_decimal_input()
                elif label in '+-*/':
                    handle_operator_input(label)
                elif label == '=':
                    handle_equals()
                elif label == 'C':
                    handle_clear_entry()
                elif label == 'AC':
                    handle_all_clear()

def handle_digit_input(digit: str) -> None:
    """Process a digit click event."""
    st.session_state['display'] += digit

def handle_decimal_input() -> None:
    """Process a decimal point click event."""
    if '.' not in st.session_state['display']:
        st.session_state['display'] += '.'

def handle_operator_input(operator: str) -> None:
    """Process a core operator click event."""
    if st.session_state['operator'] is None:
        st.session_state['operand'] = st.session_state['display']
        st.session_state['display'] = ''
    st.session_state['operator'] = operator

def handle_clear_entry() -> None:
    """Process the Clear Entry (CE) action."""
    st.session_state['display'] = ''

def handle_all_clear() -> None:
    """Process the All Clear (AC) action."""
    st.session_state['display'] = ''
    st.session_state['operator'] = None
    st.session_state['operand'] = None

def handle_equals() -> None:
    """Process the equals operation."""
    if st.session_state['operator'] and st.session_state['operand'] is not None:
        operand1 = float(st.session_state['operand'])
        operand2 = float(st.session_state['display'])
        if st.session_state['operator'] == '+':
            result = operand1 + operand2
        elif st.session_state['operator'] == '-':
            result = operand1 - operand2
        elif st.session_state['operator'] == '*':
            result = operand1 * operand2
        elif st.session_state['operator'] == '/':
            result = operand1 / operand2 if operand2 != 0 else 'Error'
        st.session_state['display'] = str(result)
        st.session_state['operator'] = None
        st.session_state['operand'] = None

def apply_custom_css(css: str) -> None:
    """Inject custom CSS styling into the UI."""
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

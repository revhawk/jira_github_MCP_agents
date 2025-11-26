import streamlit as st

class CalculatorFSM:
    def __init__(self):
        self.display = ""
        self.current_value = 0
        self.operator = None
        self.reset_next = False

    def input_digit(self, digit: str):
        if self.reset_next:
            self.display = digit
            self.reset_next = False
        else:
            self.display += digit

    def input_decimal(self):
        if '.' not in self.display:
            self.display += '.'

    def process_operator(self, operator: str):
        if self.operator and not self.reset_next:
            self.calculate()
        self.current_value = float(self.display)
        self.operator = operator
        self.reset_next = True

    def calculate(self):
        if self.operator == '+':
            self.current_value += float(self.display)
        elif self.operator == '-':
            self.current_value -= float(self.display)
        elif self.operator == '*':
            self.current_value *= float(self.display)
        elif self.operator == '/':
            if float(self.display) != 0:
                self.current_value /= float(self.display)
            else:
                self.display = "Error"
                return
        self.display = str(self.current_value)
        self.operator = None

    def clear_entry(self):
        self.display = ""

    def all_clear(self):
        self.display = ""
        self.current_value = 0
        self.operator = None
        self.reset_next = False

def initialize_calculator_fsm() -> None:
    """Initializes the CalculatorFSM object in the Streamlit session state if it hasn't been initialized yet."""
    if 'calculator_fsm' not in st.session_state:
        st.session_state['calculator_fsm'] = CalculatorFSM()

def render_ui_layout() -> None:
    """Renders the high-level layout of the Streamlit application, ensuring business logic is decoupled."""
    st.title("Calculator")
    st.write("A simple calculator built with Streamlit.")

def render_display_component(fsm: CalculatorFSM) -> None:
    """Renders the display component to show the current display string from the FSM."""
    st.text_input("Display", value=fsm.display, disabled=True)

def create_button_grid() -> None:
    """Creates a 4-column grid layout for calculator buttons using Streamlit's column feature."""
    cols = st.columns(4)
    buttons = [
        ('7', '8', '9', '/'),
        ('4', '5', '6', '*'),
        ('1', '2', '3', '-'),
        ('0', '.', '=', '+')
    ]
    for row in buttons:
        for i, button in enumerate(row):
            with cols[i]:
                st.button(button)

def bind_digit_buttons(fsm: CalculatorFSM) -> None:
    """Binds digit and decimal buttons to their respective FSM methods using on_click."""
    for digit in '0123456789':
        st.button(digit, on_click=fsm.input_digit, args=(digit,))
    st.button('.', on_click=fsm.input_decimal)

def bind_operator_buttons(fsm: CalculatorFSM) -> None:
    """Binds operator buttons to the FSM's process_operator method using on_click with kwargs."""
    for operator in '+-*/':
        st.button(operator, on_click=fsm.process_operator, args=(operator,))

def bind_control_keys(fsm: CalculatorFSM) -> None:
    """Binds control keys (CE, AC, =) to their respective FSM methods using on_click."""
    st.button('CE', on_click=fsm.clear_entry)
    st.button('AC', on_click=fsm.all_clear)
    st.button('=', on_click=fsm.calculate)

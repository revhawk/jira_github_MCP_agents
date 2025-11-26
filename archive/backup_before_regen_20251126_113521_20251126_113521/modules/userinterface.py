def main_app_entry(fsm: 'FSM') -> None:
    """Sets up the main application layout using Streamlit, ensuring business logic is decoupled."""
    if fsm is None or not hasattr(fsm, 'state'):
        raise AttributeError("FSM is not properly initialized.")
    # Assuming Streamlit setup code here
    # st.title("Calculator")
    # st.write("Welcome to the calculator app.")
    fsm.state = "initialized"

def render_display_component(fsm: 'FSM') -> None:
    """Renders the current display string from the FSM to the Streamlit UI."""
    if fsm is None or not hasattr(fsm, 'current_display'):
        raise AttributeError("FSM is not properly initialized.")
    if not isinstance(fsm.current_display, str):
        raise TypeError("FSM's current_display must be a valid string.")
    # Assuming Streamlit display code here
    # st.text(fsm.current_display)

def setup_button_grid() -> None:
    """Creates a 4-column grid layout for calculator buttons using Streamlit."""
    # Assuming Streamlit grid setup code here
    # cols = st.columns(4)
    # for i, col in enumerate(cols):
    #     col.button(f"Button {i+1}")

def bind_digit_and_decimal_buttons(fsm: 'FSM') -> None:
    """Binds digit and decimal buttons to their respective FSM methods using on_click."""
    if fsm is None or not hasattr(fsm, 'process_digit'):
        raise AttributeError("FSM is not properly initialized.")
    # Assuming Streamlit button binding code here
    # for digit in range(10):
    #     st.button(str(digit), on_click=fsm.process_digit, args=(digit,))
    # st.button('.', on_click=fsm.process_digit, args=('.',))

def bind_operator_buttons(fsm: 'FSM') -> None:
    """Binds operator buttons to the FSM's process_operator method using on_click with kwargs."""
    if fsm is None or not hasattr(fsm, 'process_operator'):
        raise AttributeError("FSM is not properly initialized.")
    # Assuming Streamlit operator button binding code here
    # operators = ['+', '-', '*', '/']
    # for op in operators:
    #     st.button(op, on_click=fsm.process_operator, args=(op,))

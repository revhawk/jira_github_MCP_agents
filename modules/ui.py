def main_app_entry(fsm) -> None:
    """Sets up the main layout of the Streamlit app, ensuring business logic is decoupled."""
    try:
        # Assuming Streamlit is used for UI layout
        import streamlit as st
        st.title("Calculator App")
        render_display_component(fsm)
        create_button_grid()
    except Exception as e:
        st.error(f"An error occurred while setting up the app: {e}")

def render_display_component(fsm) -> None:
    """Renders the display component to show the FSM's current display string."""
    try:
        import streamlit as st
        display_string = fsm.get_display_string()
        st.text(display_string)
    except ValueError as e:
        st.error("Display string is not available.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def create_button_grid() -> None:
    """Creates a 4-column grid layout for buttons using Streamlit's column functionality."""
    import streamlit as st
    cols = st.columns(4)
    buttons = ['7', '8', '9', '/',
               '4', '5', '6', '*',
               '1', '2', '3', '-',
               '0', '.', '=', '+']
    for i, button in enumerate(buttons):
        with cols[i % 4]:
            st.button(button)

def bind_digit_buttons(fsm) -> None:
    """Binds digit and decimal buttons to their respective FSM methods."""
    import streamlit as st
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
    for digit in digits:
        if st.button(digit):
            try:
                fsm.process_digit(digit)
            except AttributeError as e:
                st.error(f"Digit processing method not available: {e}")

def bind_operator_buttons(fsm) -> None:
    """Binds operator buttons to the FSM's process_operator method with the correct operator symbol."""
    import streamlit as st
    operators = ['+', '-', '*', '/']
    for operator in operators:
        if st.button(operator):
            try:
                fsm.process_operator(operator)
            except AttributeError as e:
                st.error(f"Operator processing method not available: {e}")

def bind_control_keys(fsm) -> None:
    """Binds control keys (CE, AC, =) to their respective FSM methods."""
    import streamlit as st
    control_keys = ['CE', 'AC', '=']
    for key in control_keys:
        if st.button(key):
            try:
                fsm.process_control_key(key)
            except AttributeError as e:
                st.error(f"Control key processing method not available: {e}")

def inject_custom_css() -> None:
    """Injects custom CSS to style the Streamlit app with a calculator aesthetic."""
    import streamlit as st
    css = """
    <style>
    .stButton>button {
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
        margin: 5px;
        font-size: 18px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

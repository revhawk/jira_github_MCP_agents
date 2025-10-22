from typing import List
import streamlit as st

class FSM:
    def __init__(self, display_string=""):
        self.display_string = display_string

    def process_operator(self, operator):
        # Placeholder for processing logic
        pass

def main() -> None:
    """Sets up the main structure of the Streamlit app."""
    try:
        fsm = FSM()
        st.title("FSM App")
        render_display_component(fsm)
        create_button_grid(["Button1", "Button2", "Button3", "Button4"])
        bind_operator_buttons(fsm, ["+", "-", "*", "/"])
    except Exception as e:
        st.error(f"An error occurred during app setup: {e}")

def render_display_component(fsm) -> None:
    """Renders the display component to show the FSM's current display string."""
    try:
        if not hasattr(fsm, 'display_string'):
            raise AttributeError("FSM instance must have a 'display_string' attribute.")
        st.text(f"Current State: {fsm.display_string}")
    except Exception as e:
        st.error(f"An error occurred while rendering the display component: {e}")

def create_button_grid(buttons: List[str]) -> None:
    """Creates a 4-column grid layout for buttons using Streamlit's st.columns."""
    if len(buttons) == 0:
        raise ValueError("Button list cannot be empty.")
    if len(buttons) % 4 != 0:
        raise ValueError("Number of buttons must be a multiple of 4.")
    
    try:
        cols = st.columns(4)
        for i, button in enumerate(buttons):
            with cols[i % 4]:
                st.button(button)
    except Exception as e:
        st.error(f"An error occurred while creating the button grid: {e}")

def bind_operator_buttons(fsm, operators: List[str]) -> None:
    """Binds operator buttons to the FSM's process_operator method using on_click with kwargs."""
    if not hasattr(fsm, 'process_operator'):
        raise AttributeError("FSM instance must have a 'process_operator' method.")
    if len(operators) == 0:
        raise ValueError("Operator list cannot be empty.")
    
    try:
        for operator in operators:
            st.button(operator, on_click=fsm.process_operator, kwargs={'operator': operator})
    except Exception as e:
        st.error(f"An error occurred while binding operator buttons: {e}")

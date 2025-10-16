import streamlit as st

def initialize_session_state() -> None:
    """Check st.session_state for calculator setup and initialize once per session."""
    if 'calculator_initialized' not in st.session_state:
        st.session_state['calculator_initialized'] = True

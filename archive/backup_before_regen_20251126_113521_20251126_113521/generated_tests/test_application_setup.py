import pytest
from modules.application_setup import initialize_session_state
import streamlit as st

@pytest.fixture(autouse=True)
def setup_session_state():
    # Ensure that the session state is reset before each test
    st.session_state.clear()

def test_initialize_session_state_empty():
    # Test when session state is initially empty
    assert 'calculator_initialized' not in st.session_state
    initialize_session_state()
    assert st.session_state.get('calculator_initialized') is True

def test_initialize_session_state_already_initialized():
    # Test when session state is already initialized
    st.session_state['calculator_initialized'] = True
    initialize_session_state()
    assert st.session_state.get('calculator_initialized') is True

def test_initialize_session_state_persists():
    # Test that state persists across multiple calls
    initialize_session_state()
    assert st.session_state.get('calculator_initialized') is True
    initialize_session_state()  # Call again to ensure persistence
    assert st.session_state.get('calculator_initialized') is True

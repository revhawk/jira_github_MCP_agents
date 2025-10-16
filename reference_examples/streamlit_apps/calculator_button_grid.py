"""
REFERENCE EXAMPLE: Calculator with Button Grid Layout
Pattern: button_grid
Use Case: Calculator, keypad, number entry apps
Key Features:
- st.rerun() after every button click for immediate updates
- st.markdown() for display (not disabled text_input)
- use_container_width=True for better button layout
- Session state for maintaining calculator display
"""
import streamlit as st
from modules.arithmetic_core import negate, percentage_conversion

st.set_page_config(page_title="Calculator", layout="centered")

if 'display' not in st.session_state:
    st.session_state.display = '0'

st.title('🔢 Simple Calculator')
st.markdown(f"### Display: `{st.session_state.display}`")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button('7', key='7', use_container_width=True):
        st.session_state.display = '7' if st.session_state.display == '0' else st.session_state.display + '7'
        st.rerun()
    if st.button('4', key='4', use_container_width=True):
        st.session_state.display = '4' if st.session_state.display == '0' else st.session_state.display + '4'
        st.rerun()

with col4:
    if st.button('➕', key='+', use_container_width=True):
        st.session_state.display += '+'
        st.rerun()
    if st.button('=', key='=', use_container_width=True):
        try:
            st.session_state.display = str(eval(st.session_state.display))
        except:
            st.session_state.display = 'Error'
        st.rerun()

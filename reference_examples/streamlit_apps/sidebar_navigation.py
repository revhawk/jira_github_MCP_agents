"""
REFERENCE EXAMPLE: Sidebar Navigation
Pattern: sidebar_nav
Use Case: Multi-function apps, tool collections
Key Features:
- st.sidebar.selectbox for navigation
- Separate page logic with if/elif
- Unique keys for widgets on each page
"""
import streamlit as st
from modules.calculator import add, subtract, multiply

st.title('Multi-Function App')

page = st.sidebar.selectbox('Choose function', ['Add', 'Subtract', 'Multiply'])

if page == 'Add':
    st.header('Addition')
    a = st.number_input('First number', value=0.0, key='add_a')
    b = st.number_input('Second number', value=0.0, key='add_b')
    if st.button('Calculate', key='add_btn'):
        result = add(a, b)
        st.success(f'Result: {result}')

elif page == 'Subtract':
    st.header('Subtraction')
    a = st.number_input('First number', value=0.0, key='sub_a')
    b = st.number_input('Second number', value=0.0, key='sub_b')
    if st.button('Calculate', key='sub_btn'):
        result = subtract(a, b)
        st.success(f'Result: {result}')

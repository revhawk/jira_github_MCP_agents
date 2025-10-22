"""
PATTERN: Calculator with Memory Functions
USE CASE: Button grid calculator with persistent memory (M+, MR, MC)

KEY FEATURES:
- Button grid layout (4 columns)
- Session state for display and memory
- Memory functions: M+ (add to memory), MR (recall), MC (clear)
- MR appends to display (doesn't replace) unless display is '0'
- Proper digit handling (replace '0' on first digit)
- Operator buttons use emoji labels with symbol keys
- st.rerun() after every state change

MEMORY BEHAVIOR:
- M+: Evaluates current display, adds to memory, clears display to '0'
- MR: Recalls memory value, appends to display (or replaces if display='0')
- MC: Clears memory to 0
- Memory value shown below buttons

BUTTON PATTERN:
- Every button has unique key parameter
- Digit buttons: if display=='0' replace, else append
- Operator buttons: append symbol (not emoji) to display
- Equals button: eval() with error handling
- Clear button: reset display to '0'
"""

import streamlit as st
from modules.arithmeticoperations import add, subtract, multiply, divide
from modules.userinterface import main_app_entry, render_display_component, setup_button_grid, bind_digit_and_decimal_buttons, bind_operator_buttons
from modules.inputvalidation import divide, percentage_conversion

# Initialize session state
if 'display' not in st.session_state:
    st.session_state.display = '0'
if 'memory' not in st.session_state:
    st.session_state.memory = 0

# Title
st.title('Simple Streamlit Calculator')

# Display
st.markdown(f'### Display: `{st.session_state.display}`')

# Button Grid Layout
col1, col2, col3, col4 = st.columns(4)

# First Row
with col1:
    if st.button('7', key='7', use_container_width=True):
        if st.session_state.display == '0':
            st.session_state.display = '7'
        else:
            st.session_state.display += '7'
        st.rerun()

with col2:
    if st.button('8', key='8', use_container_width=True):
        if st.session_state.display == '0':
            st.session_state.display = '8'
        else:
            st.session_state.display += '8'
        st.rerun()

with col3:
    if st.button('9', key='9', use_container_width=True):
        if st.session_state.display == '0':
            st.session_state.display = '9'
        else:
            st.session_state.display += '9'
        st.rerun()

with col4:
    if st.button('➕', key='+', use_container_width=True):
        st.session_state.display += '+'
        st.rerun()

# Second Row
with col1:
    if st.button('4', key='4', use_container_width=True):
        if st.session_state.display == '0':
            st.session_state.display = '4'
        else:
            st.session_state.display += '4'
        st.rerun()

with col2:
    if st.button('5', key='5', use_container_width=True):
        if st.session_state.display == '0':
            st.session_state.display = '5'
        else:
            st.session_state.display += '5'
        st.rerun()

with col3:
    if st.button('6', key='6', use_container_width=True):
        if st.session_state.display == '0':
            st.session_state.display = '6'
        else:
            st.session_state.display += '6'
        st.rerun()

with col4:
    if st.button('➖', key='-', use_container_width=True):
        st.session_state.display += '-'
        st.rerun()

# Third Row
with col1:
    if st.button('1', key='1', use_container_width=True):
        if st.session_state.display == '0':
            st.session_state.display = '1'
        else:
            st.session_state.display += '1'
        st.rerun()

with col2:
    if st.button('2', key='2', use_container_width=True):
        if st.session_state.display == '0':
            st.session_state.display = '2'
        else:
            st.session_state.display += '2'
        st.rerun()

with col3:
    if st.button('3', key='3', use_container_width=True):
        if st.session_state.display == '0':
            st.session_state.display = '3'
        else:
            st.session_state.display += '3'
        st.rerun()

with col4:
    if st.button('✖️', key='*', use_container_width=True):
        st.session_state.display += '*'
        st.rerun()

# Fourth Row
with col1:
    if st.button('0', key='0', use_container_width=True):
        if st.session_state.display != '0':
            st.session_state.display += '0'
        st.rerun()

with col2:
    if st.button('.', key='.', use_container_width=True):
        if '.' not in st.session_state.display.split()[-1]:
            st.session_state.display += '.'
        st.rerun()

with col3:
    if st.button('=', key='=', use_container_width=True):
        try:
            # Evaluate the expression using eval
            st.session_state.display = str(eval(st.session_state.display))
        except ZeroDivisionError:
            st.session_state.display = 'Error'
        except Exception:
            st.session_state.display = 'Error'
        st.rerun()

with col4:
    if st.button('➗', key='/', use_container_width=True):
        st.session_state.display += '/'
        st.rerun()

# Clear Button
if st.button('Clear', key='C', use_container_width=True):
    st.session_state.display = '0'
    st.rerun()

# Memory Buttons Row
st.markdown('---')
mem_col1, mem_col2, mem_col3, mem_col4 = st.columns(4)

with mem_col1:
    if st.button('M+', key='M+', use_container_width=True):
        try:
            st.session_state.memory += float(eval(st.session_state.display))
            st.session_state.display = '0'
        except:
            pass
        st.rerun()

with mem_col2:
    if st.button('MR', key='MR', use_container_width=True):
        mem_value = str(st.session_state.memory)
        if st.session_state.display == '0':
            st.session_state.display = mem_value
        else:
            st.session_state.display += mem_value
        st.rerun()

with mem_col3:
    if st.button('MC', key='MC', use_container_width=True):
        st.session_state.memory = 0
        st.rerun()

with mem_col4:
    st.markdown(f'**Memory:** `{st.session_state.memory}`')

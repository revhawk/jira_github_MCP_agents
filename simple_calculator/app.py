import streamlit as st
from modules.arithmetic_core import negate, percentage_conversion

st.set_page_config(page_title="Calculator", layout="centered")

# Initialize
if 'display' not in st.session_state:
    st.session_state.display = '0'

st.title('🔢 Simple Calculator')

# Display (shows current state)
st.markdown(f"### Display: `{st.session_state.display}`")

# Button grid
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button('7', key='7', use_container_width=True):
        st.session_state.display = '7' if st.session_state.display == '0' else st.session_state.display + '7'
        st.rerun()
    if st.button('4', key='4', use_container_width=True):
        st.session_state.display = '4' if st.session_state.display == '0' else st.session_state.display + '4'
        st.rerun()
    if st.button('1', key='1', use_container_width=True):
        st.session_state.display = '1' if st.session_state.display == '0' else st.session_state.display + '1'
        st.rerun()
    if st.button('0', key='0', use_container_width=True):
        if st.session_state.display != '0':
            st.session_state.display += '0'
        st.rerun()

with col2:
    if st.button('8', key='8', use_container_width=True):
        st.session_state.display = '8' if st.session_state.display == '0' else st.session_state.display + '8'
        st.rerun()
    if st.button('5', key='5', use_container_width=True):
        st.session_state.display = '5' if st.session_state.display == '0' else st.session_state.display + '5'
        st.rerun()
    if st.button('2', key='2', use_container_width=True):
        st.session_state.display = '2' if st.session_state.display == '0' else st.session_state.display + '2'
        st.rerun()
    if st.button('.', key='.', use_container_width=True):
        if '.' not in st.session_state.display:
            st.session_state.display += '.'
            st.rerun()

with col3:
    if st.button('9', key='9', use_container_width=True):
        st.session_state.display = '9' if st.session_state.display == '0' else st.session_state.display + '9'
        st.rerun()
    if st.button('6', key='6', use_container_width=True):
        st.session_state.display = '6' if st.session_state.display == '0' else st.session_state.display + '6'
        st.rerun()
    if st.button('3', key='3', use_container_width=True):
        st.session_state.display = '3' if st.session_state.display == '0' else st.session_state.display + '3'
        st.rerun()
    if st.button('=', key='=', use_container_width=True):
        try:
            st.session_state.display = str(eval(st.session_state.display))
        except:
            st.session_state.display = 'Error'
        st.rerun()

with col4:
    if st.button('➕', key='+', use_container_width=True):
        st.session_state.display += '+'
        st.rerun()
    if st.button('➖', key='-', use_container_width=True):
        st.session_state.display += '-'
        st.rerun()
    if st.button('✖️', key='*', use_container_width=True):
        st.session_state.display += '*'
        st.rerun()
    if st.button('➗', key='/', use_container_width=True):
        st.session_state.display += '/'
        st.rerun()

# Additional operations
st.divider()
col_c, col_neg, col_pct = st.columns(3)
with col_c:
    if st.button('Clear', key='C', use_container_width=True):
        st.session_state.display = '0'
        st.rerun()
with col_neg:
    if st.button('± Negate', key='neg', use_container_width=True):
        try:
            st.session_state.display = str(negate(float(st.session_state.display)))
        except:
            st.session_state.display = 'Error'
        st.rerun()
with col_pct:
    if st.button('% Percent', key='pct', use_container_width=True):
        try:
            st.session_state.display = str(percentage_conversion(float(st.session_state.display)))
        except:
            st.session_state.display = 'Error'
        st.rerun()

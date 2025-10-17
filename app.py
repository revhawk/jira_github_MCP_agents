import streamlit as st
from modules.arithmetic import add, subtract, multiply, divide

def main():
    st.set_page_config(page_title="Simple Calculator", layout="centered")

    if 'display' not in st.session_state:
        st.session_state.display = '0'

    st.title('🔢 Simple Calculator')
    st.markdown(f"### Display: `{st.session_state.display}`")

    col1, col2, col3, col4 = st.columns(4)

    def update_display(value):
        if st.session_state.display == '0':
            st.session_state.display = value
        else:
            st.session_state.display += value
        st.rerun()

    def clear_display():
        st.session_state.display = '0'
        st.rerun()

    with col1:
        for num in ['7', '4', '1', '0']:
            if st.button(num, key=num, use_container_width=True):
                update_display(num)

    with col2:
        for num in ['8', '5', '2', '']:
            if num:
                if st.button(num, key=num, use_container_width=True):
                    update_display(num)

    with col3:
        for num in ['9', '6', '3', '']:
            if num:
                if st.button(num, key=num, use_container_width=True):
                    update_display(num)

    with col4:
        if st.button('➕', key='+', use_container_width=True):
            update_display('+')
        if st.button('➖', key='-', use_container_width=True):
            update_display('-')
        if st.button('✖️', key='*', use_container_width=True):
            update_display('*')
        if st.button('➗', key='/', use_container_width=True):
            update_display('/')
        if st.button('C', key='clear', use_container_width=True):
            clear_display()
        if st.button('=', key='=', use_container_width=True):
            try:
                result = eval(st.session_state.display.replace('✖️', '*').replace('➗', '/'))
                st.session_state.display = str(result)
            except ZeroDivisionError:
                st.session_state.display = 'Error'
            except Exception:
                st.session_state.display = 'Error'
            st.rerun()

if __name__ == "__main__":
    main()

import streamlit as st
from modules.calculator import (
    add, subtract, multiply, divide, square_root, negate, percentage_conversion,
    to_binary, convertToBinary, addHexNumbers, convertToHex, convertToDecimalFromHex,
    convertFromHex, calculate_square_root, add_hex_numbers, convert_to_hex,
    convert_to_binary, convert_to_decimal
)

# Initialize session state
if 'display' not in st.session_state:
    st.session_state.display = '0'
if 'memory' not in st.session_state:
    st.session_state.memory = 0
if 'mode' not in st.session_state:
    st.session_state.mode = 'DEC'  # DEC, BIN, or HEX

# Title
st.title('Advanced Streamlit Calculator')

# Mode toggle
mode_col1, mode_col2, mode_col3 = st.columns(3)
with mode_col1:
    if st.button('DEC', key='mode_dec', use_container_width=True, type='primary' if st.session_state.mode == 'DEC' else 'secondary'):
        old_mode = st.session_state.mode
        st.session_state.mode = 'DEC'
        if st.session_state.display != '0' and st.session_state.display != 'Error':
            try:
                if old_mode == 'BIN':
                    st.session_state.display = str(int(st.session_state.display, 2))
                elif old_mode == 'HEX':
                    st.session_state.display = str(int(st.session_state.display, 16))
            except:
                pass
        st.rerun()

with mode_col2:
    if st.button('BIN', key='mode_bin', use_container_width=True, type='primary' if st.session_state.mode == 'BIN' else 'secondary'):
        old_mode = st.session_state.mode
        st.session_state.mode = 'BIN'
        if st.session_state.display != '0' and st.session_state.display != 'Error':
            try:
                if old_mode == 'DEC':
                    st.session_state.display = bin(int(eval(st.session_state.display)))[2:]
                elif old_mode == 'HEX':
                    st.session_state.display = bin(int(st.session_state.display, 16))[2:]
            except:
                pass
        st.rerun()

with mode_col3:
    if st.button('HEX', key='mode_hex', use_container_width=True, type='primary' if st.session_state.mode == 'HEX' else 'secondary'):
        old_mode = st.session_state.mode
        st.session_state.mode = 'HEX'
        if st.session_state.display != '0' and st.session_state.display != 'Error':
            try:
                if old_mode == 'DEC':
                    st.session_state.display = hex(int(eval(st.session_state.display)))[2:].upper()
                elif old_mode == 'BIN':
                    st.session_state.display = hex(int(st.session_state.display, 2))[2:].upper()
            except:
                pass
        st.rerun()

# Display
st.markdown(f'### Display: `{st.session_state.display}` ({st.session_state.mode})')

# Create button grid layout
col1, col2, col3, col4 = st.columns(4)

# First row of buttons
with col1:
    if st.button('7', key='7', use_container_width=True, disabled=(st.session_state.mode == 'BIN')):
        if st.session_state.display == '0':
            st.session_state.display = '7'
        else:
            st.session_state.display += '7'
        st.rerun()

with col2:
    if st.button('8', key='8', use_container_width=True, disabled=(st.session_state.mode == 'BIN')):
        if st.session_state.display == '0':
            st.session_state.display = '8'
        else:
            st.session_state.display += '8'
        st.rerun()

with col3:
    if st.button('9', key='9', use_container_width=True, disabled=(st.session_state.mode == 'BIN')):
        if st.session_state.display == '0':
            st.session_state.display = '9'
        else:
            st.session_state.display += '9'
        st.rerun()

with col4:
    if st.button('➕', key='+', use_container_width=True):
        st.session_state.display += '+'
        st.rerun()

# Second row of buttons
with col1:
    if st.button('4', key='4', use_container_width=True, disabled=(st.session_state.mode == 'BIN')):
        if st.session_state.display == '0':
            st.session_state.display = '4'
        else:
            st.session_state.display += '4'
        st.rerun()

with col2:
    if st.button('5', key='5', use_container_width=True, disabled=(st.session_state.mode == 'BIN')):
        if st.session_state.display == '0':
            st.session_state.display = '5'
        else:
            st.session_state.display += '5'
        st.rerun()

with col3:
    if st.button('6', key='6', use_container_width=True, disabled=(st.session_state.mode == 'BIN')):
        if st.session_state.display == '0':
            st.session_state.display = '6'
        else:
            st.session_state.display += '6'
        st.rerun()

with col4:
    if st.button('➖', key='-', use_container_width=True):
        st.session_state.display += '-'
        st.rerun()

# Third row of buttons
with col1:
    if st.button('1', key='1', use_container_width=True):
        if st.session_state.display == '0':
            st.session_state.display = '1'
        else:
            st.session_state.display += '1'
        st.rerun()

with col2:
    if st.button('2', key='2', use_container_width=True, disabled=(st.session_state.mode == 'BIN')):
        if st.session_state.display == '0':
            st.session_state.display = '2'
        else:
            st.session_state.display += '2'
        st.rerun()

with col3:
    if st.button('3', key='3', use_container_width=True, disabled=(st.session_state.mode == 'BIN')):
        if st.session_state.display == '0':
            st.session_state.display = '3'
        else:
            st.session_state.display += '3'
        st.rerun()

with col4:
    if st.button('✖️', key='*', use_container_width=True):
        st.session_state.display += '*'
        st.rerun()

# Fourth row of buttons
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
            if st.session_state.mode == 'BIN':
                expr = st.session_state.display
                import re
                def bin_to_dec(match):
                    return str(int(match.group(0), 2))
                expr_dec = re.sub(r'[01]+', bin_to_dec, expr)
                result = eval(expr_dec)
                st.session_state.display = bin(int(result))[2:]
            elif st.session_state.mode == 'HEX':
                expr = st.session_state.display
                import re
                # Split by operators while keeping them
                parts = re.split(r'([+\-*/])', expr)
                # Convert hex numbers to decimal
                converted = []
                for part in parts:
                    if part in ['+', '-', '*', '/']:
                        converted.append(part)
                    elif part.strip():
                        try:
                            converted.append(str(int(part, 16)))
                        except:
                            converted.append(part)
                expr_dec = ''.join(converted)
                result = eval(expr_dec)
                st.session_state.display = hex(int(result))[2:].upper()
            else:
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

# Fifth row - Clear, Square Root, Binary
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button('Clear', key='C', use_container_width=True):
        st.session_state.display = '0'
        st.rerun()

with col2:
    if st.button('√', key='sqrt', use_container_width=True):
        try:
            if st.session_state.mode == 'BIN':
                dec_val = int(st.session_state.display, 2)
                result = square_root(float(dec_val))
                # For binary, convert back to decimal to show decimal result
                st.session_state.mode = 'DEC'
                st.session_state.display = str(result)
            elif st.session_state.mode == 'HEX':
                dec_val = int(st.session_state.display, 16)
                result = square_root(float(dec_val))
                # For hex, convert back to decimal to show decimal result
                st.session_state.mode = 'DEC'
                st.session_state.display = str(result)
            else:
                result = square_root(float(eval(st.session_state.display)))
                st.session_state.display = str(result)
        except ValueError:
            st.session_state.display = 'Error'
        except Exception:
            st.session_state.display = 'Error'
        st.rerun()

with col3:
    if st.button('±', key='negate', use_container_width=True):
        try:
            if st.session_state.mode == 'BIN':
                dec_val = int(st.session_state.display, 2)
                result = negate(float(dec_val))
                st.session_state.display = bin(int(result))[2:]
            elif st.session_state.mode == 'HEX':
                dec_val = int(st.session_state.display, 16)
                result = negate(float(dec_val))
                st.session_state.display = hex(int(result))[2:].upper()
            else:
                result = negate(float(eval(st.session_state.display)))
                st.session_state.display = str(result)
        except Exception:
            st.session_state.display = 'Error'
        st.rerun()

with col4:
    if st.button('%', key='percent', use_container_width=True):
        try:
            result = percentage_conversion(float(eval(st.session_state.display)))
            st.session_state.display = str(result)
        except Exception:
            st.session_state.display = 'Error'
        st.rerun()

# Hex digits row (A-F) - only visible in HEX mode
if st.session_state.mode == 'HEX':
    st.markdown('---')
    hex_col1, hex_col2, hex_col3, hex_col4, hex_col5, hex_col6 = st.columns(6)
    
    with hex_col1:
        if st.button('A', key='A', use_container_width=True):
            if st.session_state.display == '0':
                st.session_state.display = 'A'
            else:
                st.session_state.display += 'A'
            st.rerun()
    
    with hex_col2:
        if st.button('B', key='B', use_container_width=True):
            if st.session_state.display == '0':
                st.session_state.display = 'B'
            else:
                st.session_state.display += 'B'
            st.rerun()
    
    with hex_col3:
        if st.button('C', key='C_hex', use_container_width=True):
            if st.session_state.display == '0':
                st.session_state.display = 'C'
            else:
                st.session_state.display += 'C'
            st.rerun()
    
    with hex_col4:
        if st.button('D', key='D', use_container_width=True):
            if st.session_state.display == '0':
                st.session_state.display = 'D'
            else:
                st.session_state.display += 'D'
            st.rerun()
    
    with hex_col5:
        if st.button('E', key='E', use_container_width=True):
            if st.session_state.display == '0':
                st.session_state.display = 'E'
            else:
                st.session_state.display += 'E'
            st.rerun()
    
    with hex_col6:
        if st.button('F', key='F', use_container_width=True):
            if st.session_state.display == '0':
                st.session_state.display = 'F'
            else:
                st.session_state.display += 'F'
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

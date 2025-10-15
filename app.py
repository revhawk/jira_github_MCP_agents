import streamlit as st
from modules.arithmetic_operations import add, subtract, multiply, divide, negate, percentage_conversion
from modules.input_processing import process_digit, process_decimal, process_negate, process_percent
from modules.ui_interaction import process_operator, process_equals, process_clear_entry, process_all_clear, handle_error
from modules.memory_management import memory_clear, memory_add, memory_subtract, memory_recall
from modules.app_setup import initialize_app, render_layout, render_display, create_button_grid, bind_digit_buttons, bind_operator_buttons, bind_control_keys, bind_memory_keys, apply_custom_css

def main():
    st.title('Simple Calculator')
    
    # Initialize the app
    initialize_app()
    
    # Sidebar for navigation
    page = st.sidebar.selectbox('Choose function', ['Arithmetic Operations', 'Memory Management'])
    
    if page == 'Arithmetic Operations':
        st.header('Arithmetic Operations')
        
        operation = st.selectbox('Select Operation', ['Add', 'Subtract', 'Multiply', 'Divide', 'Negate', 'Percentage Conversion'])
        
        if operation in ['Add', 'Subtract', 'Multiply', 'Divide']:
            a = st.number_input('First number', value=0.0, key='num_a')
            b = st.number_input('Second number', value=0.0, key='num_b')
            
            if st.button('Calculate', key='calc_btn'):
                if operation == 'Add':
                    result = add(a, b)
                elif operation == 'Subtract':
                    result = subtract(a, b)
                elif operation == 'Multiply':
                    result = multiply(a, b)
                elif operation == 'Divide':
                    try:
                        result = divide(a, b)
                    except ZeroDivisionError:
                        st.error("Cannot divide by zero.")
                
                st.success(f'Result: {result}')
        
        elif operation == 'Negate':
            n = st.number_input('Number to Negate', value=0.0, key='num_negate')
            if st.button('Negate', key='negate_btn'):
                result = negate(n)
                st.success(f'Result: {result}')
        
        elif operation == 'Percentage Conversion':
            n = st.number_input('Number for Percentage Conversion', value=0.0, key='num_percent')
            if st.button('Convert', key='percent_btn'):
                result = percentage_conversion(n)
                st.success(f'Result: {result}')
    
    elif page == 'Memory Management':
        st.header('Memory Management')
        
        memory_value = st.session_state.get('memory_value', 0.0)
        st.write(f'Current Memory Value: {memory_value}')
        
        if st.button('Memory Clear', key='mem_clear_btn'):
            memory_clear()
            st.session_state['memory_value'] = 0.0
            st.success('Memory cleared.')
        
        value_to_memory = st.number_input('Value to Add/Subtract to Memory', value=0.0, key='mem_value')
        
        if st.button('Memory Add', key='mem_add_btn'):
            memory_add(value_to_memory)
            st.session_state['memory_value'] += value_to_memory
            st.success(f'Added {value_to_memory} to memory.')
        
        if st.button('Memory Subtract', key='mem_subtract_btn'):
            memory_subtract(value_to_memory)
            st.session_state['memory_value'] -= value_to_memory
            st.success(f'Subtracted {value_to_memory} from memory.')
        
        if st.button('Memory Recall', key='mem_recall_btn'):
            recalled_value = memory_recall()
            st.success(f'Recalled Memory Value: {recalled_value}')

if __name__ == '__main__':
    main()
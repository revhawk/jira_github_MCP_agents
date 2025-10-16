# Simple Calculator

A working Streamlit calculator application generated from Jira tickets.

## Features
- Basic arithmetic operations: +, -, *, /
- Number input (0-9, decimal point)
- Clear, negate, and percentage functions
- Real-time display updates

## Running the App

```bash
streamlit run app.py
```

## Files
- `app.py` - Main Streamlit application
- `modules/arithmetic_core.py` - Core calculator functions

## Key Implementation Details
- Uses `st.rerun()` after button clicks for immediate display updates
- Display shown with `st.markdown()` for proper state reflection
- Session state manages calculator display value

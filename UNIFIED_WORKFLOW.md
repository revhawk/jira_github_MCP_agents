# Unified Application Workflow

## Overview

The unified workflow creates **one integrated Streamlit application** from multiple Jira tickets, with proper software architecture and modular design.

## Key Differences

### Old Workflow (Single Ticket)
- Input: One ticket (e.g., `CAL-1`)
- Output: `generated_code/CAL_1.py` (standalone app)
- Run: `streamlit run generated_code/CAL_1.py`

### New Workflow (Unified)
- Input: Multiple tickets (e.g., `CAL-1, CAL-2, CAL-3`)
- Output: 
  - `app.py` (main Streamlit app)
  - `modules/calculator.py` (business logic)
  - `modules/validator.py` (business logic)
- Run: `streamlit run app.py`

## Workflow Steps

1. **Jira Reader** - Fetches all specified tickets
2. **System Architect** - Designs application structure
   - Groups tickets by functionality
   - Creates logical modules (not ticket-based)
   - Plans main app integration
3. **Spec Agent** - Extracts specs for each module
4. **Spec Reviewer** - Validates specs
5. **Generate Tests** - Creates pytest tests for modules (TDD)
6. **Generate Code** - Implements modules to pass tests
7. **Generate Main App** - Creates Streamlit UI that integrates modules
8. **Run Tests** - Validates all modules

## Usage

```bash
python main.py
# Choose option 3: Unified app
# Enter project key: CAL
# Enter tickets: CAL-1,CAL-2,CAL-3
```

## Output Structure

```
app.py                    # Main Streamlit application
modules/
  __init__.py
  calculator.py           # Business logic module
  validator.py            # Business logic module
generated_tests/
  test_calculator.py      # Module tests
  test_validator.py       # Module tests
```

## Benefits

1. **Better Architecture** - Proper separation of concerns
2. **Better Code Quality** - Modules designed by function, not ticket
3. **Better Tests** - Tests logical units, not arbitrary ticket groupings
4. **Single App** - One cohesive application, not scattered files
5. **Maintainable** - Clear module boundaries and responsibilities

## Example

**Tickets:**
- CAL-1: Add two numbers
- CAL-2: Subtract two numbers
- CAL-3: Validate numeric input

**Architecture:**
```json
{
  "modules": [
    {
      "name": "calculator",
      "tickets": ["CAL-1", "CAL-2"],
      "functions": ["add", "subtract"]
    },
    {
      "name": "validator",
      "tickets": ["CAL-3"],
      "functions": ["validate_number"]
    }
  ]
}
```

**Generated Files:**
- `modules/calculator.py` - Pure functions: `add()`, `subtract()`
- `modules/validator.py` - Pure function: `validate_number()`
- `app.py` - Streamlit UI using sidebar navigation

## Running the App

```bash
streamlit run app.py
```

The app will have:
- Sidebar navigation for different features
- Clean UI for each function
- Integrated experience across all tickets

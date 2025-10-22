# Test Setup Instructions

## Issue
Tests are not running because pytest is not installed in your Python environment.

## Solution Options

### Option 1: Use Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest generated_tests/ -v
```

### Option 2: Install System-Wide (Not Recommended)
```bash
pip install --break-system-packages pytest pytest-json-report
```

### Option 3: Use pipx for Isolated Installation
```bash
# Install pipx if not available
sudo apt install pipx

# Install pytest
pipx install pytest
pipx inject pytest pytest-json-report
```

## Verify Installation
```bash
python -m pytest --version
```

Should output: `pytest 8.x.x` or similar

## Run Generated Tests
```bash
# Run all tests
python -m pytest generated_tests/ -v

# Run specific module tests
python -m pytest generated_tests/test_calculator.py -v

# Run with detailed output
python -m pytest generated_tests/ -vv --tb=short
```

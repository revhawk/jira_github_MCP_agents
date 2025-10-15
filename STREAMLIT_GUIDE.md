# Streamlit App Guide

## ✅ Ensuring Generated Apps Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Validate Project
```bash
python validate_project.py
```

### 3. Run a Streamlit App
```bash
streamlit run generated_code/CAL_1.py
```

## 🔍 Verification

### Check Single File
```bash
python verify_streamlit.py generated_code/CAL_1.py
```

### Check All Files
```bash
for f in generated_code/CAL_*.py; do
  python verify_streamlit.py "$f"
done
```

## 🛠️ Troubleshooting

### App Won't Run
**Symptom:** `streamlit run` fails or shows errors

**Solutions:**
1. Check file has all required components:
   ```python
   # Required:
   import streamlit as st
   
   def main():
       st.title('My App')
       # ... UI code
   
   if __name__ == '__main__':
       main()
   ```

2. Regenerate the file:
   ```bash
   python main.py
   # Choose option 1 (single ticket)
   # Enter ticket key (e.g., CAL-1)
   ```

### Missing Streamlit Import
**Fix:** The code generator now automatically adds Streamlit UI if missing.

### No main() Function
**Fix:** The validator adds a basic main() function automatically.

## 📊 What Gets Generated

Each generated file includes:
1. **ISSUE_KEY** constant
2. **Backend functions** (testable with pytest)
3. **main()** function with Streamlit UI
4. **Entry point** (`if __name__ == '__main__'`)

## 🎯 Quality Checks

The reviewer agent checks:
- ✅ Test quality (coverage, clarity, assertions)
- ✅ Code quality (correctness, type hints, error handling)
- ✅ Streamlit UI completeness
- ✅ All tests pass

## 🚀 Quick Start

```bash
# 1. Generate code
python main.py

# 2. Validate
python validate_project.py

# 3. Run app
streamlit run generated_code/CAL_1.py
```

## 📝 Notes

- All generated apps are standalone
- No dependencies between generated files
- Each app can run independently
- Tests validate backend functions only (not UI)

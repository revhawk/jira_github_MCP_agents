#!/usr/bin/env python3
"""Verify that generated Streamlit apps can run."""
import sys
import subprocess
from pathlib import Path

def verify_streamlit_app(file_path: str) -> bool:
    """Check if a Python file can be run as a Streamlit app."""
    try:
        # Check file exists
        if not Path(file_path).exists():
            print(f"❌ File not found: {file_path}")
            return False
        
        # Read file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check required components
        has_main = "def main():" in content or "def main(" in content
        has_streamlit = "import streamlit" in content or "from streamlit" in content
        has_entrypoint = "if __name__ == '__main__':" in content
        
        if not has_main:
            print(f"❌ {file_path}: Missing main() function")
            return False
        
        if not has_streamlit:
            print(f"❌ {file_path}: Missing streamlit import")
            return False
        
        if not has_entrypoint:
            print(f"❌ {file_path}: Missing if __name__ == '__main__' block")
            return False
        
        # Try to import (syntax check)
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", file_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            print(f"❌ {file_path}: Syntax error")
            print(result.stderr)
            return False
        
        print(f"✅ {file_path}: Ready to run")
        return True
        
    except Exception as e:
        print(f"❌ {file_path}: Error - {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_streamlit.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    success = verify_streamlit_app(file_path)
    sys.exit(0 if success else 1)

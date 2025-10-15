#!/usr/bin/env python3
"""Validate entire project for errors."""
import os
import sys
from pathlib import Path

def validate_project():
    """Run comprehensive project validation."""
    errors = []
    warnings = []
    
    print("🔍 Validating Jira_coder project...\n")
    
    # 1. Check required files
    required_files = [
        "main.py",
        "requirements.txt",
        "graph/langgraph_poc.py",
        "config/settings.py",
        ".env"
    ]
    
    for file in required_files:
        if not Path(file).exists():
            errors.append(f"Missing required file: {file}")
        else:
            print(f"✅ Found: {file}")
    
    # 2. Check generated_code directory
    if not Path("generated_code").exists():
        errors.append("Missing generated_code directory")
    else:
        print(f"✅ Found: generated_code/")
        
        # Check for Streamlit apps
        code_files = list(Path("generated_code").glob("CAL_*.py"))
        print(f"\n📊 Found {len(code_files)} generated code files")
        
        streamlit_ready = 0
        for code_file in code_files:
            with open(code_file, 'r') as f:
                content = f.read()
            
            has_main = "def main():" in content
            has_streamlit = "import streamlit" in content
            has_entrypoint = "if __name__ == '__main__':" in content
            
            if has_main and has_streamlit and has_entrypoint:
                streamlit_ready += 1
            else:
                warnings.append(f"{code_file.name}: Missing Streamlit components")
        
        print(f"   ✅ {streamlit_ready} files ready for Streamlit")
        print(f"   ⚠️  {len(code_files) - streamlit_ready} files need Streamlit UI")
    
    # 3. Check requirements
    if Path("requirements.txt").exists():
        with open("requirements.txt", 'r') as f:
            reqs = f.read()
        
        required_packages = ["streamlit", "openai", "langgraph", "pytest", "jira"]
        missing = [pkg for pkg in required_packages if pkg not in reqs]
        
        if missing:
            errors.append(f"Missing packages in requirements.txt: {', '.join(missing)}")
        else:
            print(f"\n✅ All required packages in requirements.txt")
    
    # 4. Summary
    print("\n" + "="*60)
    print("📋 VALIDATION SUMMARY")
    print("="*60)
    
    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for err in errors:
            print(f"   - {err}")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warn in warnings[:5]:  # Show first 5
            print(f"   - {warn}")
        if len(warnings) > 5:
            print(f"   ... and {len(warnings) - 5} more")
    
    if not errors and not warnings:
        print("\n✅ Project validation passed!")
        print("\n🚀 To run a Streamlit app:")
        print("   streamlit run generated_code/CAL_1.py")
    elif not errors:
        print("\n⚠️  Project has warnings but should work")
        print("\n💡 Regenerate files with warnings using:")
        print("   python main.py")
    else:
        print("\n❌ Project has errors. Fix them before running.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(validate_project())

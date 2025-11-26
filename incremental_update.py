#!/usr/bin/env python3
"""
Incremental Update Mode - Add new features AND regenerate UI

Usage: python3 incremental_update.py CAL-31 CAL-32
"""
import sys
import os
from agents.jira_agent import jira_client
from agents.implementation_agent import write_files
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from config.settings import Settings
import json
import re
from utils.langsmith_stats import display_run_stats

def incremental_update(ticket_keys: list):
    """Add new functions to existing modules based on tickets."""
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0.2, max_tokens=1000)
    
    # Read tickets
    tickets = []
    for key in ticket_keys:
        data = jira_client.read_issue(key)
        if "error" not in data and data.get("issuetype", "").upper() != "EPIC":
            tickets.append({
                "key": key,
                "title": data.get("summary", ""),
                "description": str(data.get("description", ""))
            })
    
    if not tickets:
        print("No tickets found")
        return
    
    print(f"📋 Processing {len(tickets)} tickets: {[t['key'] for t in tickets]}")
    
    # Analyze what functions are needed
    tickets_text = "\n".join([f"{t['key']}: {t['title']}\n{t['description']}" for t in tickets])
    
    analysis_prompt = f"""Analyze these Jira tickets and determine what NEW functions need to be added to the calculator module.

TICKETS:
{tickets_text}

OUTPUT JSON:
{{
  "module": "calculator",
  "new_functions": [
    {{"name": "function_name", "description": "what it does", "params": ["param1", "param2"], "returns": "return_type"}}
  ]
}}
"""
    
    messages = [
        SystemMessage(content="You are a code analyzer. Output ONLY valid JSON, no markdown or explanations."),
        HumanMessage(content=analysis_prompt)
    ]
    resp = llm.invoke(messages)
    analysis = resp.content.strip()
    analysis = re.sub(r'^```json\s*', '', analysis)
    analysis = re.sub(r'```\s*$', '', analysis)
    
    try:
        plan = json.loads(analysis)
        new_funcs = plan.get("new_functions", [])
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse analysis: {e}")
        print(f"Raw response: {analysis[:200]}...")
        return
    
    if not new_funcs:
        print("No new functions identified")
        return
    
    print(f"🔍 Identified {len(new_funcs)} new functions: {[f['name'] for f in new_funcs]}")
    
    # Load existing calculator module
    calc_path = "modules/calculator.py"
    if not os.path.exists(calc_path):
        print(f"❌ {calc_path} not found")
        return
    
    with open(calc_path, 'r') as f:
        existing_code = f.read()
    
    # Check which functions already exist
    existing_funcs = re.findall(r'^def (\w+)\(', existing_code, re.MULTILINE)
    funcs_to_add = [f for f in new_funcs if f['name'] not in existing_funcs]
    
    if not funcs_to_add:
        print("✅ All functions already exist")
        print("\n🎨 Regenerating UI with existing functions...")
        regenerate_ui(existing_code, calc_path)
        return
    
    print(f"➕ Adding {len(funcs_to_add)} new functions: {[f['name'] for f in funcs_to_add]}")
    
    # Generate new functions
    funcs_spec = json.dumps(funcs_to_add, indent=2)
    
    merge_prompt = f"""Add these NEW functions to the existing calculator module. Preserve ALL existing code.

EXISTING CODE:
{existing_code}

NEW FUNCTIONS TO ADD:
{funcs_spec}

RULES:
1. Keep ALL existing functions and imports
2. Add new functions at the end
3. Add necessary imports (e.g., import math for sqrt)
4. Include proper error handling
5. Add docstrings

OUTPUT: Complete merged module code.
"""
    
    llm_code = ChatOpenAI(model="gpt-4o", temperature=0.1, max_tokens=3000)
    messages = [
        SystemMessage(content="You are a Python code expert. Output only valid Python code, no markdown."),
        HumanMessage(content=merge_prompt)
    ]
    resp = llm_code.invoke(messages)
    merged_code = resp.content.strip()
    merged_code = re.sub(r'^```python\s*', '', merged_code)
    merged_code = re.sub(r'```\s*$', '', merged_code)
    
    # Validate syntax
    try:
        compile(merged_code, calc_path, 'exec')
    except SyntaxError as e:
        print(f"❌ Generated code has syntax error: {e}")
        return
    
    # Backup existing file
    backup_path = f"{calc_path}.backup"
    with open(calc_path, 'r') as f:
        with open(backup_path, 'w') as b:
            b.write(f.read())
    
    # Write merged code
    write_files([{"path": calc_path, "content": merged_code}])
    print(f"✅ Updated {calc_path} (backup: {backup_path})")
    
    # Show what was added
    new_funcs_in_code = re.findall(r'^def (\w+)\(', merged_code, re.MULTILINE)
    added = [f for f in new_funcs_in_code if f not in existing_funcs]
    print(f"📝 Added functions: {added}")
    
    # Regenerate UI with all functions
    print("\n🎨 Regenerating UI with all functions...")
    regenerate_ui(merged_code, calc_path)

def regenerate_ui(module_code: str, module_path: str):
    """Regenerate app.py UI to include new functions."""
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import SystemMessage, HumanMessage
    from config.settings import Settings
    from agents.implementation_agent import write_files
    import re
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1, max_tokens=4000)
    
    # Extract all function signatures from module
    func_matches = re.findall(r'^def (\w+)\(([^)]*)\)', module_code, re.MULTILINE)
    functions = [{"name": name, "params": params} for name, params in func_matches]
    
    # Load existing app.py if it exists
    app_path = "app.py"
    existing_app = ""
    if os.path.exists(app_path):
        with open(app_path, 'r') as f:
            existing_app = f.read()
    
    # Load reference examples
    ref_examples = ""
    ref_dir = "reference_examples/streamlit_apps"
    if os.path.exists(ref_dir):
        for fname in os.listdir(ref_dir):
            if fname.endswith('.py'):
                with open(os.path.join(ref_dir, fname), 'r') as f:
                    ref_examples += f"\n--- {fname} ---\n{f.read()}\n"
    
    ui_prompt = f"""Regenerate the Streamlit calculator UI to include ALL available functions.

AVAILABLE FUNCTIONS:
{json.dumps(functions, indent=2)}

EXISTING APP.PY:
{existing_app}

REFERENCE EXAMPLES:
{ref_examples}

REQUIREMENTS:
1. Keep existing UI patterns (button grid, mode toggles, memory buttons)
2. Add UI elements for NEW functions:
   - If hex functions exist: Add HEX mode toggle AND A-F hex digit buttons
   - A-F buttons should only show when mode is HEX
   - Use unique keys for hex buttons (e.g., key='C_hex' to avoid conflict with Clear)
3. Import all functions from modules.calculator
4. Use st.rerun() for button clicks
5. Handle DEC/BIN/HEX modes if hex functions exist:
   - Mode conversion must handle all combinations: DEC↔BIN, DEC↔HEX, BIN↔HEX
   - Store old_mode before switching to know how to convert
   - DEC→BIN: bin(int(eval(display)))[2:]
   - DEC→HEX: hex(int(eval(display)))[2:].upper()
   - BIN→DEC: str(int(display, 2))
   - BIN→HEX: hex(int(display, 2))[2:].upper()
   - HEX→DEC: str(int(display, 16))
   - HEX→BIN: bin(int(display, 16))[2:]
6. Arithmetic evaluation per mode:
   - BIN: Split by operators, convert binary to decimal, eval, convert back to binary
   - HEX: Split by operators ([+\-*/]), convert each hex number to decimal, eval, convert back to hex
   - DEC: Normal eval
7. Operations that produce decimals (√, /, etc.):
   - If in BIN or HEX mode and result has decimals, auto-switch to DEC mode
   - Example: √C in HEX → convert C to 12, calculate √12=3.464, switch to DEC, show 3.464
   - This prevents truncation and preserves precision
8. Negate (±) button:
   - Must handle negative numbers in all modes
   - BIN: Convert to decimal, negate, convert back
   - HEX: Convert to decimal, negate, convert back
   - DEC: Normal negation
9. Maintain clean button grid layout
10. Keep all existing features working (memory, square root, etc.)
11. Disable inappropriate buttons per mode:
    - BIN mode: Disable 2-9, A-F
    - HEX mode: Enable 0-9, A-F
    - DEC mode: Enable 0-9, disable A-F

OUTPUT: Complete app.py code with updated UI including all hex functionality and edge cases.
"""
    
    messages = [
        SystemMessage(content="You are a Streamlit UI expert. Output only valid Python code, no markdown."),
        HumanMessage(content=ui_prompt)
    ]
    resp = llm.invoke(messages)
    new_app_code = resp.content.strip()
    new_app_code = re.sub(r'^```python\s*', '', new_app_code)
    new_app_code = re.sub(r'```\s*$', '', new_app_code)
    
    # Validate syntax
    try:
        compile(new_app_code, app_path, 'exec')
    except SyntaxError as e:
        print(f"⚠️  Generated UI has syntax error: {e}")
        print("   Keeping existing app.py")
        return
    
    # Backup existing app.py
    if os.path.exists(app_path):
        backup_path = f"{app_path}.backup"
        with open(app_path, 'r') as f:
            with open(backup_path, 'w') as b:
                b.write(f.read())
        print(f"💾 Backed up app.py to {backup_path}")
    
    # Write new app.py
    write_files([{"path": app_path, "content": new_app_code}])
    print(f"✅ Updated {app_path} with new UI")
    print("\n🚀 Run: streamlit run app.py")
    
    # Display LangSmith stats for this run
    display_run_stats(limit=20)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 incremental_update.py CAL-31 CAL-32")
        sys.exit(1)
    
    ticket_keys = sys.argv[1:]
    incremental_update(ticket_keys)

#!/usr/bin/env python3
"""
Incremental Update Mode - Add new features without regenerating app.py

Usage: python3 incremental_update.py CAL-31 CAL-32
"""
import sys
import os
from agents.jira_agent import jira_client
from agents.implementation_agent import write_files
from openai import OpenAI
from config.settings import Settings
import json
import re

def incremental_update(ticket_keys: list):
    """Add new functions to existing modules based on tickets."""
    
    client = OpenAI(api_key=Settings.OPENAI_API_KEY)
    
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
    
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a code analyzer. Output ONLY valid JSON, no markdown or explanations."},
            {"role": "user", "content": analysis_prompt}
        ],
        temperature=0.2,
        max_tokens=1000
    )
    
    analysis = resp.choices[0].message.content.strip()
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
    
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a Python code expert. Output only valid Python code, no markdown."},
            {"role": "user", "content": merge_prompt}
        ],
        temperature=0.1,
        max_tokens=3000
    )
    
    merged_code = resp.choices[0].message.content.strip()
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
    
    print("\n⚠️  NOTE: app.py was NOT modified. You need to manually add UI for new functions.")
    print("   Or run full generation to regenerate app.py with new features.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 incremental_update.py CAL-31 CAL-32")
        sys.exit(1)
    
    ticket_keys = sys.argv[1:]
    incremental_update(ticket_keys)

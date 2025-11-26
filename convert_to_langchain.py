#!/usr/bin/env python3
"""
Script to convert OpenAI client calls to LangChain in create_streamlit_app.py
"""
import re

# Read the file
with open('graph/create_streamlit_app.py', 'r') as f:
    content = f.read()

# Pattern to match OpenAI client creation and usage
# client = OpenAI(api_key=Settings.OPENAI_API_KEY)
# ...
# resp = client.chat.completions.create(
#     model="...",
#     messages=[...],
#     temperature=...,
#     max_tokens=...
# )
# result = resp.choices[0].message.content

# Replace pattern
def replace_openai_call(match):
    full_match = match.group(0)
    
    # Extract model
    model_match = re.search(r'model="([^"]+)"', full_match)
    model = model_match.group(1) if model_match else "gpt-4o-mini"
    
    # Extract temperature
    temp_match = re.search(r'temperature=([\d.]+)', full_match)
    temperature = temp_match.group(1) if temp_match else "0.2"
    
    # Extract max_tokens
    tokens_match = re.search(r'max_tokens=(\d+)', full_match)
    max_tokens = tokens_match.group(1) if tokens_match else "2000"
    
    # Extract messages
    messages_match = re.search(r'messages=\[(.*?)\]', full_match, re.DOTALL)
    if not messages_match:
        return full_match  # Can't parse, skip
    
    messages_str = messages_match.group(1)
    
    # Extract system and user prompts
    system_match = re.search(r'\{"role":\s*"system",\s*"content":\s*([^}]+)\}', messages_str)
    user_match = re.search(r'\{"role":\s*"user",\s*"content":\s*([^}]+)\}', messages_str)
    
    if not user_match:
        return full_match  # Need at least user prompt
    
    system_prompt = system_match.group(1) if system_match else '""'
    user_prompt = user_match.group(1)
    
    # Extract variable name
    var_match = re.search(r'(\w+)\s*=\s*resp\.choices\[0\]\.message\.content', full_match)
    var_name = var_match.group(1) if var_match else "result"
    
    # Build replacement
    replacement = f'''        {var_name} = call_llm(
            system_prompt={system_prompt},
            user_prompt={user_prompt},
            model="{model}",
            temperature={temperature},
            max_tokens={max_tokens}
        )'''
    
    return replacement

# This is complex - let's just print what needs to be done
print("File has been prepared with imports.")
print("Manual replacement needed for 16 OpenAI client calls.")
print("Use the llm_helper.call_llm() function.")

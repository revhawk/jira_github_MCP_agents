#!/usr/bin/env python3
"""Convert OpenAI calls to LangChain in create_streamlit_app.py"""
import re

with open('graph/create_streamlit_app.py', 'r') as f:
    content = f.read()

# Pattern 1: Simple client instantiation followed by chat completion
# Replace: client = OpenAI(...) followed by client.chat.completions.create(...)
# With: call_llm(...)

# Find all occurrences of client.chat.completions.create and replace with call_llm
def convert_openai_to_langchain(content):
    # Pattern to match the full OpenAI call structure
    pattern = r'client = OpenAI\(api_key=Settings\.OPENAI_API_KEY\)\s+.*?resp = client\.chat\.completions\.create\((.*?)\)\s+(.*?)= (?:resp\.choices\[0\]\.message\.content|.*?resp\.choices\[0\]\.message\.content.*?$)'
    
    # This is too complex for regex. Let's do manual replacements.
    # Remove all "client = OpenAI(api_key=Settings.OPENAI_API_KEY)" lines
    content = re.sub(r'\s*client = OpenAI\(api_key=Settings\.OPENAI_API_KEY\)\s*\n', '\n', content)
    
    return content

# Just remove the client instantiations for now
content = convert_openai_to_langchain(content)

with open('graph/create_streamlit_app.py', 'w') as f:
    f.write(content)

print("Removed OpenAI client instantiations. Now need to convert client.chat.completions.create calls.")

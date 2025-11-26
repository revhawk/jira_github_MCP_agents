#!/usr/bin/env python3
"""
Jira Coder - Streamlit Web UI
AI-powered code generation from Jira tickets
"""
import streamlit as st
import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(
    page_title="Jira Coder",
    page_icon="🔧",
    layout="wide"
)

# Initialize session state
if 'generation_running' not in st.session_state:
    st.session_state.generation_running = False
if 'log_output' not in st.session_state:
    st.session_state.log_output = []

# Title
st.title("🔧 Jira Coder")
st.markdown("AI-powered code generation from Jira tickets")

# Sidebar - Mode Selection
st.sidebar.header("Mode Selection")
mode = st.sidebar.radio(
    "Choose Mode:",
    [
        "1. TDD Workflow",
        "2. Full Generation",
        "3. Incremental Update",
        "4. Compare Archives",
        "10. Demo: Basic Calculator",
        "11. Demo: Calculator with Memory",
        "12. Demo: Calculator with Binary",
    ]
)

mode_num = mode.split(".")[0]

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Configuration")
    
    if mode_num in ["1", "2", "3"]:
        # Generation modes
        if mode_num == "1":
            st.subheader("TDD Workflow - Single Ticket")
            ticket_key = st.text_input("Jira Ticket Key", placeholder="CAL-1")
            
            if st.button("Generate Module", type="primary"):
                if ticket_key:
                    st.session_state.generation_running = True
                    with st.spinner(f"Generating module for {ticket_key}..."):
                        try:
                            result = subprocess.run(
                                ["python3", "main.py"],
                                input=f"1\n{ticket_key}\n",
                                capture_output=True,
                                text=True,
                                timeout=300
                            )
                            st.success("✅ Generation complete!")
                            st.code(result.stdout, language="text")
                            if result.stderr:
                                st.error(result.stderr)
                        except subprocess.TimeoutExpired:
                            st.error("⏱️ Generation timed out (5 min limit)")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                        finally:
                            st.session_state.generation_running = False
                else:
                    st.warning("Please enter a ticket key")
        
        elif mode_num == "2":
            st.subheader("Full Generation - Multiple Tickets")
            
            # Check for existing code
            if os.path.exists("app.py") or (os.path.exists("modules") and any(f.endswith('.py') for f in os.listdir("modules"))):
                st.warning("⚠️ Existing code detected!")
                backup_option = st.radio(
                    "Choose action:",
                    ["Backup and regenerate", "Cancel", "Overwrite (DANGEROUS)"]
                )
            else:
                backup_option = None
            
            project_key = st.text_input("Project Key", value="CAL")
            ticket_input = st.text_input("Ticket Keys (comma-separated, or leave empty for ALL)", placeholder="CAL-1,CAL-2,CAL-3")
            
            if st.button("Generate Application", type="primary"):
                if backup_option == "Cancel":
                    st.info("ℹ️ Cancelled. Use Mode 3 for incremental updates.")
                elif backup_option == "Overwrite (DANGEROUS)":
                    confirm = st.text_input("Type 'DELETE' to confirm:")
                    if confirm != "DELETE":
                        st.error("Confirmation required")
                        st.stop()
                
                if project_key:
                    st.session_state.generation_running = True
                    with st.spinner(f"Generating application for {project_key}..."):
                        try:
                            input_text = f"2\n{project_key}\n{ticket_input}\n"
                            if backup_option == "Backup and regenerate":
                                input_text = f"2\n1\n{project_key}\n{ticket_input}\n"
                            
                            result = subprocess.run(
                                ["python3", "main.py"],
                                input=input_text,
                                capture_output=True,
                                text=True,
                                timeout=600
                            )
                            st.success("✅ Generation complete!")
                            st.code(result.stdout, language="text")
                            if result.stderr:
                                st.error(result.stderr)
                        except subprocess.TimeoutExpired:
                            st.error("⏱️ Generation timed out (10 min limit)")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                        finally:
                            st.session_state.generation_running = False
                else:
                    st.warning("Please enter a project key")
        
        elif mode_num == "3":
            st.subheader("Incremental Update - Add Features")
            ticket_keys = st.text_input("Ticket Keys to Add", placeholder="CAL-31,CAL-32")
            
            if st.button("Add Features", type="primary"):
                if ticket_keys:
                    st.session_state.generation_running = True
                    with st.spinner(f"Adding features from {ticket_keys}..."):
                        try:
                            result = subprocess.run(
                                ["python3", "main.py"],
                                input=f"3\n{ticket_keys}\n",
                                capture_output=True,
                                text=True,
                                timeout=300
                            )
                            st.success("✅ Features added!")
                            st.code(result.stdout, language="text")
                            if result.stderr:
                                st.error(result.stderr)
                        except subprocess.TimeoutExpired:
                            st.error("⏱️ Update timed out (5 min limit)")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                        finally:
                            st.session_state.generation_running = False
                else:
                    st.warning("Please enter ticket keys")
    
    elif mode_num == "4":
        # Compare archives
        st.subheader("Compare Archived Apps")
        
        # List archives
        archive_dir = "archive"
        if os.path.exists(archive_dir):
            archives = [d for d in os.listdir(archive_dir) if os.path.isdir(os.path.join(archive_dir, d))]
            archives.sort(reverse=True)
            
            if archives:
                archive_options = {f"{20+i}. {arch}": arch for i, arch in enumerate(archives[:10])}
                
                col_a, col_b = st.columns(2)
                with col_a:
                    archive1 = st.selectbox("First Archive", options=list(archive_options.keys()))
                with col_b:
                    archive2 = st.selectbox("Second Archive", options=list(archive_options.keys()))
                
                if st.button("Compare", type="primary"):
                    mode1 = int(archive1.split(".")[0])
                    mode2 = int(archive2.split(".")[0])
                    
                    with st.spinner("Comparing archives..."):
                        try:
                            result = subprocess.run(
                                ["python3", "compare_archives.py", str(mode1), str(mode2)],
                                capture_output=True,
                                text=True,
                                timeout=30
                            )
                            st.code(result.stdout, language="diff")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
            else:
                st.info("No archives found. Generate apps first to create archives.")
        else:
            st.info("No archive directory found.")
    
    else:
        # Demo modes
        demo_paths = {
            "10": "demos/basic_calculator.py",
            "11": "demos/calculator_with_memory.py",
            "12": "demos/calculator_with_binary.py"
        }
        
        demo_path = demo_paths.get(mode_num)
        
        if demo_path and os.path.exists(demo_path):
            st.subheader(f"Demo: {mode.split(': ')[1]}")
            st.info("Click the button below to launch the demo in a new Streamlit instance")
            
            if st.button("Launch Demo", type="primary"):
                st.info(f"🚀 Launching demo...")
                st.code(f"streamlit run {demo_path}", language="bash")
                st.markdown("Run this command in your terminal to launch the demo.")
        else:
            st.error(f"Demo not found at {demo_path}")

with col2:
    st.header("Status")
    
    # Show generated files
    if os.path.exists("app.py"):
        st.success("✅ app.py exists")
        if st.button("View app.py"):
            with open("app.py", "r") as f:
                st.code(f.read(), language="python")
    
    if os.path.exists("modules"):
        modules = [f for f in os.listdir("modules") if f.endswith('.py') and f != '__init__.py']
        if modules:
            st.success(f"✅ {len(modules)} modules")
            selected_module = st.selectbox("View module:", modules)
            if selected_module:
                with open(f"modules/{selected_module}", "r") as f:
                    st.code(f.read(), language="python")
    
    # Show recent logs
    st.subheader("Recent Logs")
    if os.path.exists("logs"):
        logs = sorted([f for f in os.listdir("logs") if f.endswith('.log')], reverse=True)
        if logs:
            latest_log = logs[0]
            if st.button("View Latest Log"):
                with open(f"logs/{latest_log}", "r") as f:
                    st.text_area("Log Output", f.read(), height=300)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Actions")
if st.sidebar.button("🗂️ Open Archive Folder"):
    st.sidebar.code("archive/", language="text")
if st.sidebar.button("📊 View Test Results"):
    if os.path.exists("generated_tests/.report.json"):
        import json
        with open("generated_tests/.report.json", "r") as f:
            report = json.load(f)
            st.sidebar.json(report)
    else:
        st.sidebar.info("No test results yet")

# LangSmith Stats
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 LangSmith Stats")

api_key = os.getenv("LANGCHAIN_API_KEY")
project_name = os.getenv("LANGCHAIN_PROJECT", "jira-code-generator")

if api_key:
    if st.sidebar.button("🔄 Refresh Stats"):
        try:
            from langsmith import Client
            client = Client(api_key=api_key)
            
            runs = list(client.list_runs(project_name=project_name, limit=10))
            
            if runs:
                total_tokens = sum(getattr(run, 'total_tokens', 0) or 0 for run in runs)
                success_count = sum(1 for run in runs if run.status == "success")
                
                st.sidebar.metric("Recent Runs", len(runs))
                st.sidebar.metric("Success Rate", f"{success_count}/{len(runs)}")
                st.sidebar.metric("Total Tokens", f"{total_tokens:,}")
                st.sidebar.metric("Est. Cost", f"${total_tokens * 0.000001:.4f}")
                
                st.sidebar.markdown(f"[View Dashboard →](https://smith.langchain.com/)")
            else:
                st.sidebar.info("No runs yet")
        except ImportError:
            st.sidebar.warning("Install: `pip install langsmith`")
        except Exception as e:
            st.sidebar.error(f"Error: {str(e)[:50]}")
else:
    st.sidebar.info("Add LANGCHAIN_API_KEY to .env")
    st.sidebar.markdown("[Get API Key →](https://smith.langchain.com/)")

st.sidebar.markdown("---")
st.sidebar.caption("Jira Coder v2.0 | AI-Powered Code Generation")

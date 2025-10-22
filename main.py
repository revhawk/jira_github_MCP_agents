#!/usr/bin/env python3
"""
Jira Coder: AI-powered code generation from Jira tickets.

This is the main entry point for the application. It allows users to choose between different code generation modes.
"""
import subprocess
from config.settings import Settings
from graph.tdd_code import run_poc_graph
from graph.create_streamlit_app import run_unified_graph
from agents.jira_agent import jira_client
import json
import os

# Constants for mode selection and paths
MODE_TDD = "1"
MODE_UNIFIED = "2"
MODE_DEMO = "3"
MAX_JIRA_RESULTS = 50
DEMO_APP_PATH = "simple_calculator/app.py"

def main():
    """
    Main function to run the Jira Coder application.

    Presents the user with a choice of modes:
    1. Generate Standalone Module: Creates a tested module from one or more tickets using a TDD workflow.
    2. Build Integrated Application: Creates a single, unified Streamlit application from multiple tickets.
    3. Run Calculator Demo: Launches a pre-built demo application.
    """
    # Ensure all env vars are present
    Settings.check()

    # Ask user for mode
    print("\n🔧 Jira Coder")
    print("1. Generate Standalone code and tests (from a single Jira ticket using TDD)") # This is already correct
    print("2. Build Integrated Application (from multiple tickets)") # This is already correct
    print("3. Run Calculator Demo") # This is already correct
    try:
        # Default to '2' (Unified App) if user just presses Enter, as per previous request
        mode = input("Choose mode (1, 2, or 3): ").strip() or MODE_UNIFIED
    except EOFError:
        mode = MODE_UNIFIED # Default to unified app on EOF

    if mode == MODE_UNIFIED:
        # Mode 2: Build Integrated Application
        try:
            project_key = input("Enter Jira project key (e.g., CAL): ").strip().upper()
        except EOFError:
            project_key = ""
        if not project_key:
            print("⚠️ No project key provided. Exiting.")
            return
        
        try:
            ticket_input = input("Enter ticket keys (comma-separated, or press Enter for ALL): ").strip()
        except EOFError:
            ticket_input = ""
        
        if not ticket_input:
            # Load all tickets from project
            print(f"\n📦 Fetching all tickets from {project_key}...")
            result = jira_client.list_all_issues_in_project(project_key, max_results=MAX_JIRA_RESULTS)
            issues = result.get("issues", [])
            if not issues:
                print(f"⚠️ No tickets found in {project_key}. Details: {result.get('details')}")
                return
            ticket_keys = [issue.get("key") for issue in issues]
            print(f"Found {len(ticket_keys)} tickets: {', '.join(ticket_keys[:5])}{'...' if len(ticket_keys) > 5 else ''}")
        else:
            ticket_keys = [k.strip() for k in ticket_input.split(",") if k.strip()]
        
        print(f"\n🏗️ Building integrated application for {len(ticket_keys)} tickets...")
        run_unified_graph(project_key, ticket_keys)

    elif mode == MODE_DEMO:
        # Mode 3: Run the calculator demo
        print(f"\n🚀 Launching calculator demo from '{DEMO_APP_PATH}'...")
        if os.path.exists(DEMO_APP_PATH):
            subprocess.run(["streamlit", "run", DEMO_APP_PATH])
        else:
            print(f"⚠️  Demo application not found at '{DEMO_APP_PATH}'.")
            print("   Please ensure the calculator app is saved in the 'simple_calculator' directory.")
    
    else: # mode == MODE_TDD or default to 1
        # Mode 1: Generate Standalone Module (can be single or bulk)
        # For Mode 1, we only need the ticket key.
        ticket_key = input("Enter a single Jira ticket key (e.g., CAL-1): ").strip().upper()
        if not ticket_key:
            print("⚠️ No ticket key provided. Exiting.")
            return
        
        print(f"\n--- Processing {ticket_key} with TDD workflow ---")
        status = "✅ success"
        try:
            run_poc_graph(ticket_key)
        except Exception as e:
            print(f"⚠️ Error processing {ticket_key}: {e}")
            status = f"❌ error: {e}"
        
        # For a single ticket, just print the result directly
        print("\n" + "="*60)
        print(f"📊 TDD Generation Result for {ticket_key}")
        print("="*60)
        print(f"{ticket_key}: {status}")
        print("="*60)
        
        # No manifest for single ticket, as it's not a bulk run

if __name__ == "__main__":
    main()

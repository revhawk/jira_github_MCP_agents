# main.py
from config.settings import Settings
from graph.langgraph_poc import run_poc_graph
from graph.langgraph_unified import run_unified_graph
from agents.jira_agent import jira_client
import time
import json
import os

def main():
    # Ensure all env vars are present
    Settings.check()

    # Ask user for mode
    print("\n🔧 Jira Coder")
    print("1. Generate Standalone Module (from a single ticket via TDD)")
    print("2. Build Integrated Application (from multiple tickets)")
    print("3. Run Calculator Demo")
    try:
        mode = input("Choose mode (1, 2, or 3): ").strip()
    except EOFError:
        mode = "1"

    if mode == "2":
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
            result = jira_client.list_all_issues_in_project(project_key, max_results=50)
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

    elif mode == "3":
        # Mode 3: Run the calculator demo
        demo_app_path = "simple_calculator/app.py"
        print(f"\n🚀 Launching calculator demo from '{demo_app_path}'...")
        if os.path.exists(demo_app_path):
            os.system(f"streamlit run {demo_app_path}")
        else:
            print(f"⚠️  Demo application not found at '{demo_app_path}'.")
            print("   Please ensure the calculator app is saved in the 'simple_calculator' directory.")
    
    else: # mode == "1" or default
        # Mode 1: Generate Standalone Module (can be single or bulk)
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
            print(f"\n📦 Fetching all tickets from {project_key}...")
            result = jira_client.list_all_issues_in_project(project_key, max_results=100)
            issues = result.get("issues", [])
            if not issues:
                print(f"⚠️ Could not fetch issues: {result.get('error')}")
                return
            ticket_keys = [issue.get("key") for issue in issues]
            print(f"Found {len(ticket_keys)} tickets. Starting bulk generation...")
        else:
            ticket_keys = [k.strip() for k in ticket_input.split(",") if k.strip()]

        summary = []
        print(f"\nProcessing {len(ticket_keys)} ticket(s) with TDD workflow...\n")
        for idx, key in enumerate(ticket_keys, start=1):
            print(f"\n--- [{idx}/{len(ticket_keys)}] Processing {key} ---")
            try:
                result = run_poc_graph(key)
                summary.append({"key": key, "status": "✅ success"})
            except Exception as e:
                print(f"⚠️ Error processing {key}: {e}")
                summary.append({"key": key, "status": f"❌ error: {e}"})
            # Small delay to avoid rate limits
            if idx < len(ticket_keys):
                time.sleep(1)
        
        if len(ticket_keys) > 1:
            # Print summary table for bulk runs
            print("\n" + "="*60)
            print("📊 TDD Generation Summary")
            print("="*60)
            for item in summary:
                print(f"{item['key']}: {item['status']}")
            print("="*60)
            
            # Save manifest
            manifest_path = "workspace/tdd_manifest.json"
            os.makedirs("workspace", exist_ok=True)
            with open(manifest_path, "w") as f:
                json.dump(summary, f, indent=2)
            print(f"\n📄 Manifest saved to {manifest_path}")

if __name__ == "__main__":
    main()

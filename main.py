# main.py
from config.settings import Settings
from graph.langgraph_poc import run_poc_graph
from graph.langgraph_unified import run_unified_graph
from agents.jira_agent import list_recent_tickets, list_all_issues_in_project
import time
import json

def main():
    # Ensure all env vars are present
    Settings.check()

    # Ask user for mode
    print("\n🔧 Jira Code Generator")
    print("1. Single ticket (standalone app per ticket)")
    print("2. Bulk import (standalone apps for all tickets)")
    print("3. Unified app (one integrated Streamlit app)")
    try:
        mode = input("Choose mode (1, 2, or 3): ").strip()
    except EOFError:
        mode = "1"

    if mode == "3":
        # Unified mode
        try:
            project_key = input("Enter Jira project key (e.g., CAL): ").strip().upper()
        except EOFError:
            project_key = ""
        if not project_key:
            print("⚠️  No project key provided. Exiting.")
            return
        
        try:
            ticket_input = input("Enter ticket keys (comma-separated, or press Enter to load ALL): ").strip()
        except EOFError:
            ticket_input = ""
        
        if not ticket_input:
            # Load all tickets from project
            print(f"\n📦 Fetching all tickets from {project_key}...")
            result = list_all_issues_in_project(project_key, max_results=50)
            issues = result.get("issues", [])
            if not issues:
                print(f"⚠️  No tickets found in {project_key}")
                return
            ticket_keys = [issue.get("key") for issue in issues]
            print(f"Found {len(ticket_keys)} tickets: {', '.join(ticket_keys[:5])}{'...' if len(ticket_keys) > 5 else ''}")
        else:
            ticket_keys = [k.strip() for k in ticket_input.split(",") if k.strip()]
        
        print(f"\n🏗️  Creating unified app for {len(ticket_keys)} tickets...")
        run_unified_graph(project_key, ticket_keys)
    
    elif mode == "2":
        # Bulk mode
        try:
            project_key = input("Enter Jira project key (e.g., MFLP): ").strip().upper()
        except EOFError:
            project_key = ""
        if not project_key:
            print("⚠️  No project key provided. Exiting.")
            return
        
        print(f"\n📦 Fetching all issues from project {project_key}...")
        result = list_all_issues_in_project(project_key, max_results=100)
        issues = result.get("issues", [])
        if not issues:
            err = result.get("error")
            print(f"⚠️  Could not fetch issues: {err}")
            return
        
        print(f"Found {len(issues)} issue(s). Starting generation...\n")
        summary = []
        for idx, issue in enumerate(issues, start=1):
            key = issue.get("key")
            fields = issue.get("fields", {})
            title = fields.get("summary", "")
            print(f"\n[{idx}/{len(issues)}] Processing {key}: {title}")
            try:
                run_poc_graph(key)
                summary.append({"key": key, "status": "✅ success"})
            except Exception as e:
                print(f"⚠️  Error processing {key}: {e}")
                summary.append({"key": key, "status": f"❌ error: {e}"})
            # Small delay to avoid rate limits
            if idx < len(issues):
                time.sleep(1)
        
        # Print summary table
        print("\n" + "="*60)
        print("📊 Bulk Generation Summary")
        print("="*60)
        for item in summary:
            print(f"{item['key']}: {item['status']}")
        print("="*60)
        
        # Save manifest
        with open("generation_manifest.json", "w") as f:
            json.dump(summary, f, indent=2)
        print("\n📄 Manifest saved to generation_manifest.json")
        
    else:
        # Single ticket mode
        listing = list_recent_tickets(max_results=10, project_key=Settings.JIRA_PROJECT_KEY, board_id=Settings.JIRA_BOARD_ID)
        issues = listing.get("issues", [])
        if issues:
            print("\n🗂  Recent Jira Issues:")
            for idx, issue in enumerate(issues, start=1):
                key = issue.get("key")
                fields = issue.get("fields", {})
                summary = fields.get("summary", "(no summary)")
                status = fields.get("status", {}).get("name", "unknown")
                print(f"  {idx}. {key} [{status}] - {summary}")
        else:
            err = listing.get("error")
            if err:
                print(f"⚠️  Could not list issues: {err}")

        try:
            issue_key = input("\nEnter Jira issue key from the list (e.g., PROJ-123): ").strip()
        except EOFError:
            issue_key = ""

        if not issue_key:
            print("⚠️  No issue key provided. Exiting.")
            return

        run_poc_graph(issue_key)

if __name__ == "__main__":
    main()

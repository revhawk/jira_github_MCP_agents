#!/usr/bin/env python3
"""View LangSmith statistics for the Jira Code Generator project."""

import os
from datetime import datetime, timedelta
from langsmith import Client
from dotenv import load_dotenv

load_dotenv()

def main():
    api_key = os.getenv("LANGCHAIN_API_KEY")
    project_name = os.getenv("LANGCHAIN_PROJECT", "jira-code-generator")
    
    if not api_key:
        print("❌ LANGCHAIN_API_KEY not found in .env file")
        return
    
    client = Client(api_key=api_key)
    
    print(f"📊 LangSmith Stats for Project: {project_name}\n")
    print(f"🌐 Dashboard: https://smith.langchain.com/\n")
    
    # Get recent runs
    try:
        runs = list(client.list_runs(project_name=project_name, limit=10))
        
        if not runs:
            print("ℹ️  No runs found yet. Run the Jira Code Generator to see stats here.")
            return
        
        print(f"📝 Recent Runs (Last 10):\n")
        print(f"{'Status':<10} {'Name':<30} {'Tokens':<10} {'Cost':<10} {'Time'}")
        print("-" * 80)
        
        total_tokens = 0
        total_cost = 0.0
        
        for run in runs:
            status = "✅" if run.status == "success" else "❌"
            name = (run.name or "unnamed")[:28]
            tokens = getattr(run, 'total_tokens', 0) or 0
            
            # Estimate cost (rough approximation)
            cost = tokens * 0.000001 if tokens else 0
            
            duration = ""
            if run.end_time and run.start_time:
                delta = run.end_time - run.start_time
                duration = f"{delta.total_seconds():.1f}s"
            
            print(f"{status:<10} {name:<30} {tokens:<10} ${cost:<9.4f} {duration}")
            
            total_tokens += tokens
            total_cost += cost
        
        print("-" * 80)
        print(f"{'TOTAL':<10} {'':<30} {total_tokens:<10} ${total_cost:<9.4f}")
        print(f"\n💡 View detailed traces at: https://smith.langchain.com/")
        
    except Exception as e:
        print(f"❌ Error fetching runs: {e}")
        print(f"\n💡 Make sure your LANGCHAIN_API_KEY is valid")
        print(f"💡 View stats at: https://smith.langchain.com/")

if __name__ == "__main__":
    main()

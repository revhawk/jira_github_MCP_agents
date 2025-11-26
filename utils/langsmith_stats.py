#!/usr/bin/env python3
"""
LangSmith stats display utility
"""
import os
from datetime import datetime, timedelta
from functools import wraps

def display_run_stats(limit=5):
    """Display LangSmith stats for recent runs."""
    api_key = os.getenv("LANGCHAIN_API_KEY")
    project_name = os.getenv("LANGCHAIN_PROJECT", "jira-code-generator")
    
    if not api_key:
        return
    
    try:
        from langsmith import Client
        client = Client(api_key=api_key)
        
        # Get recent runs
        runs = list(client.list_runs(
            project_name=project_name,
            limit=limit
        ))
        
        if not runs:
            return
        
        print("\n" + "="*60)
        print(f"📊 LangSmith Stats (Last {len(runs)} Runs)")
        print("="*60)
        
        total_tokens = 0
        total_cost = 0.0
        
        for run in runs:
            status = "✅" if run.status == "success" else "❌"
            name = (run.name or "unnamed")[:35]
            tokens = getattr(run, 'total_tokens', 0) or 0
            cost = tokens * 0.000001 if tokens else 0
            
            duration = ""
            if run.end_time and run.start_time:
                delta = run.end_time - run.start_time
                duration = f"{delta.total_seconds():.1f}s"
            
            print(f"{status} {name:<35} {tokens:>8} tokens  ${cost:>7.4f}  {duration}")
            
            total_tokens += tokens
            total_cost += cost
        
        print("-"*60)
        print(f"{'TOTAL':<37} {total_tokens:>8} tokens  ${total_cost:>7.4f}")
        print("="*60)
        print(f"🌐 View details: https://smith.langchain.com/")
        print()
        
    except ImportError:
        pass  # langsmith not installed
    except Exception:
        pass  # silently fail if LangSmith unavailable

def with_langsmith_stats(func):
    """Decorator to display LangSmith stats after function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        display_run_stats()
        return result
    return wrapper

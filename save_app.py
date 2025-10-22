#!/usr/bin/env python3
"""
Save generated app to archive after manual testing.

Usage:
    python3 save_app.py <project_key> [app_name]
    
Example:
    python3 save_app.py CAL calculator
    python3 save_app.py CAL  # Uses project_key as name
"""
import sys
import os
import shutil
from datetime import datetime

def save_app(project_key: str, app_name: str = None):
    """Save current generated app to archive directory."""
    
    # Use project_key as app_name if not provided
    if not app_name:
        app_name = project_key.lower()
    
    # Create archive directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_dir = f"archive/{app_name}_{timestamp}"
    
    print(f"📦 Saving app to {archive_dir}...")
    
    # Create archive directory
    os.makedirs(archive_dir, exist_ok=True)
    
    # Files/directories to save
    items_to_save = [
        ("app.py", "app.py"),
        ("modules/", "modules/"),
        ("generated_tests/", "generated_tests/"),
    ]
    
    saved_count = 0
    for src, dst in items_to_save:
        if os.path.exists(src):
            dst_path = os.path.join(archive_dir, dst)
            if os.path.isdir(src):
                shutil.copytree(src, dst_path)
                print(f"  ✅ Saved {src}")
            else:
                shutil.copy2(src, dst_path)
                print(f"  ✅ Saved {src}")
            saved_count += 1
        else:
            print(f"  ⚠️  Skipped {src} (not found)")
    
    # Find and copy the latest log file
    log_pattern = f"logs/unified_{project_key}_*.log"
    import glob
    log_files = glob.glob(log_pattern)
    if log_files:
        latest_log = max(log_files, key=os.path.getmtime)
        shutil.copy2(latest_log, os.path.join(archive_dir, "generation.log"))
        print(f"  ✅ Saved {latest_log}")
        saved_count += 1
    
    # Create README with metadata
    readme_content = f"""# {app_name.title()} Application

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Project**: {project_key}
**Status**: Manually tested and approved ✅

## Files
- `app.py` - Main Streamlit application
- `modules/` - Business logic modules
- `generated_tests/` - Pytest test suite
- `generation.log` - Generation workflow log

## Run
```bash
streamlit run app.py
```

## Test
```bash
python3 -m pytest generated_tests/ -v
```
"""
    
    readme_path = os.path.join(archive_dir, "README.md")
    with open(readme_path, "w") as f:
        f.write(readme_content)
    print(f"  ✅ Created README.md")
    
    print(f"\n✅ Saved {saved_count} items to {archive_dir}")
    print(f"📄 Archive contains: app.py, modules/, tests/, log, README")
    
    return archive_dir

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 save_app.py <project_key> [app_name]")
        print("Example: python3 save_app.py CAL calculator")
        sys.exit(1)
    
    project_key = sys.argv[1]
    app_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    save_app(project_key, app_name)

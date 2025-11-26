#!/usr/bin/env python3
"""
Compare two archived apps to see what changed.
Usage: python3 compare_archives.py 20 22
"""
import sys
import os
import difflib
from pathlib import Path

def get_archive_list():
    """Get list of archived apps."""
    archive_dir = "archive"
    if not os.path.exists(archive_dir):
        return []
    
    archives = [d for d in os.listdir(archive_dir) if os.path.isdir(os.path.join(archive_dir, d))]
    archives.sort(reverse=True)  # Newest first
    return archives

def get_archive_by_mode(mode_num):
    """Get archive name by mode number (20, 21, 22, etc.)."""
    archives = get_archive_list()
    idx = mode_num - 20
    if 0 <= idx < len(archives):
        return archives[idx]
    return None

def read_file_safe(path):
    """Read file content safely."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except:
        return None

def compare_files(file1, file2, label1, label2):
    """Compare two files and show diff."""
    content1 = read_file_safe(file1)
    content2 = read_file_safe(file2)
    
    if content1 is None and content2 is None:
        return f"❌ Both files missing"
    elif content1 is None:
        return f"❌ {label1} missing"
    elif content2 is None:
        return f"❌ {label2} missing"
    
    if content1 == content2:
        return "✅ Identical"
    
    # Generate unified diff
    diff = difflib.unified_diff(
        content1.splitlines(keepends=True),
        content2.splitlines(keepends=True),
        fromfile=label1,
        tofile=label2,
        lineterm=''
    )
    
    return ''.join(diff)

def compare_archives(mode1, mode2):
    """Compare two archived apps."""
    archive1 = get_archive_by_mode(mode1)
    archive2 = get_archive_by_mode(mode2)
    
    if not archive1:
        print(f"❌ Archive mode {mode1} not found")
        return
    
    if not archive2:
        print(f"❌ Archive mode {mode2} not found")
        return
    
    path1 = os.path.join("archive", archive1)
    path2 = os.path.join("archive", archive2)
    
    print(f"\n📊 Comparing Archives:")
    print(f"Mode {mode1}: {archive1}")
    print(f"Mode {mode2}: {archive2}")
    print("=" * 80)
    
    # Compare key files
    files_to_compare = [
        "app.py",
        "modules/calculator.py",
        "README.md"
    ]
    
    for file in files_to_compare:
        file1 = os.path.join(path1, file)
        file2 = os.path.join(path2, file)
        
        print(f"\n📄 {file}")
        print("-" * 80)
        
        result = compare_files(file1, file2, f"{archive1}/{file}", f"{archive2}/{file}")
        
        if result.startswith("✅") or result.startswith("❌"):
            print(result)
        else:
            # Show diff (limit to first 50 lines)
            lines = result.split('\n')
            if len(lines) > 50:
                print('\n'.join(lines[:50]))
                print(f"\n... ({len(lines) - 50} more lines)")
            else:
                print(result)
    
    # Compare module counts
    modules1 = []
    modules2 = []
    
    modules_dir1 = os.path.join(path1, "modules")
    modules_dir2 = os.path.join(path2, "modules")
    
    if os.path.exists(modules_dir1):
        modules1 = [f for f in os.listdir(modules_dir1) if f.endswith('.py') and f != '__init__.py']
    
    if os.path.exists(modules_dir2):
        modules2 = [f for f in os.listdir(modules_dir2) if f.endswith('.py') and f != '__init__.py']
    
    print(f"\n📦 Modules Summary:")
    print(f"Mode {mode1}: {len(modules1)} modules - {', '.join(modules1)}")
    print(f"Mode {mode2}: {len(modules2)} modules - {', '.join(modules2)}")
    
    # Show added/removed modules
    added = set(modules2) - set(modules1)
    removed = set(modules1) - set(modules2)
    
    if added:
        print(f"➕ Added: {', '.join(added)}")
    if removed:
        print(f"➖ Removed: {', '.join(removed)}")

def list_archives():
    """List all available archives."""
    archives = get_archive_list()
    
    if not archives:
        print("❌ No archives found")
        return
    
    print("\n📦 Available Archives:")
    for i, archive in enumerate(archives):
        mode_num = 20 + i
        archive_path = os.path.join("archive", archive)
        app_exists = os.path.exists(os.path.join(archive_path, "app.py"))
        status = "✅" if app_exists else "⚠️"
        print(f"{mode_num}. {status} {archive}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No args - list archives
        list_archives()
        print("\nUsage: python3 compare_archives.py <mode1> <mode2>")
        print("Example: python3 compare_archives.py 20 22")
    elif len(sys.argv) == 3:
        try:
            mode1 = int(sys.argv[1])
            mode2 = int(sys.argv[2])
            compare_archives(mode1, mode2)
        except ValueError:
            print("❌ Invalid mode numbers. Use integers like: 20 22")
    else:
        print("Usage: python3 compare_archives.py <mode1> <mode2>")
        print("Example: python3 compare_archives.py 20 22")

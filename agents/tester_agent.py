# agents/tester_agent.py
import subprocess
import json
import sys
import os

def run_pytest(test_path: str, extra_paths: list | None = None) -> dict:
    """
    Runs pytest on a given test file, with the ability to add temporary paths to sys.path.

    Args:
        test_path (str): The path to the test file to run.
        extra_paths (list, optional): A list of extra directories to add to the Python path. Defaults to None.

    Returns:
        dict: A dictionary containing the test results (passed, failed, collected, output).
    """
    if not os.path.exists(test_path):
        return {"passed": 0, "failed": 1, "collected": 0, "output": f"Test file not found: {test_path}"}

    # This is the critical logic from the old workflow.
    # It temporarily adds directories to the path so that tests can find the generated modules.
    original_path = sys.path[:]
    if extra_paths:
        for path in extra_paths:
            if path not in sys.path:
                sys.path.insert(0, path)
    
    try:
        # Use the -p no:cacheprovider flag to prevent pytest from using stale cache
        command = [sys.executable, "-m", "pytest", test_path, "--json-report", "-p", "no:cacheprovider", "-v"]
        
        # Run from project root so pytest can find modules/ directory
        project_root = os.getcwd()
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            cwd=project_root
        )
    finally:
        # Restore the original path to avoid side effects
        sys.path[:] = original_path

    output = result.stdout + "\n" + result.stderr
    
    try:
        # The .report.json file is created by pytest-json-report in project root
        report_path = os.path.join(os.getcwd(), ".report.json")
        with open(report_path) as f:
            report = json.load(f)
        
        summary = report.get("summary", {})
        passed = summary.get("passed", 0)
        failed = summary.get("failed", 0)
        collected = summary.get("total", 0)
        
        return {"passed": passed, "failed": failed, "collected": collected, "output": output}
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback if json report fails
        passed = output.count(" PASSED")
        failed = output.count(" FAILED")
        collected = passed + failed
        return {"passed": passed, "failed": failed, "collected": collected, "output": output}


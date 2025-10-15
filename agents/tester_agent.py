from typing import Dict, Any, Optional
import subprocess
import json


def run_pytest(path: Optional[str] = None) -> Dict[str, Any]:
    """Run pytest quietly and capture results and output."""
    try:
        cmd = ["python", "-m", "pytest", "-q"]
        if path:
            cmd.append(path)
        proc = subprocess.run(cmd, capture_output=True, text=True)
        output = (proc.stdout or "") + "\n" + (proc.stderr or "")
        # Parse results from pytest output
        passed = failed = 0
        collected = None
        for line in output.splitlines():
            s = line.strip()
            if s.startswith("collected ") and "items" in s:
                try:
                    collected = int(s.split()[1])
                except Exception:
                    pass
            # Handle standard summary lines: '=== 3 passed in ... ===' or '3 passed in ...'
            if (" passed" in s) or (" failed" in s):
                import re
                m = re.search(r"(\d+)\s+passed", s)
                if m:
                    try:
                        passed = int(m.group(1))
                    except Exception:
                        pass
                m = re.search(r"(\d+)\s+failed", s)
                if m:
                    try:
                        failed = int(m.group(1))
                    except Exception:
                        pass
        # If pytest didn't print a 'collected N items' line but we have passes, infer collection
        if collected is None and passed > 0:
            collected = passed
        no_tests = (collected == 0) or ("no tests ran" in output.lower())
        # If non-zero return code or no tests collected, treat as failure
        if proc.returncode != 0 or no_tests:
            if failed == 0 and (proc.returncode != 0 or no_tests):
                failed = 1
        return {"returncode": proc.returncode, "passed": passed, "failed": failed, "collected": collected, "output": output}
    except Exception as e:
        return {"error": str(e)}



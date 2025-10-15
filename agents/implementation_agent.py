from typing import Dict, Any, List
import os
import json


def _to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        try:
            return "\n".join(str(x) for x in content)
        except Exception:
            return json.dumps(content, ensure_ascii=False, indent=2)
    if content is None:
        return ""
    try:
        return str(content)
    except Exception:
        return json.dumps(content, ensure_ascii=False, indent=2)


def write_files(files: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Write a list of files to disk. Each item: {"path": str, "content": str}."""
    written = []
    for f in files:
        path = f.get("path")
        content = _to_text(f.get("content", ""))
        if not path:
            continue
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        written.append(path)
    return {"written": written}



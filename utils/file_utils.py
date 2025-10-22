# utils/file_utils.py
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def load_prompt(file_name: str) -> str:
    """
    Loads a prompt from the prompts directory.

    Args:
        file_name (str): The name of the prompt file.

    Returns:
        str: The content of the prompt file.
    """
    prompt_path = Path("prompts") / file_name
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.warning(f"Prompt file not found: {prompt_path}. Returning empty string.")
        return ""

def read_text_safe(path: str) -> str:
    """Safely reads a text file, returning an empty string if it doesn't exist."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except (FileNotFoundError, TypeError):
        return ""
#!/usr/bin/env python3
"""Validate entire project for errors."""
import os
import sys
from pathlib import Path
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)

def check_required_files(errors: list):
    """Checks for the presence of core project files."""
    logger.info("🔍 Checking for required files...")
    required_files = [ # Updated to reflect new file names
        "main.py", "requirements.txt", "graph/tdd_code.py",
        "graph/create_streamlit_app.py",
        "config/settings.py", ".env",
        "utils/file_utils.py",
        "utils/logging_utils.py"
    ]
    for file in required_files:
        if not Path(file).exists():
            errors.append(f"Missing required file: {file}")
        else:
            logger.info(f"   ✅ Found: {file}")

def check_workspace(warnings: list):
    """Checks the structure of the generated code in the workspace directory."""
    logger.info("\n🔍 Checking workspace directory...")
    workspace_dir = Path("workspace")
    if not workspace_dir.exists():
        warnings.append("Workspace directory not found. Run a generation workflow to create it.")
        return

    logger.info(f"   ✅ Found: {workspace_dir}/")
    # Check for key generated files
    generated_app = workspace_dir / "app.py"
    modules_dir = workspace_dir / "modules"
    tests_dir = workspace_dir / "tests"

    if generated_app.exists():
        logger.info(f"      ✅ Found main application: {generated_app}")
    else:
        warnings.append(f"Main application missing: {generated_app}")

    if modules_dir.exists():
        logger.info(f"      ✅ Found modules directory: {modules_dir}")
    if tests_dir.exists():
        logger.info(f"      ✅ Found tests directory: {tests_dir}")

def check_requirements(errors: list):
    """Validates that core packages are listed in requirements.txt."""
    logger.info("\n🔍 Checking requirements.txt...")
    req_path = Path("requirements.txt")
    if not req_path.exists():
        return # This error is already caught by check_required_files

    with open(req_path, 'r', encoding='utf-8') as f:
        reqs_content = f.read()

    core_packages = ["streamlit", "openai", "langgraph", "pytest", "jira", "langsmith", "python-decouple"]
    missing = [pkg for pkg in core_packages if pkg not in reqs_content]

    if missing:
        errors.append(f"Missing core packages in requirements.txt: {', '.join(missing)}")
    else:
        logger.info("   ✅ All core packages found in requirements.txt")

def check_langsmith_config(errors: list):
    """Validates that LangSmith environment variables are set."""
    logger.info("\n🔍 Validating LangSmith Configuration...")
    langsmith_vars = ["LANGCHAIN_TRACING_V2", "LANGCHAIN_API_KEY", "LANGCHAIN_PROJECT"]
    missing = [var for var in langsmith_vars if not os.getenv(var)]
    if missing:
        for var in missing:
            errors.append(f"Missing LangSmith environment variable in .env: {var}")
    else:
        logger.info("   ✅ LangSmith environment variables found.")

def validate_project():
    """
    Run comprehensive project validation.

    Checks for required files, directory structures, package dependencies,
    and the integrity of generated code files.
    """
    # Load .env file for environment variable checks
    load_dotenv()
    
    errors = []
    warnings = []
    
    logger.info("🚀 Validating Jira_coder project...\n")
    
    check_required_files(errors)
    check_workspace(warnings)
    check_requirements(errors)
    check_langsmith_config(errors)
    
    # 5. Summary
    logger.info("\n" + "="*60)
    logger.info("📋 VALIDATION SUMMARY")
    logger.info("="*60)
    
    if errors:
        logger.error(f"\n❌ ERRORS ({len(errors)}):")
        for err in errors:
            logger.error(f"   - {err}")
    
    if warnings:
        logger.warning(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warn in warnings[:5]:  # Show first 5
            logger.warning(f"   - {warn}")
        if len(warnings) > 5:
            logger.warning(f"   ... and {len(warnings) - 5} more")
    
    if not errors and not warnings:
        logger.info("\n✅ Project validation passed!")
        logger.info("\n🚀 To run the generated unified app:")
        logger.info("   streamlit run workspace/app.py")
    elif not errors:
        logger.warning("\n⚠️  Project has warnings but should work")
        logger.info("\n💡 Regenerate files with warnings using:")
        logger.info("   python main.py")
    else:
        logger.error("\n❌ Project has errors. Fix them before running.")
        return 1
    
    return 0

if __name__ == "__main__":
    # The main function now returns an exit code, which is passed to sys.exit
    # This is a standard pattern for command-line scripts.
    exit_code = validate_project()
    sys.exit(exit_code)

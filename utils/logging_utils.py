# utils/logging_utils.py
import logging
import os
from datetime import datetime

def setup_logging(log_prefix: str, identifier: str = None):
    """
    Sets up logging for the application, creating a timestamped log file
    and configuring console output.

    Args:
        log_prefix (str): Prefix for the log file name (e.g., "unified", "generation").
        identifier (str, optional): An identifier (e.g., issue_key, project_key)
                                    to include in the log file name. Defaults to None.
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log_file_name = f"{log_prefix}_{identifier}_{timestamp}.log" if identifier else f"{log_prefix}_{timestamp}.log"
    log_file = os.path.join(log_dir, log_file_name)
    
    # Clear existing handlers to prevent duplicate logs if called multiple times
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_file), logging.StreamHandler()])
    logger = logging.getLogger(__name__)
    logger.info(f"Logging to: {log_file}")
    print(f"📝 Logging to: {log_file}")
    return logger, log_file
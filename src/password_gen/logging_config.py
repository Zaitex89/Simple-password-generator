import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Create a folder named "logs" in the project root if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

def setup_logging():
    """
    This function configures the gloabl logging settings
    - A file logger 
    - A console logger for terminal output
    """

    # Format : 2025-04-29 14:10:15 | INFO | src.main | main.py:10 | Application started
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s"        
    )

    # File handler = writes logs to logs/app.log
    #RotatingFileHandler means 
    #when reaching over 5 MB -> create a new file, keep only the last 5 files

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8"
    )

    # Console handler = prints logs to the terminal
    console_handler = logging.StreamHandler()

    # Apply the same format to both handlers 
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Config the root logger
    # All loggers in the project inherit this config

    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler] # Where logs go
    )
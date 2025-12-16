"""
Custom logging configuration module.
Handles different levels of logs with file and console output.
"""
import logging
import sys
from pathlib import Path


def get_log_directory() -> Path:
    """
    Get or create the logs directory.
    
    Returns:
        Path to logs directory
    """
    # Get the project root (3 levels up from this file)
    project_root = Path(__file__).resolve().parent.parent.parent
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    return logs_dir


def setup_logging(
    log_level: str = "INFO",
    log_file: str = "password_gen.log",
    console_output: bool = True
) -> logging.Logger:
    """
    Setup logging configuration with file and console handlers.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Name of log file
        console_output: Whether to output to console
        
    Returns:
        Configured logger instance
    """
    # Get logs directory
    logs_dir = get_log_directory()
    log_path = logs_dir / log_file
    
    # Create logger
    logger = logging.getLogger("password_gen")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # File handler (detailed logs)
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler (simpler logs)
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)
    
    # Add handlers
    logger.addHandler(file_handler)
    
    # Log startup
    logger.info("="*60)
    logger.info(f"Logging initialized - Log file: {log_path}")
    logger.info("="*60)
    
    return logger


def get_logger(name: str = "password_gen") -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
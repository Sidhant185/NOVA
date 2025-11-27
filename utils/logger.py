"""
Logging configuration for NOVA Assistant.
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from config import Config

def setup_logging():
    """Setup logging configuration."""
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Configure logging level
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # File handler with rotation
    if Config.LOG_TO_FILE:
        file_handler = RotatingFileHandler(
            'logs/nova.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    if Config.LOG_TO_FILE:
        root_logger.addHandler(file_handler)
    
    return root_logger


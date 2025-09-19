"""Logging configuration and utilities."""

import logging
import sys
from typing import Optional
from app.config import settings

def setup_logging() -> None:
    """Setup application logging configuration."""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name or __name__)

# Initialize logging on module import
setup_logging()
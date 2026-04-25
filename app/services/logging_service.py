"""
Logging service for the AI-Powered Talent Scouting Agent.
Provides structured logging for tracking operations and debugging.
"""
import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional


class LoggingService:
    """Service for application logging."""
    
    def __init__(self, log_file: str = "talent_scout.log"):
        """Initialize the logging service."""
        self.log_file = log_file
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up the logger with appropriate handlers."""
        logger = logging.getLogger("talent_scout")
        logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def log_info(self, message: str):
        """Log an info message."""
        self.logger.info(message)
    
    def log_warning(self, message: str):
        """Log a warning message."""
        self.logger.warning(message)
    
    def log_error(self, message: str):
        """Log an error message."""
        self.logger.error(message)
    
    def log_operation(self, operation: str, details: Optional[Dict[str, Any]] = None):
        """Log a business operation with details."""
        if details:
            details_str = ", ".join([f"{k}={v}" for k, v in details.items()])
            message = f"Operation: {operation} | Details: {details_str}"
        else:
            message = f"Operation: {operation}"
        
        self.logger.info(message)
    
    def log_candidate_matching(self, candidate_id: str, score: float, 
                              explanation: str = ""):
        """Log candidate matching results."""
        message = f"Candidate Match - ID: {candidate_id}, Score: {score}"
        if explanation:
            message += f", Explanation: {explanation}"
        
        self.logger.info(message)
    
    def log_api_call(self, endpoint: str, method: str, status_code: int):
        """Log API calls."""
        message = f"API Call - Endpoint: {endpoint}, Method: {method}, Status: {status_code}"
        self.logger.info(message)
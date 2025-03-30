"""
Utility Helpers Module

This module provides utility functions for the quantum secure messenger.
It includes functions for message formatting, file handling, logging,
and other common operations.

Functions:
    format_message(): Formats messages for display
    validate_file(): Validates file uploads
    log_event(): Logs system events
    generate_timestamp(): Generates formatted timestamps
    sanitize_input(): Sanitizes user input
    format_file_size(): Formats file sizes for display
    validate_quantum_key(): Validates quantum keys
    generate_session_id(): Generates unique session IDs

Dependencies:
    - datetime
    - os
    - logging
    - typing
"""

from datetime import datetime
import os
import logging
from typing import Dict, Any, Optional, List
import re
import uuid
import magic
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Allowed file types
ALLOWED_EXTENSIONS = {
    'images': {'png', 'jpg', 'jpeg', 'gif'},
    'documents': {'pdf', 'doc', 'docx', 'txt'},
    'audio': {'mp3', 'wav', 'ogg'},
    'video': {'mp4', 'avi', 'mov'}
}

def format_message(message: str, max_length: int = 1000) -> str:
    """
    Formats a message for display in the chat interface.
    
    Args:
        message (str): The message to format
        max_length (int): Maximum length of the message
    
    Returns:
        str: The formatted message
    
    Raises:
        Exception: If formatting fails
    """
    try:
        # Truncate if too long
        if len(message) > max_length:
            message = message[:max_length] + "..."
        
        # Escape HTML characters
        message = message.replace('&', '&amp;')
        message = message.replace('<', '&lt;')
        message = message.replace('>', '&gt;')
        
        # Convert URLs to links
        message = re.sub(
            r'(https?://\S+)',
            r'<a href="\1" target="_blank">\1</a>',
            message
        )
        
        return message
    except Exception as e:
        logger.error(f"Error formatting message: {str(e)}")
        return message

def validate_file(file_path: str, max_size: int = 10 * 1024 * 1024) -> Tuple[bool, str]:
    """
    Validates a file for upload.
    
    Args:
        file_path (str): Path to the file
        max_size (int): Maximum allowed file size in bytes
    
    Returns:
        Tuple[bool, str]: A tuple containing:
            - True if file is valid, False otherwise
            - Error message if invalid
    """
    try:
        # Check file exists
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > max_size:
            return False, f"File too large (max {max_size/1024/1024}MB)"
        
        # Check file type
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        
        # Validate file type
        if not any(file_type.startswith(ft) for ft in ['image/', 'application/', 'audio/', 'video/']):
            return False, "Invalid file type"
        
        return True, ""
    except Exception as e:
        logger.error(f"Error validating file: {str(e)}")
        return False, str(e)

def log_event(event_type: str, details: Dict[str, Any]) -> None:
    """
    Logs a system event.
    
    Args:
        event_type (str): Type of event to log
        details (Dict[str, Any]): Event details
    
    Raises:
        Exception: If logging fails
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {event_type}: {details}"
        logger.info(log_message)
    except Exception as e:
        logger.error(f"Error logging event: {str(e)}")

def generate_timestamp() -> str:
    """
    Generates a formatted timestamp.
    
    Returns:
        str: The formatted timestamp
    """
    try:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logger.error(f"Error generating timestamp: {str(e)}")
        return ""

def sanitize_input(input_str: str) -> str:
    """
    Sanitizes user input to prevent XSS and injection attacks.
    
    Args:
        input_str (str): The input to sanitize
    
    Returns:
        str: The sanitized input
    """
    try:
        # Remove HTML tags
        input_str = re.sub(r'<[^>]+>', '', input_str)
        
        # Escape special characters
        input_str = input_str.replace('&', '&amp;')
        input_str = input_str.replace('<', '&lt;')
        input_str = input_str.replace('>', '&gt;')
        input_str = input_str.replace('"', '&quot;')
        input_str = input_str.replace("'", '&#x27;')
        
        return input_str
    except Exception as e:
        logger.error(f"Error sanitizing input: {str(e)}")
        return input_str

def format_file_size(size_bytes: int) -> str:
    """
    Formats a file size in bytes to human-readable format.
    
    Args:
        size_bytes (int): File size in bytes
    
    Returns:
        str: Formatted file size
    """
    try:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"
    except Exception as e:
        logger.error(f"Error formatting file size: {str(e)}")
        return "0 B"

def validate_quantum_key(key: str) -> bool:
    """
    Validates a quantum key.
    
    Args:
        key (str): The quantum key to validate
    
    Returns:
        bool: True if key is valid, False otherwise
    """
    try:
        # Check key length
        if len(key) != 32:
            return False
        
        # Check key format (binary string)
        if not all(bit in '01' for bit in key):
            return False
        
        return True
    except Exception as e:
        logger.error(f"Error validating quantum key: {str(e)}")
        return False

def generate_session_id() -> str:
    """
    Generates a unique session ID.
    
    Returns:
        str: The generated session ID
    """
    try:
        return str(uuid.uuid4())
    except Exception as e:
        logger.error(f"Error generating session ID: {str(e)}")
        return ""

def get_file_extension(file_path: str) -> str:
    """
    Gets the file extension from a file path.
    
    Args:
        file_path (str): Path to the file
    
    Returns:
        str: The file extension
    """
    try:
        return Path(file_path).suffix.lower()[1:]
    except Exception as e:
        logger.error(f"Error getting file extension: {str(e)}")
        return ""

def is_allowed_file_type(file_path: str) -> bool:
    """
    Checks if a file type is allowed.
    
    Args:
        file_path (str): Path to the file
    
    Returns:
        bool: True if file type is allowed, False otherwise
    """
    try:
        extension = get_file_extension(file_path)
        return any(extension in types for types in ALLOWED_EXTENSIONS.values())
    except Exception as e:
        logger.error(f"Error checking file type: {str(e)}")
        return False

def create_directory_if_not_exists(directory: str) -> bool:
    """
    Creates a directory if it doesn't exist.
    
    Args:
        directory (str): Path to the directory
    
    Returns:
        bool: True if directory exists or was created, False otherwise
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory: {str(e)}")
        return False

def get_file_mime_type(file_path: str) -> str:
    """
    Gets the MIME type of a file.
    
    Args:
        file_path (str): Path to the file
    
    Returns:
        str: The MIME type of the file
    """
    try:
        mime = magic.Magic(mime=True)
        return mime.from_file(file_path)
    except Exception as e:
        logger.error(f"Error getting MIME type: {str(e)}")
        return "" 
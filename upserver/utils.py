"""
Utility functions for the upserver package.
"""

import os
import shutil
import platform
from pathlib import Path


def sanitize_filename(filename):
    """
    Sanitize a filename by removing quotes and preventing path traversal.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove spaces, quotes and any directory components
    return os.path.basename(filename.strip().strip("'\""))


def get_disk_space(path):
    """
    Get disk space information in a cross-platform way.
    Works on both Windows and Linux.
    
    Args:
        path (str): Path to check disk space for
        
    Returns:
        tuple: (total_gb, used_gb, free_gb)
    """
    try:
        # Using shutil.disk_usage which works on both Windows and Linux
        total, used, free = shutil.disk_usage(path)
        
        # Convert to GB
        total_gb = total / (1024 ** 3)
        used_gb = used / (1024 ** 3)  
        free_gb = free / (1024 ** 3)
        
        return total_gb, used_gb, free_gb
        
    except Exception as e:
        print(f"⚠️  Error getting disk space information: {e}")
        # Default values in case of error
        return 0.0, 0.0, 0.0


def format_file_size(size_bytes):
    """
    Format file size in human readable format.
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"


def ensure_directory_exists(directory):
    """
    Ensure that a directory exists, create if it doesn't.
    
    Args:
        directory (str or Path): Directory path
        
    Returns:
        Path: Path object for the directory
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_system_info():
    """
    Get system information for logging purposes.
    
    Returns:
        dict: System information
    """
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version()
    }
"""
upserver - A file server for uploading and downloading files.

This package provides a simple and efficient way to set up a file server
that supports both file uploads and downloads.
"""

__version__ = "0.1.0"
__author__ = "Álex Vieira"
__license__ = "MIT"

from .server import FileServer

__all__ = ["FileServer"]

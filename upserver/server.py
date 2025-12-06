"""
Main server module for file upload and download functionality.
"""

import os
from pathlib import Path


class FileServer:
    """
    A file server that handles uploading and downloading of files.
    
    Attributes:
        upload_dir (Path): Directory where uploaded files are stored
        host (str): Server host address
        port (int): Server port number
    """
    
    def __init__(self, upload_dir="uploads", host="0.0.0.0", port=8000):
        """
        Initialize the file server.
        
        Args:
            upload_dir (str): Directory to store uploaded files
            host (str): Host address to bind the server
            port (int): Port number to bind the server
        """
        self.upload_dir = Path(upload_dir)
        self.host = host
        self.port = port
        
        # Create upload directory if it doesn't exist
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def start(self):
        """
        Start the file server.
        
        This is a placeholder method. The actual server implementation
        will be added in a future update. Currently, it only prints
        startup information.
        
        TODO: Implement actual server logic with HTTP endpoints for
        file upload and download operations.
        """
        print(f"File server starting on {self.host}:{self.port}")
        print(f"Upload directory: {self.upload_dir.absolute()}")
        print("Note: This is a placeholder. Server implementation coming soon.")
        # TODO: Implement actual server logic
    
    def upload_file(self, file_data, filename):
        """
        Upload a file to the server.
        
        Args:
            file_data (bytes): File content as bytes
            filename (str): Name of the file to save
            
        Returns:
            Path: Path to the saved file
        """
        # Prevent path traversal attacks by using only the filename component
        safe_filename = Path(filename).name
        file_path = self.upload_dir / safe_filename
        with open(file_path, 'wb') as f:
            f.write(file_data)
        return file_path
    
    def download_file(self, filename):
        """
        Download a file from the server.
        
        Args:
            filename (str): Name of the file to download
            
        Returns:
            bytes: File content as bytes
            
        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        # Prevent path traversal attacks by using only the filename component
        safe_filename = Path(filename).name
        file_path = self.upload_dir / safe_filename
        if not file_path.exists():
            raise FileNotFoundError(f"File '{filename}' not found")
        
        with open(file_path, 'rb') as f:
            return f.read()
    
    def list_files(self):
        """
        List all files in the upload directory.
        
        Returns:
            list: List of filenames
        """
        return [f.name for f in self.upload_dir.iterdir() if f.is_file()]

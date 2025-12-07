"""
Tests for the FileServer class and related functionality.
"""

import pytest
import tempfile
import shutil
import threading
import time
from pathlib import Path
from upserver.server import FileServer
from upserver.config import ServerConfig
from upserver.utils import sanitize_filename, get_disk_space, format_file_size


class TestFileServer:
    """Test cases for FileServer class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)
    
    def test_initialization(self, temp_dir):
        """Test FileServer initialization with new parameters."""
        server = FileServer(
            upload_dir=temp_dir, 
            host="127.0.0.1", 
            port=9000,
            chunk_size=1024*1024
        )
        assert server.host == "127.0.0.1"
        assert server.port == 9000
        assert server.upload_dir == Path(temp_dir)
        assert server.temp_dir == Path(temp_dir) / "temp"
        assert server.chunk_size == 1024*1024
        assert server.upload_dir.exists()
        assert server.temp_dir.exists()
    
    def test_legacy_upload_file(self, temp_dir):
        """Test legacy file upload functionality."""
        server = FileServer(upload_dir=temp_dir)
        test_data = b"Hello, World!"
        filename = "test.txt"
        
        result = server.upload_file(test_data, filename)
        
        assert result.exists()
        assert result.name == filename
        with open(result, 'rb') as f:
            assert f.read() == test_data
    
    def test_legacy_download_file(self, temp_dir):
        """Test legacy file download functionality."""
        server = FileServer(upload_dir=temp_dir)
        test_data = b"Test content"
        filename = "download_test.txt"
        
        # Upload a file first
        server.upload_file(test_data, filename)
        
        # Download the file
        downloaded_data = server.download_file(filename)
        assert downloaded_data == test_data
    
    def test_list_files(self, temp_dir):
        """Test file listing functionality."""
        server = FileServer(upload_dir=temp_dir)
        
        # Upload multiple files
        files = [("file1.txt", b"Content 1"), ("file2.txt", b"Content 2")]
        for filename, content in files:
            server.upload_file(content, filename)
        
        # List files
        file_list = server.list_files()
        assert len(file_list) == 2
        assert "file1.txt" in file_list
        assert "file2.txt" in file_list
    
    def test_server_startup_info(self, temp_dir, capsys):
        """Test server startup information display."""
        server = FileServer(upload_dir=temp_dir, host="localhost", port=8080)
        
        # Call the private method to test startup info
        server._print_startup_info()
        
        captured = capsys.readouterr()
        assert "RESUMABLE HTTP FILE SERVER" in captured.out
        assert "localhost:8080" in captured.out
        assert str(temp_dir) in captured.out


class TestServerConfig:
    """Test cases for ServerConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ServerConfig()
        assert config.host == "0.0.0.0"
        assert config.port == 8000
        assert config.upload_dir == "uploads"
        assert config.chunk_size == 5 * 1024 * 1024
        assert config.max_file_size == 0
        assert config.enable_logging == True
        assert config.cors_enabled == True
        assert config.allowed_origins == ["*"]
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = ServerConfig(
            host="127.0.0.1",
            port=9000,
            upload_dir="custom_uploads",
            chunk_size=10 * 1024 * 1024,
            max_file_size=1024 * 1024 * 1024
        )
        assert config.host == "127.0.0.1"
        assert config.port == 9000
        assert config.upload_dir == "custom_uploads"
        assert config.chunk_size == 10 * 1024 * 1024
        assert config.max_file_size == 1024 * 1024 * 1024
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Valid config
        valid_config = ServerConfig(port=8080, chunk_size=1024)
        assert valid_config.validate() == True
        
        # Invalid port
        invalid_port_config = ServerConfig(port=70000)
        assert invalid_port_config.validate() == False
        
        # Invalid chunk size
        invalid_chunk_config = ServerConfig(chunk_size=512)
        assert invalid_chunk_config.validate() == False
        
        # Invalid max file size
        invalid_size_config = ServerConfig(max_file_size=-1)
        assert invalid_size_config.validate() == False
    
    def test_config_save_load(self, tmp_path):
        """Test configuration save and load functionality."""
        config_file = tmp_path / "test_config.json"
        
        # Create and save config
        original_config = ServerConfig(
            host="192.168.1.1",
            port=9999,
            upload_dir="test_uploads"
        )
        original_config.save_to_file(str(config_file))
        
        # Load config
        loaded_config = ServerConfig.load_from_file(str(config_file))
        
        assert loaded_config.host == original_config.host
        assert loaded_config.port == original_config.port
        assert loaded_config.upload_dir == original_config.upload_dir


class TestUtils:
    """Test cases for utility functions."""
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        # Normal filename
        assert sanitize_filename("test.txt") == "test.txt"
        
        # Filename with quotes
        assert sanitize_filename('"test.txt"') == "test.txt"
        assert sanitize_filename("'test.txt'") == "test.txt"
        
        # Filename with path traversal attempt
        assert sanitize_filename("../../../etc/passwd") == "passwd"
        assert sanitize_filename("/etc/passwd") == "passwd"
        assert sanitize_filename("C:\\Windows\\system32\\file.txt") == "file.txt"
        
        # Filename with spaces
        assert sanitize_filename("  test file.txt  ") == "test file.txt"
    
    def test_format_file_size(self):
        """Test file size formatting."""
        assert format_file_size(0) == "0 B"
        assert format_file_size(1024) == "1.00 KB"
        assert format_file_size(1024 * 1024) == "1.00 MB"
        assert format_file_size(1024 * 1024 * 1024) == "1.00 GB"
        assert format_file_size(1536) == "1.50 KB"  # 1.5 KB
    
    def test_get_disk_space(self, tmp_path):
        """Test disk space information retrieval."""
        total, used, free = get_disk_space(str(tmp_path))
        
        # Should return valid numbers
        assert isinstance(total, float)
        assert isinstance(used, float)
        assert isinstance(free, float)
        
        # Basic sanity checks
        assert total >= 0
        assert used >= 0
        assert free >= 0
        assert total >= used  # Total should be >= used
        
        # Download it
        downloaded_data = server.download_file(filename)
        assert downloaded_data == test_data
    
    def test_download_nonexistent_file(self, temp_dir):
        """Test downloading a file that doesn't exist."""
        server = FileServer(upload_dir=temp_dir)
        
        with pytest.raises(FileNotFoundError):
            server.download_file("nonexistent.txt")
    
    def test_list_files(self, temp_dir):
        """Test listing files in upload directory."""
        server = FileServer(upload_dir=temp_dir)
        
        # Initially empty
        assert server.list_files() == []
        
        # Upload some files
        server.upload_file(b"data1", "file1.txt")
        server.upload_file(b"data2", "file2.txt")
        
        files = server.list_files()
        assert len(files) == 2
        assert "file1.txt" in files
        assert "file2.txt" in files
    
    def test_upload_directory_creation(self):
        """Test that upload directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            upload_path = Path(temp_dir) / "new_uploads"
            assert not upload_path.exists()
            
            server = FileServer(upload_dir=str(upload_path))
            assert upload_path.exists()
    
    def test_path_traversal_protection_upload(self, temp_dir):
        """Test that path traversal attacks are prevented in upload."""
        server = FileServer(upload_dir=temp_dir)
        test_data = b"malicious content"
        
        # Try to upload with path traversal
        result = server.upload_file(test_data, "../../../malicious.txt")
        
        # File should be saved in the upload directory, not outside
        assert result.parent == Path(temp_dir)
        assert result.name == "malicious.txt"
    
    def test_path_traversal_protection_download(self, temp_dir):
        """Test that path traversal attacks are prevented in download."""
        server = FileServer(upload_dir=temp_dir)
        test_data = b"safe content"
        
        # Upload a legitimate file
        server.upload_file(test_data, "safe.txt")
        
        # Try to download with path traversal
        # Should look for "etc/passwd" as a filename, not as a path
        with pytest.raises(FileNotFoundError):
            server.download_file("../../../etc/passwd")


class TestTemplates:
    """Test cases for HTML templates."""
    
    def test_upload_page_html(self):
        """Test upload page HTML generation."""
        from upserver.templates import get_upload_page_html
        
        html = get_upload_page_html()
        
        # Check for essential HTML elements
        assert "<!DOCTYPE html>" in html
        assert "<html>" in html
        assert "Upload Resumable" in html
        assert "startUpload" in html  # JavaScript function
        assert "showFileList" in html  # JavaScript function
        assert "progress-container" in html  # CSS class
    
    def test_css_styles(self):
        """Test CSS styles generation."""
        from upserver.templates import get_css_styles
        
        css = get_css_styles()
        
        # Check for essential CSS classes
        assert ".container" in css
        assert ".upload-box" in css
        assert ".progress-bar" in css
        assert "linear-gradient" in css  # Should have gradients
    
    def test_javascript_code(self):
        """Test JavaScript code generation."""
        from upserver.templates import get_javascript_code
        
        js = get_javascript_code()
        
        # Check for essential JavaScript functions
        assert "function addLog" in js
        assert "function startUpload" in js
        assert "function showFileList" in js
        assert "async function startUpload" in js
        assert "FormData" in js  # Should use FormData for uploads


class TestIntegration:
    """Integration tests for the complete system."""
    
    @pytest.fixture
    def server_config(self, tmp_path):
        """Create a test server configuration."""
        return {
            "upload_dir": str(tmp_path / "uploads"),
            "host": "127.0.0.1", 
            "port": 0,  # Let OS choose port
            "chunk_size": 1024 * 1024  # 1MB for testing
        }
    
    def test_server_creation_and_config(self, server_config):
        """Test server creation with various configurations."""
        server = FileServer(**server_config)
        
        assert server.host == server_config["host"]
        assert str(server.upload_dir) == server_config["upload_dir"]
        assert server.chunk_size == server_config["chunk_size"]
        
        # Directories should be created
        assert server.upload_dir.exists()
        assert server.temp_dir.exists()
    
    def test_configuration_precedence(self):
        """Test configuration precedence (CLI > config file > env > defaults)."""
        from upserver.config import ServerConfig
        
        # Test default values
        default_config = ServerConfig()
        assert default_config.port == 8000
        
        # Test custom values override defaults
        custom_config = ServerConfig(port=9999)
        assert custom_config.port == 9999
        
        # Test validation catches invalid values
        invalid_config = ServerConfig(port=99999)
        assert not invalid_config.validate()
    
    def test_error_handling(self, tmp_path):
        """Test error handling in various scenarios."""
        server = FileServer(upload_dir=str(tmp_path / "uploads"))
        
        # Test downloading non-existent file
        with pytest.raises(FileNotFoundError):
            server.download_file("nonexistent.txt")
        
        # Test sanitization prevents path traversal
        safe_name = sanitize_filename("../../../etc/passwd")
        assert safe_name == "passwd"
        assert "/" not in safe_name
        assert ".." not in safe_name


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# upserver

A Python file server for uploading and downloading files.

## Description

`upserver` is a simple and efficient file server package that provides functionality for uploading, downloading, and managing files on a server. It's designed to be easy to use and integrate into your Python projects.

## Installation

You can install `upserver` using pip:

```bash
pip install upserver
```

Or install from source:

```bash
git clone https://github.com/eiAlex/upserver.git
cd upserver
pip install -e .
```

## Usage

### As a Command-Line Tool

After installation, you can run the server directly from the command line:

```bash
upserver
```

With custom options:

```bash
upserver --host 127.0.0.1 --port 8080 --upload-dir /path/to/uploads
```

### Command-Line Options

- `--host`: Host address to bind the server (default: 0.0.0.0)
- `--port`: Port number to bind the server (default: 8000)
- `--upload-dir`: Directory to store uploaded files (default: uploads)
- `--version`: Show the version number

### As a Python Module

You can also use `upserver` as a module in your Python code:

```python
from upserver import FileServer

# Create a file server instance
server = FileServer(upload_dir="my_uploads", host="0.0.0.0", port=8000)

# Start the server
server.start()

# Upload a file
with open("example.txt", "rb") as f:
    file_data = f.read()
server.upload_file(file_data, "example.txt")

# List files
files = server.list_files()
print(files)

# Download a file
content = server.download_file("example.txt")
```

### Running as a Module

You can also run upserver as a Python module:

```bash
python -m upserver
```

## Features

- **File Upload**: Upload files to a specified directory
- **File Download**: Download files from the server
- **File Listing**: List all available files
- **Command-Line Interface**: Easy-to-use CLI for running the server
- **Configurable**: Customize host, port, and upload directory

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/eiAlex/upserver.git
cd upserver

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black upserver/
```

### Type Checking

```bash
mypy upserver/
```

## Requirements

- Python >= 3.7

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Álex Vieira

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any problems or have suggestions, please open an issue on the [GitHub repository](https://github.com/eiAlex/upserver/issues).
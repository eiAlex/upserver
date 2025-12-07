# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2024-12-07

### 🚀 Major Features Added

- **Resumable chunked file uploads**: Complete rewrite to support chunked uploads with automatic resume capability
- **Web interface**: Beautiful, responsive web UI for file management with real-time progress tracking
- **Pause/Resume functionality**: Users can manually pause and resume uploads
- **Cross-platform compatibility**: Enhanced support for Windows, Linux, and macOS

### ✨ New Features

- **Advanced configuration system**: JSON config files, environment variables, and CLI arguments
- **Professional logging**: Configurable logging with file output and colored console output
- **Real-time progress tracking**: Live upload progress with speed metrics and time estimates
- **File management interface**: Web-based file listing and download functionality
- **Security enhancements**: Improved filename sanitization and path traversal protection
- **CORS support**: Configurable cross-origin resource sharing
- **Disk space monitoring**: Real-time disk space information display
- **System information**: Detailed system and environment information logging

### 🏗️ Architecture Changes

- **Modular structure**: Split code into logical modules (handlers, utils, config, templates)
- **Separated concerns**: HTML templates extracted to separate module
- **Enhanced CLI**: Rich command-line interface with comprehensive options
- **Configuration management**: Centralized configuration with validation
- **Logging framework**: Professional logging system with multiple output options

### 📊 Technical Improvements

- **HTTP handlers**: Custom HTTP request handlers for resumable uploads
- **Chunk management**: Efficient handling of large file chunks (default: 5MB)
- **Temporary file handling**: Safe temporary file management during uploads
- **Error handling**: Comprehensive error handling and recovery
- **Performance optimization**: Optimized for large file transfers
- **Memory efficiency**: Reduced memory usage for large file operations

### 🔧 Configuration Options

- **Server settings**: Host, port, upload directory configuration
- **Upload parameters**: Configurable chunk size and maximum file size
- **Logging options**: Log level, file output, colored output controls
- **Security settings**: CORS configuration and allowed origins
- **Performance tuning**: Chunk size and buffer size optimization

### 📚 Documentation

- **Comprehensive README**: Updated with detailed usage examples and features
- **Contributing guide**: Complete guide for community contributions
- **API documentation**: Detailed API endpoint documentation
- **Configuration examples**: Sample configuration files and usage patterns

### 🧪 Testing

- **Comprehensive test suite**: Tests for all major components
- **Unit tests**: Individual component testing
- **Integration tests**: Full system integration testing
- **Configuration testing**: Configuration validation and loading tests
- **Utility testing**: Helper function and utility testing

### 🛠️ Developer Experience

- **Type hints**: Added type annotations throughout codebase
- **Code formatting**: Black code formatting compliance
- **Documentation strings**: Comprehensive docstrings for all public APIs
- **Error messages**: Improved error messages and debugging information
- **Development tools**: Enhanced development and debugging tools

### 🔄 Migration from 0.1.0

The 0.2.0 version maintains backward compatibility for basic usage:

```python
# This still works
from upserver import FileServer
server = FileServer(upload_dir="uploads", host="0.0.0.0", port=8000)
server.start()
```

New features are opt-in and don't break existing code.

### ⚠️ Breaking Changes

- **Python version requirement**: Now requires Python 3.8+ (was 3.7+)
- **Package structure**: Internal module organization changed (affects direct imports)
- **CLI behavior**: Server now shows more detailed startup information
- **Configuration**: Some advanced configuration options have new names

### 🐛 Bug Fixes

- Fixed file path handling on Windows systems
- Improved error handling for disk space issues
- Fixed potential memory leaks with large file uploads
- Enhanced filename sanitization for various edge cases
- Fixed CORS headers for browser compatibility

### 🔒 Security Improvements

- Enhanced path traversal protection
- Improved filename sanitization
- Better handling of malicious filenames
- Secure temporary file management
- Input validation for all parameters

## [0.1.0] - 2024-XX-XX

### Added
- Initial release with basic file server functionality
- Simple file upload and download capabilities
- Command-line interface
- Basic configuration options
- File listing functionality

---

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information about contributing to this project.

## Support

If you encounter any issues or have questions, please:

1. Check the [documentation](README.md)
2. Search [existing issues](https://github.com/eiAlex/upserver/issues)
3. Create a [new issue](https://github.com/eiAlex/upserver/issues/new) if needed
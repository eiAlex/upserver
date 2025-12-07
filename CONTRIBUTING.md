# Contributing to upserver

Thank you for your interest in contributing to upserver! We welcome contributions from the community and are grateful for any help you can provide.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Code Style](#code-style)
- [Project Structure](#project-structure)
- [Feature Requests](#feature-requests)
- [Bug Reports](#bug-reports)

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct. Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/upserver.git
   cd upserver
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/eiAlex/upserver.git
   ```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the package in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

3. Verify the installation:
   ```bash
   upserver --version
   ```

### Project Structure

```
upserver/
├── upserver/              # Main package directory
│   ├── __init__.py       # Package initialization
│   ├── server.py         # Main FileServer class
│   ├── handlers.py       # HTTP request handlers
│   ├── cli.py            # Command-line interface
│   ├── config.py         # Configuration management
│   ├── logging_config.py # Logging setup
│   ├── utils.py          # Utility functions
│   └── templates.py      # HTML templates
├── tests/                # Test files
├── docs/                 # Documentation (if any)
├── README.md             # Project README
├── CONTRIBUTING.md       # This file
├── LICENSE               # License information
├── pyproject.toml        # Project configuration
└── requirements.txt      # Dependencies
```

## Making Changes

### Creating a Branch

Always create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### Branch Naming Convention

- `feature/description` - for new features
- `fix/description` - for bug fixes  
- `docs/description` - for documentation changes
- `refactor/description` - for code refactoring
- `test/description` - for adding tests

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=upserver

# Run specific test file
pytest tests/test_server.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Place test files in the `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test function names
- Include both positive and negative test cases
- Test edge cases and error conditions

Example test structure:
```python
def test_file_upload_success():
    """Test successful file upload."""
    # Arrange
    server = FileServer()
    
    # Act
    result = server.upload_file(b"test content", "test.txt")
    
    # Assert
    assert result.exists()
```

## Code Style

### Python Style Guide

We follow PEP 8 with some modifications. Use the following tools:

```bash
# Code formatting
black upserver/

# Import sorting
isort upserver/

# Linting
flake8 upserver/

# Type checking
mypy upserver/
```

### Code Quality Standards

- Write clear, readable code with meaningful variable names
- Add docstrings for all public functions and classes
- Use type hints where appropriate
- Keep functions small and focused
- Comment complex logic
- Follow existing code patterns

### Example Code Style

```python
def upload_file(self, file_data: bytes, filename: str) -> Path:
    """
    Upload a file to the server.
    
    Args:
        file_data (bytes): File content as bytes
        filename (str): Name of the file to save
        
    Returns:
        Path: Path to the saved file
        
    Raises:
        ValueError: If filename is invalid
        OSError: If file cannot be written
    """
    safe_filename = sanitize_filename(filename)
    if not safe_filename:
        raise ValueError("Invalid filename")
    
    file_path = self.upload_dir / safe_filename
    
    try:
        with open(file_path, 'wb') as f:
            f.write(file_data)
    except OSError as e:
        self.logger.error(f"Failed to write file: {e}")
        raise
    
    return file_path
```

## Submitting Changes

### Pull Request Process

1. Ensure your code follows the style guidelines
2. Add or update tests for your changes
3. Update documentation if needed
4. Ensure all tests pass
5. Update the CHANGELOG.md if applicable

### Pull Request Template

When submitting a pull request, please include:

- **Description**: Clear description of what the PR does
- **Type**: Feature, bug fix, documentation, etc.
- **Testing**: How you tested the changes
- **Breaking Changes**: Any breaking changes and migration path
- **Related Issues**: Link to any related issues

### Commit Message Format

Use clear, descriptive commit messages:

```
type(scope): description

- feat: add new feature
- fix: bug fix
- docs: documentation changes
- style: formatting changes
- refactor: code refactoring
- test: adding tests
- chore: maintenance tasks

Examples:
feat(server): add chunked upload support
fix(cli): handle invalid port numbers
docs(readme): update installation instructions
```

## Feature Requests

### Suggesting New Features

1. Check existing issues to avoid duplicates
2. Open a new issue with the "feature request" label
3. Provide detailed description of the feature
4. Explain the use case and benefits
5. Consider implementation approach

### Feature Development Process

1. Discuss the feature in an issue first
2. Get approval from maintainers
3. Create a design document for complex features
4. Implement the feature following contribution guidelines
5. Submit PR with comprehensive tests

## Bug Reports

### Creating Good Bug Reports

Include the following information:

- **Environment**: OS, Python version, upserver version
- **Steps to Reproduce**: Exact steps to trigger the bug
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Logs**: Relevant log output or error messages
- **Code Sample**: Minimal code that reproduces the issue

### Bug Report Template

```markdown
**Environment:**
- OS: [e.g., Windows 10, Ubuntu 20.04]
- Python: [e.g., 3.9.2]
- upserver: [e.g., 0.2.0]

**Steps to Reproduce:**
1. Start server with `upserver --port 8080`
2. Upload a file larger than 1GB
3. Observe the error

**Expected Behavior:**
File should upload successfully with progress indication.

**Actual Behavior:**
Server crashes with memory error.

**Logs:**
```
[ERROR] Memory allocation failed
```

**Additional Context:**
This happens only with files larger than 1GB.
```

## Development Tips

### Local Testing

Test your changes with different scenarios:

```bash
# Test basic functionality
upserver --port 9000 &
curl -F "file=@test.txt" http://localhost:9000/upload

# Test with configuration
upserver --config test_config.json

# Test CLI options
upserver --help
upserver --version
```

### Debugging

Enable debug logging for development:

```bash
upserver --log-level DEBUG --log-file debug.log
```

### Performance Testing

Test with large files and multiple concurrent uploads:

```bash
# Generate test file
dd if=/dev/zero of=largefile.bin bs=1M count=100

# Test upload performance
time curl -F "file=@largefile.bin" http://localhost:8000/upload
```

## Getting Help

- **Documentation**: Check the README.md and code comments
- **Issues**: Search existing issues on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Contact**: Reach out to maintainers via GitHub

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes for significant contributions
- GitHub contributor statistics

Thank you for contributing to upserver! 🚀
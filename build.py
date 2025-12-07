#!/usr/bin/env python3
"""
Build and distribution script for upserver.

This script helps with building, testing, and distributing the upserver package.
"""

import sys
import subprocess
import shutil
import os
from pathlib import Path

# Colors for terminal output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(message):
    """Print a step message in blue."""
    print(f"{Colors.BLUE}{Colors.BOLD}📦 {message}{Colors.ENDC}")

def print_success(message):
    """Print a success message in green."""
    print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")

def print_warning(message):
    """Print a warning message in yellow."""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.ENDC}")

def print_error(message):
    """Print an error message in red."""
    print(f"{Colors.RED}❌ {message}{Colors.ENDC}")

def run_command(cmd, description=None):
    """Run a command and handle errors."""
    if description:
        print_step(description)
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {cmd}")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False

def clean():
    """Clean build artifacts."""
    print_step("Cleaning build artifacts...")
    
    dirs_to_clean = [
        "build",
        "dist",
        "*.egg-info",
        "__pycache__",
        ".pytest_cache",
        "upserver/__pycache__",
        "tests/__pycache__"
    ]
    
    for pattern in dirs_to_clean:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"Removed directory: {path}")
            elif path.is_file():
                path.unlink()
                print(f"Removed file: {path}")
    
    print_success("Clean completed")

def install_dev_dependencies():
    """Install development dependencies."""
    deps = [
        "build",
        "twine",
        "pytest",
        "pytest-cov",
        "black",
        "flake8",
        "mypy"
    ]
    
    cmd = f"pip install {' '.join(deps)}"
    return run_command(cmd, "Installing development dependencies")

def run_tests():
    """Run the test suite."""
    print_step("Running test suite...")
    
    # Run tests with coverage
    if not run_command("python -m pytest tests/ -v --cov=upserver --cov-report=term-missing"):
        return False
    
    print_success("All tests passed")
    return True

def check_code_quality():
    """Run code quality checks."""
    print_step("Running code quality checks...")
    
    # Check code formatting with black
    if not run_command("python -m black --check upserver/ tests/", "Checking code formatting"):
        print_warning("Code formatting issues found. Run 'python -m black upserver/ tests/' to fix.")
        return False
    
    # Run flake8 for linting
    if not run_command("python -m flake8 upserver/ tests/ --max-line-length=88 --extend-ignore=E203,W503", "Running linting"):
        print_warning("Linting issues found.")
        return False
    
    # Run type checking with mypy
    if not run_command("python -m mypy upserver/ --ignore-missing-imports", "Running type checking"):
        print_warning("Type checking issues found.")
        return False
    
    print_success("Code quality checks passed")
    return True

def build_package():
    """Build the package."""
    print_step("Building package...")
    
    if not run_command("python -m build", "Building wheel and sdist"):
        return False
    
    # List built files
    dist_files = list(Path("dist").glob("*"))
    if dist_files:
        print_success("Package built successfully:")
        for file in dist_files:
            print(f"  📦 {file}")
    else:
        print_error("No distribution files found")
        return False
    
    return True

def check_package():
    """Check the built package."""
    print_step("Checking package...")
    
    return run_command("python -m twine check dist/*", "Validating package")

def upload_test():
    """Upload to Test PyPI."""
    print_step("Uploading to Test PyPI...")
    
    print_warning("This will upload to Test PyPI. Make sure you have configured your credentials.")
    response = input("Continue? (y/N): ")
    
    if response.lower() != 'y':
        print("Upload cancelled.")
        return False
    
    return run_command("python -m twine upload --repository testpypi dist/*")

def upload_pypi():
    """Upload to PyPI."""
    print_step("Uploading to PyPI...")
    
    print_warning("This will upload to the REAL PyPI. This action cannot be undone!")
    response = input("Are you sure? (y/N): ")
    
    if response.lower() != 'y':
        print("Upload cancelled.")
        return False
    
    return run_command("python -m twine upload dist/*")

def main():
    """Main build script."""
    if len(sys.argv) < 2:
        print(f"""
{Colors.BOLD}UpServer Build Script{Colors.ENDC}

Usage: python build.py <command>

Commands:
  clean          Clean build artifacts
  deps           Install development dependencies
  test           Run test suite
  quality        Run code quality checks
  build          Build package (includes clean, test, quality)
  check          Check built package
  upload-test    Upload to Test PyPI
  upload         Upload to PyPI
  full           Full build and check (clean, deps, test, quality, build, check)
  
Examples:
  python build.py clean
  python build.py test
  python build.py full
  python build.py upload-test
        """)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "clean":
        clean()
    
    elif command == "deps":
        install_dev_dependencies()
    
    elif command == "test":
        if not run_tests():
            sys.exit(1)
    
    elif command == "quality":
        if not check_code_quality():
            sys.exit(1)
    
    elif command == "build":
        clean()
        if not run_tests():
            sys.exit(1)
        if not check_code_quality():
            sys.exit(1)
        if not build_package():
            sys.exit(1)
    
    elif command == "check":
        if not check_package():
            sys.exit(1)
    
    elif command == "upload-test":
        if not upload_test():
            sys.exit(1)
    
    elif command == "upload":
        if not upload_pypi():
            sys.exit(1)
    
    elif command == "full":
        clean()
        if not install_dev_dependencies():
            sys.exit(1)
        if not run_tests():
            sys.exit(1)
        if not check_code_quality():
            sys.exit(1)
        if not build_package():
            sys.exit(1)
        if not check_package():
            sys.exit(1)
        print_success("Full build completed successfully!")
        print_step("Next steps:")
        print("  • Review the built packages in dist/")
        print("  • Test upload: python build.py upload-test")
        print("  • Production upload: python build.py upload")
    
    else:
        print_error(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
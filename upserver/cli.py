"""
Command-line interface for the upserver package.
"""

import argparse
import sys
from .server import FileServer
from . import __version__


def main():
    """
    Main CLI entry point for upserver.
    """
    parser = argparse.ArgumentParser(
        description="upserver - A file server for uploading and downloading files",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"upserver {__version__}"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host address to bind the server (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port number to bind the server (default: 8000)"
    )
    
    parser.add_argument(
        "--upload-dir",
        type=str,
        default="uploads",
        help="Directory to store uploaded files (default: uploads)"
    )
    
    args = parser.parse_args()
    
    try:
        server = FileServer(
            upload_dir=args.upload_dir,
            host=args.host,
            port=args.port
        )
        server.start()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Startup script for the Local Database API.
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = ['flask', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("Failed to install dependencies. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True

def start_api():
    """Start the database API server."""
    if not check_dependencies():
        return
    
    print("Starting Local Database API...")
    print("The API will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print()
    
    # Import and run the API
    from .db_api import app
    
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == "__main__":
    start_api() 
#!/usr/bin/env python3
"""
Development script to run the GDM Hackathon application
"""

import subprocess
import sys
from pathlib import Path


def run_backend():
    """Run the FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    print("📡 API will be available at: http://localhost:8000")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    print("=" * 50)

    try:
        subprocess.run([sys.executable, "api.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend server failed to start: {e}")
        return False
    return True


def run_frontend():
    """Run the frontend development server"""
    frontend_dir = Path("front")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False

    print("🎨 Starting frontend development server...")
    print("🌐 Frontend will be available at: http://localhost:5173")
    print("=" * 50)

    try:
        # Change to frontend directory and run npm dev
        subprocess.run(["npm", "run", "dev"], cwd=frontend_dir, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend server failed to start: {e}")
        return False
    return True


def main():
    print("🏥 GDM Hackathon Development Server")
    print("=" * 50)

    if len(sys.argv) > 1:
        if sys.argv[1] == "backend":
            run_backend()
        elif sys.argv[1] == "frontend":
            run_frontend()
        else:
            print("Usage: python run_dev.py [backend|frontend]")
            print("  backend  - Run only the FastAPI backend")
            print("  frontend - Run only the frontend development server")
            print("  (no args) - Run backend only")
    else:
        # Default: run backend only
        run_backend()


if __name__ == "__main__":
    main()

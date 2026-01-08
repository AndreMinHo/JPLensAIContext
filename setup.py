#!/usr/bin/env python3
"""
Setup script for JPLensAIContext
Automatically creates virtual environment and installs dependencies
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def main():
    """Main setup function"""
    print("🚀 JPLensAIContext Setup")
    print("=" * 40)

    # Check Python version
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required for this project. You have {sys.version}")
        print("💡 Consider upgrading Python or using pyenv to install Python 3.12")
        print("   Visit: https://www.python.org/downloads/")
        return False

    print(f"✅ Python version: {sys.version.split()[0]}")

    # Check if Python 3.12 is specifically available
    python312_available = False
    try:
        result = subprocess.run(["python3.12", "--version"], capture_output=True, text=True)
        if result.returncode == 0 and "Python 3.12" in result.stdout:
            python312_available = True
            print("✅ Python 3.12 found!")
    except (FileNotFoundError, subprocess.SubprocessError):
        pass

    if not python312_available:
        print("❌ Python 3.12 is required but not found.")
        print("💡 Please install Python 3.12 from: https://www.python.org/downloads/")
        print("💡 Or make sure python3.12 is in your PATH")
        print()
        print("To check if Python 3.12 is installed:")
        print("  python3.12 --version")
        return False

    # Create virtual environment with Python 3.12
    if not run_command("python3.12 -m venv venv", "Creating virtual environment with Python 3.12"):
        print("❌ Failed to create venv with Python 3.12")
        return False

    # Determine activation command based on OS
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "python -m pip install -r requirements.txt"
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "pip install -r requirements.txt"

    # Install dependencies
    if not run_command(pip_cmd, "Installing dependencies"):
        return False

    print("\n🎉 Setup complete!")
    print("\nTo activate the virtual environment:")
    if os.name == 'nt':
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")

    print("\nTo run tests:")
    print("  python -m pytest tests/")

    print("\nTo run the demo:")
    print("  python demo_ai_analysis.py")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
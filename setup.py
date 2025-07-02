#!/usr/bin/env python3
"""
Setup script for boto3-examples project.

This script automates the setup process for the development environment.
It creates a virtual environment, installs dependencies, and verifies the setup.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(command, description, check=True):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, check=check, 
                                  capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=check, 
                                  capture_output=True, text=True)
        
        if result.stdout.strip():
            print(f"   {result.stdout.strip()}")
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
        return result
        
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return None


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported.")
        print("   Please install Python 3.8 or higher.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def create_virtual_environment():
    """Create a virtual environment."""
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print("ℹ️  Virtual environment already exists at .venv")
        return True
    
    result = run_command([sys.executable, "-m", "venv", ".venv"], 
                        "Creating virtual environment")
    return result is not None


def get_activation_command():
    """Get the command to activate the virtual environment."""
    system = platform.system().lower()
    
    if system == "windows":
        return ".venv\\Scripts\\activate"
    else:
        return "source .venv/bin/activate"


def install_dependencies():
    """Install project dependencies."""
    system = platform.system().lower()
    
    if system == "windows":
        pip_path = ".venv\\Scripts\\pip.exe"
        python_path = ".venv\\Scripts\\python.exe"
    else:
        pip_path = ".venv/bin/pip"
        python_path = ".venv/bin/python"
    
    # Upgrade pip first
    run_command([python_path, "-m", "pip", "install", "--upgrade", "pip"], 
                "Upgrading pip")
    
    # Install boto3 and related packages
    packages = ["boto3", "botocore"]
    for package in packages:
        result = run_command([pip_path, "install", package], 
                           f"Installing {package}")
        if result is None:
            return False
    
    return True


def verify_installation():
    """Verify that boto3 is properly installed."""
    system = platform.system().lower()
    
    if system == "windows":
        python_path = ".venv\\Scripts\\python.exe"
    else:
        python_path = ".venv/bin/python"
    
    result = run_command([python_path, "-c", "import boto3; print(f'boto3 version: {boto3.__version__}')"], 
                        "Verifying boto3 installation")
    return result is not None


def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        try:
            content = env_example.read_text()
            env_file.write_text(content)
            print("✅ Created .env file")
            print("   Please edit .env with your AWS credentials")
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")


def main():
    """Main setup function."""
    print("🚀 Setting up boto3-examples development environment...")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("❌ Failed to verify installation")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print(f"   1. Activate the virtual environment: {get_activation_command()}")
    print("   2. Configure your AWS credentials (see README.md)")
    print("   3. Test the setup: python examples/test_connection.py")
    print("\n📚 Resources:")
    print("   - Project README: README.md")
    print("   - AWS Documentation: https://docs.aws.amazon.com/")
    print("   - Boto3 Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html")


if __name__ == "__main__":
    main()

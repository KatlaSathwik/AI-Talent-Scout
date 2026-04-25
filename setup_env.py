"""
Environment setup script for the AI-Powered Talent Scouting Agent.
Helps set up the environment and install dependencies.
"""
import os
import sys
import subprocess
import venv
from pathlib import Path


def create_virtual_environment():
    """Create a virtual environment for the project."""
    print("Creating virtual environment...")
    
    # Create venv directory
    venv_dir = Path("venv")
    if not venv_dir.exists():
        venv.create(venv_dir, with_pip=True)
        print("Virtual environment created successfully!")
    else:
        print("Virtual environment already exists.")


def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    
    try:
        # Upgrade pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    
    return True


def setup_directories():
    """Set up required directories."""
    print("Setting up directories...")
    
    directories = [
        "data",
        "data/logs",
        "data/cache"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {directory}")


def main():
    """Main setup function."""
    print("AI-Powered Talent Scouting Agent - Environment Setup")
    print("=" * 50)
    
    # Create virtual environment
    create_virtual_environment()
    
    # Setup directories
    setup_directories()
    
    # Install dependencies
    if install_dependencies():
        print("\n🎉 Environment setup completed successfully!")
        print("\nTo activate the virtual environment:")
        if os.name == 'nt':  # Windows
            print("  venv\\Scripts\\activate")
        else:  # Unix/Linux/Mac
            print("  source venv/bin/activate")
        
        print("\nTo run the application:")
        print("  python main.py")
        print("  # or")
        print("  python cli.py --job-description sample_jd.txt")
    else:
        print("\n❌ Environment setup failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
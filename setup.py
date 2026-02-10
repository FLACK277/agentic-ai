#!/usr/bin/env python3
"""
Setup script for Smart Research & Productivity Assistant
Automates initial project setup
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f" {text}")
    print("=" * 70)


def check_python_version():
    """Ensure Python 3.9+"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True


def create_virtual_environment():
    """Create Python virtual environment"""
    print_header("Creating Virtual Environment")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("⚠️  Virtual environment already exists")
        response = input("   Recreate? (y/N): ").lower()
        if response != 'y':
            print("   Skipping...")
            return True
        
        import shutil
        shutil.rmtree(venv_path)
    
    try:
        print("Creating venv...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✓ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def install_dependencies():
    """Install required packages"""
    print_header("Installing Dependencies")
    
    venv_python = Path("venv/bin/python") if os.name != 'nt' else Path("venv/Scripts/python.exe")
    
    if not venv_python.exists():
        print("❌ Virtual environment not found")
        print("   Run this script again to create it")
        return False
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.run(
            [str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
        print("✓ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def setup_env_file():
    """Create .env file from template"""
    print_header("Setting Up Environment Variables")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("⚠️  .env file already exists")
        response = input("   Overwrite? (y/N): ").lower()
        if response != 'y':
            print("   Skipping...")
            return True
    
    if not env_example.exists():
        print("❌ .env.example not found")
        return False
    
    # Copy template
    with open(env_example) as f:
        content = f.read()
    
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("✓ .env file created from template")
    print("\n⚠️  IMPORTANT: Edit .env and add your API keys:")
    print("   - ANTHROPIC_API_KEY (required)")
    print("   - Get it from: https://console.anthropic.com/")
    
    return True


def create_data_directory():
    """Create data directory for storing memories"""
    print_header("Creating Data Directory")
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Create empty memory file
    memory_file = data_dir / "memory.json"
    if not memory_file.exists():
        memory_file.write_text("[]")
    
    print("✓ Data directory ready")
    return True


def create_logs_directory():
    """Create logs directory"""
    print_header("Creating Logs Directory")
    
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create .gitkeep
    gitkeep = logs_dir / ".gitkeep"
    gitkeep.touch()
    
    print("✓ Logs directory ready")
    return True


def run_demo():
    """Ask if user wants to run demo"""
    print_header("Setup Complete!")
    
    print("\nYour agent is ready! Next steps:\n")
    print("1. Edit .env and add your ANTHROPIC_API_KEY")
    print("2. Activate virtual environment:")
    if os.name != 'nt':
        print("   source venv/bin/activate")
    else:
        print("   venv\\Scripts\\activate")
    print("3. Run the agent:")
    print("   python src/cli.py")
    print("\nOr run the demo (no API key required):")
    print("   python demo.py")
    
    response = input("\nRun demo now? (Y/n): ").lower()
    if response != 'n':
        print("\nStarting demo...")
        try:
            subprocess.run([sys.executable, "demo.py"])
        except Exception as e:
            print(f"Error running demo: {e}")


def main():
    """Main setup flow"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   Smart Research & Productivity Assistant - Setup            ║
    ║                                                              ║
    ║   This script will:                                          ║
    ║   • Check Python version                                     ║
    ║   • Create virtual environment                               ║
    ║   • Install dependencies                                     ║
    ║   • Set up configuration files                               ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Run setup steps
    steps = [
        ("Python Version", check_python_version),
        ("Virtual Environment", create_virtual_environment),
        ("Dependencies", install_dependencies),
        ("Environment Variables", setup_env_file),
        ("Data Directory", create_data_directory),
        ("Logs Directory", create_logs_directory),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please fix the error and run setup.py again")
            sys.exit(1)
    
    # Offer to run demo
    run_demo()


if __name__ == "__main__":
    main()

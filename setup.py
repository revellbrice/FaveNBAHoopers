#!/usr/bin/env python3
"""
Setup script to help initialize the NBA Stats ETL project.

This script will guide you through the initial setup process.
"""
import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Check if Python version is 3.8+."""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    print("✅ Python version is compatible")


def create_env_file():
    """Create .env file from .env.example if it doesn't exist."""
    print_header("Setting Up Environment Variables")
    
    if os.path.exists('.env'):
        print("⚠️  .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print("Skipping .env creation")
            return
    
    if not os.path.exists('.env.example'):
        print("❌ Error: .env.example not found")
        return
    
    # Copy .env.example to .env
    with open('.env.example', 'r') as f:
        content = f.read()
    
    with open('.env', 'w') as f:
        f.write(content)
    
    print("✅ Created .env file from template")
    print("\n📝 Please edit .env and add your PostgreSQL credentials:")
    print("   - DB_HOST")
    print("   - DB_PORT")
    print("   - DB_NAME")
    print("   - DB_USER")
    print("   - DB_PASSWORD")


def install_dependencies():
    """Install Python dependencies from requirements.txt."""
    print_header("Installing Dependencies")
    
    if not os.path.exists('requirements.txt'):
        print("❌ Error: requirements.txt not found")
        return
    
    print("Installing packages from requirements.txt...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ All dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        sys.exit(1)


def check_database_connection():
    """Check if database connection works."""
    print_header("Testing Database Connection")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from sqlalchemy import create_engine
        from config import config
        
        engine = create_engine(config.database_url)
        connection = engine.connect()
        connection.close()
        
        print("✅ Database connection successful!")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\nPlease check your .env file and ensure:")
        print("  1. PostgreSQL is running")
        print("  2. Database credentials are correct")
        print("  3. Database exists")
        return False
    
    return True


def create_directories():
    """Create necessary directories."""
    print_header("Creating Directories")
    
    directories = ['data', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/ directory")


def main():
    """Run the setup process."""
    print("\n" + "🏀" * 30)
    print("  NBA STATS ETL - SETUP WIZARD")
    print("🏀" * 30)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    response = input("\nInstall Python dependencies? (Y/n): ").strip().lower()
    if response != 'n':
        install_dependencies()
    
    # Create .env file
    create_env_file()
    
    # Create directories
    create_directories()
    
    # Wait for user to configure .env
    print_header("Configure Database Credentials")
    print("Before testing the database connection, please:")
    print("  1. Open the .env file")
    print("  2. Add your PostgreSQL credentials")
    print("  3. Save the file")
    
    input("\nPress Enter when you've configured the .env file...")
    
    # Test database connection
    if check_database_connection():
        print_header("Setup Complete! 🎉")
        print("You're ready to run the ETL pipeline:")
        print("\n  python nba_stats_etl.py")
        print("\nOr analyze existing data:")
        print("\n  python analyze_stats.py")
        print("\nFor more information, see README.md")
    else:
        print_header("Setup Incomplete")
        print("Please fix the database connection issue and try again.")


if __name__ == '__main__':
    main()

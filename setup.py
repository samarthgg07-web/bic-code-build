#!/usr/bin/env python3
"""
Code, Bid & Build - Setup Script
Helps initialize the application and database
"""

import os
import sys
import subprocess
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print_header("Checking Python Version")
    
    if sys.version_info < (3, 8):
        print_error(f"Python 3.8+ required. You have {sys.version_info.major}.{sys.version_info.minor}")
        return False
    
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_project_structure():
    """Check if all required files exist"""
    print_header("Checking Project Structure")
    
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        'README.md',
        'templates/base.html',
        'templates/index.html',
        'static/css/style.css',
        'static/js/script.js',
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print_success(f"Found: {file}")
        else:
            print_error(f"Missing: {file}")
            all_exist = False
    
    return all_exist

def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Dependencies")
    
    if not os.path.exists('requirements.txt'):
        print_error("requirements.txt not found!")
        return False
    
    try:
        print_info("Installing packages from requirements.txt...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print_success("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install dependencies")
        return False

def create_database():
    """Initialize database"""
    print_header("Initializing Database")
    
    try:
        from app import app, db
        
        with app.app_context():
            db.create_all()
            print_success("Database initialized successfully!")
            
            from app import TeamRegistration
            table_count = TeamRegistration.query.count()
            print_info(f"Current registrations: {table_count}")
        
        return True
    except Exception as e:
        print_error(f"Failed to initialize database: {str(e)}")
        return False

def display_credentials():
    """Display default admin credentials"""
    print_header("Admin Credentials")
    
    print_info("Default Login Credentials (CHANGE IN PRODUCTION):")
    print(f"\n  {Colors.BOLD}Username:{Colors.ENDC} admin")
    print(f"  {Colors.BOLD}Password:{Colors.ENDC} Admin@123\n")
    print_warning("⚠ Please change these credentials before deploying to production!")

def display_startup_info():
    """Display application startup information"""
    print_header("Application Ready!")
    
    print_info("To start the application, run:")
    print(f"\n  {Colors.BOLD}python app.py{Colors.ENDC}\n")
    
    print_info("Then open your browser and visit:")
    print(f"\n  {Colors.BOLD}http://localhost:5000{Colors.ENDC}\n")

def main():
    """Main setup function"""
    print_header("Code, Bid & Build - Setup Script")
    
    # Step 1: Check Python version
    if not check_python_version():
        print_error("Setup failed: Python version incompatible")
        sys.exit(1)
    
    # Step 2: Check project structure
    if not check_project_structure():
        print_error("Setup failed: Some required files are missing")
        sys.exit(1)
    
    # Step 3: Install dependencies
    if not install_dependencies():
        print_error("Setup failed: Could not install dependencies")
        sys.exit(1)
    
    # Step 4: Initialize database
    if not create_database():
        print_warning("Database initialization failed, but you can still run the app")
    
    # Step 5: Display credentials
    display_credentials()
    
    # Step 6: Display startup info
    display_startup_info()
    
    print_success("Setup completed successfully! Happy Coding! 🎉\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\nSetup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)

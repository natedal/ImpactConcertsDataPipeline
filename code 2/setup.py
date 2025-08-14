#!/usr/bin/env python3
"""
Setup script for iVoted data processing pipeline
Run this script to install dependencies and verify setup
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors gracefully"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def verify_installation():
    """Verify that all required packages are installed"""
    required_packages = [
        "pandas", "selenium", "webdriver-manager", 
        "gspread", "gspread-dataframe", "oauth2client"
    ]
    
    print("🔍 Verifying package installation...")
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ["files_for_processing", "results"]
    
    print("📁 Creating necessary directories...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created {directory}/")
        else:
            print(f"✅ {directory}/ already exists")
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up iVoted data processing pipeline...\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("\n❌ Setup failed during verification")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\n❌ Setup failed during directory creation")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Place your Google Cloud service account JSON file in the project directory")
    print("2. Update SPREADSHEET_ID in UploadtoGoogleSheets.py")
    print("3. Run: python main.py (to process city data)")
    print("4. Run: python UploadtoGoogleSheets.py (to upload to Google Sheets)")
    print("\n📖 See README.md for detailed instructions")

if __name__ == "__main__":
    main() 
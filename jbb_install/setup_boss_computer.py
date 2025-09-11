"""
COMPLETE Setup script to prepare the ISSA dashboard for boss's computer
Run this once after cloning the repository
Enhanced based on project history and requirements
"""

import os
import sys
from pathlib import Path
import subprocess
import shutil

def setup_paths():
    """Ensure all file paths are relative and work cross-platform"""
    
    # Get the current directory (should be the project root)
    project_root = Path(__file__).parent
    print(f"Setting up project in: {project_root}")
    
    # Check if we're in the right directory
    expected_files = ['src/dashboard/fully_integrated_dashboard.py', 'README.md']
    missing_files = []
    
    for file in expected_files:
        if not (project_root / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("ERROR: Some expected files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        print("Make sure you're running this from the project root directory.")
        return False
    
    print("✅ All expected files found!")
    
    # Create any missing directories
    directories_to_create = [
        'src/metrics/cfo',
        'src/metrics/cio', 
        'src/metrics/cto',
        'src/metrics/hbcu',
        'src/metrics/pm',  # Project Manager metrics
        'src/dashboard',
        'data',
        'screenshots',
        'logs'  # For debugging
    ]
    
    for directory in directories_to_create:
        dir_path = project_root / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 8:
        print(f"✅ Python version {python_version.major}.{python_version.minor} is compatible")
    else:
        print(f"⚠️  Python version {python_version.major}.{python_version.minor} may have compatibility issues")
        print("   Recommended: Python 3.8 or newer")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️  Not in a virtual environment. Consider using 'python -m venv venv'")
    
    return True

def check_packages():
    """Check if required packages are installed"""
    # Enhanced package list based on your project history
    required_packages = [
        'streamlit',
        'pandas', 
        'plotly',
        'numpy',
        'openpyxl',  # For Excel file handling
        'python-dateutil',  # For date handling
        'requests'  # For web requests
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is NOT installed")
    
    if missing_packages:
        print("\nTo install missing packages, run:")
        print("pip install -r requirements_complete.txt")
        return False
    
    return True

def create_requirements_complete():
    """Create a complete requirements.txt file based on project history"""
    
    requirements_content = """streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
numpy>=1.24.0
python-dateutil>=2.8.0
openpyxl>=3.1.0
xlsxwriter>=3.1.0
requests>=2.31.0
pathlib2
typing-extensions"""
    
    requirements_path = Path(__file__).parent / "requirements_complete.txt"
    with open(requirements_path, 'w') as f:
        f.write(requirements_content)
    
    print(f"✅ Created complete requirements file: {requirements_path}")
    return requirements_path

def create_run_scripts():
    """Create multiple run scripts for different scenarios"""
    
    # Windows batch script
    run_script_content = '''@echo off
echo Starting ISSA Dashboard for Paul Quinn College...
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "venv\\Scripts\\activate.bat" (
    echo Activating virtual environment...
    call venv\\Scripts\\activate.bat
)

REM Check if required packages are installed
python -c "import streamlit, pandas, plotly" 2>nul
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements_complete.txt
)

REM Run the dashboard
echo Starting Streamlit dashboard...
echo Dashboard will open at: http://localhost:8503
streamlit run src/dashboard/fully_integrated_dashboard.py --server.port 8503

echo.
echo Dashboard stopped. Press any key to close...
pause >nul
'''
    
    script_path = Path(__file__).parent / "run_dashboard.bat"
    with open(script_path, 'w') as f:
        f.write(run_script_content)
    
    print(f"✅ Created run script: {script_path}")
    
    # PowerShell script for advanced users
    ps_script_content = '''# ISSA Dashboard PowerShell Runner
Write-Host "Starting ISSA Dashboard for Paul Quinn College..." -ForegroundColor Green
Set-Location $PSScriptRoot

# Activate virtual environment if it exists
if (Test-Path "venv\\Scripts\\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\\venv\\Scripts\\Activate.ps1
}

# Check and install packages if needed
try {
    python -c "import streamlit, pandas, plotly"
    Write-Host "✅ All packages installed" -ForegroundColor Green
} catch {
    Write-Host "Installing required packages..." -ForegroundColor Yellow
    pip install -r requirements_complete.txt
}

# Run the dashboard
Write-Host "Starting Streamlit dashboard..." -ForegroundColor Green
Write-Host "Dashboard will open at: http://localhost:8503" -ForegroundColor Cyan
streamlit run src/dashboard/fully_integrated_dashboard.py --server.port 8503

Read-Host "Press Enter to close..."
'''
    
    ps_script_path = Path(__file__).parent / "run_dashboard.ps1"
    with open(ps_script_path, 'w') as f:
        f.write(ps_script_content)
    
    print(f"✅ Created PowerShell script: {ps_script_path}")
    
    return script_path, ps_script_path

def create_quick_install_guide():
    """Create a quick installation guide for the boss"""
    
    guide_content = """# ISSA Dashboard - Quick Installation Guide

## Option 1: Easy Installation (Recommended)
1. Double-click `run_dashboard.bat`
2. Wait for installation to complete
3. Dashboard will open in your browser

## Option 2: Manual Installation
1. Open Command Prompt in this folder
2. Run: `python -m venv venv`
3. Run: `venv\\Scripts\\activate`
4. Run: `pip install -r requirements_complete.txt`
5. Run: `streamlit run src/dashboard/fully_integrated_dashboard.py`

## Troubleshooting
- If Python is not found: Install Python 3.8+ from python.org
- If packages fail to install: Try running as Administrator
- If dashboard won't open: Check Windows Firewall settings

## What This Dashboard Does
- Displays financial metrics for Paul Quinn College IT spending
- Shows CFO, CIO, CTO, and Project Manager views
- Includes HBCU-specific institutional metrics
- Provides AI-powered optimization recommendations

## Support
Contact: [Your contact information here]
"""
    
    guide_path = Path(__file__).parent / "INSTALLATION_GUIDE.md"
    with open(guide_path, 'w') as f:
        f.write(guide_content)
    
    print(f"✅ Created installation guide: {guide_path}")
    return guide_path

def check_git_setup():
    """Check if Git is properly configured"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git is installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Git command failed")
            return False
    except FileNotFoundError:
        print("❌ Git is not installed or not in PATH")
        return False

def create_troubleshooting_script():
    """Create a script to diagnose common issues"""
    
    troubleshoot_content = '''@echo off
echo ISSA Dashboard Troubleshooting Tool
echo =====================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8 or newer.
    pause
    exit /b 1
)

echo.
echo Checking Python packages...
python -c "import sys; print(f'Python path: {sys.executable}')"
python -c "import streamlit; print(f'Streamlit version: {streamlit.__version__}')" 2>nul
if errorlevel 1 (
    echo ❌ Streamlit not installed
) else (
    echo ✅ Streamlit installed
)

python -c "import pandas; print(f'Pandas version: {pandas.__version__}')" 2>nul
if errorlevel 1 (
    echo ❌ Pandas not installed
) else (
    echo ✅ Pandas installed
)

python -c "import plotly; print(f'Plotly version: {plotly.__version__}')" 2>nul
if errorlevel 1 (
    echo ❌ Plotly not installed
) else (
    echo ✅ Plotly installed
)

echo.
echo Checking file structure...
if exist "src\\dashboard\\fully_integrated_dashboard.py" (
    echo ✅ Main dashboard file found
) else (
    echo ❌ Main dashboard file missing
)

if exist "requirements_complete.txt" (
    echo ✅ Requirements file found
) else (
    echo ❌ Requirements file missing
)

echo.
echo Troubleshooting complete.
pause
'''
    
    troubleshoot_path = Path(__file__).parent / "troubleshoot.bat"
    with open(troubleshoot_path, 'w') as f:
        f.write(troubleshoot_content)
    
    print(f"✅ Created troubleshooting script: {troubleshoot_path}")
    return troubleshoot_path

def main():
    print("🚀 Setting up ISSA Dashboard for Boss's Computer")
    print("=" * 60)
    print("Paul Quinn College IT Analytics Suite - Complete Setup")
    print("=" * 60)
    
    # Setup paths and directories
    if not setup_paths():
        print("❌ Setup failed. Please check the errors above.")
        return
    
    print("\n📦 Creating complete requirements file...")
    create_requirements_complete()
    
    print("\n🔍 Checking installed packages...")
    packages_ok = check_packages()
    
    print("\n🎯 Creating convenience scripts...")
    run_script, ps_script = create_run_scripts()
    
    print("\n📚 Creating installation guide...")
    create_quick_install_guide()
    
    print("\n🔧 Creating troubleshooting tools...")
    create_troubleshooting_script()
    
    print("\n🔍 Checking Git setup...")
    git_ok = check_git_setup()
    
    print("\n" + "=" * 60)
    if packages_ok:
        print("🎉 Setup completed successfully!")
        print("\n📋 FILES CREATED:")
        print("   • run_dashboard.bat - Double-click to start dashboard")
        print("   • run_dashboard.ps1 - PowerShell alternative")
        print("   • requirements_complete.txt - All required packages")
        print("   • INSTALLATION_GUIDE.md - Step-by-step instructions")
        print("   • troubleshoot.bat - Diagnose issues")
        
        print("\n🚀 TO RUN THE DASHBOARD:")
        print("   1. Double-click 'run_dashboard.bat' OR")
        print("   2. Open Command Prompt here and run:")
        print("      streamlit run src/dashboard/fully_integrated_dashboard.py")
        
        print("\n🌐 DASHBOARD WILL OPEN AT:")
        print("   http://localhost:8503")
        
    else:
        print("⚠️  Setup completed with warnings.")
        print("Please install missing packages before running the dashboard.")
        print("Run: pip install -r requirements_complete.txt")
    
    if not git_ok:
        print("\n⚠️  Git not detected. This is OK for running the dashboard,")
        print("    but needed for version control and updates.")

if __name__ == "__main__":
    main()
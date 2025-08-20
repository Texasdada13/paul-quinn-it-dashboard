#!/usr/bin/env python3
"""
Script to safely reorganize Paul Quinn IT project files
Run this from your Paul-Quinn-IT-Spend-GitHub directory
"""

import os
import shutil
from pathlib import Path
import json

def create_directory_structure():
    """Create the new directory structure"""
    directories = [
        "src",
        "src/data_processing",
        "src/dashboard",
        "src/utils",
        "src/tests",
        "src/alerts",  # Added for your contract alerts
        "data/raw",
        "data/processed",
        "data/mock",
        "docs/requirements",
        "docs/setup",
        "config",
        "notebooks"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {dir_path}")
    
    # Create __init__.py files
    init_files = [
        "src/__init__.py",
        "src/data_processing/__init__.py",
        "src/dashboard/__init__.py",
        "src/utils/__init__.py",
        "src/tests/__init__.py",
        "src/alerts/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"✓ Created {init_file}")

def get_file_mapping():
    """Define where each file should go"""
    return {
        # Data processing files
        "analyze_robust_data.py": "src/data_processing/",
        "data_requirements_checklist.py": "src/data_processing/",
        "export_analytics.py": "src/data_processing/",
        
        # Dashboard files
        "app.py": "src/dashboard/",
        "it_dashboard_app.py": "src/dashboard/",
        "it_dashboard_app_fixed.py": "src/dashboard/",
        
        # Alert files
        "cfo_contract_expiration_alerts_script.py": "src/alerts/",
        "tech_stack_health_metrics_script.py": "src/alerts/",
        "asset_lifecycle_management_metrics_script.py": "src/alerts/",
        
        # Utility files
        "generate_robust_mock_data.py": "src/utils/",
        "generate_robust_mock_data_fixed.py": "src/utils/",
        "generate_usage_roi_data.py": "src/utils/",
        
        # Test files
        "app_test.py": "src/tests/",
        
        # Data files
        "PQC_Data_Collection_Template.xlsx": "data/raw/",
        "PQC_Robust_Mock_Data.xlsx": "data/mock/",
        "PQC_Usage_Efficiency_ROI_Data.xlsx": "data/mock/",
        
        # Documentation
        "paul_quinn_data_requirements.xlsx": "docs/requirements/",
        "requirements.txt": "./",  # Keep in root
        "README.md": "./"  # Keep in root
    }

def move_files():
    """Move files to their new locations"""
    file_mapping = get_file_mapping()
    moved_files = []
    skipped_files = []
    
    for filename, destination in file_mapping.items():
        source = Path(filename)
        if source.exists():
            dest_path = Path(destination) / filename
            try:
                # Create destination directory if it doesn't exist
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Move the file
                shutil.move(str(source), str(dest_path))
                moved_files.append(f"{filename} → {destination}")
                print(f"✓ Moved {filename} to {destination}")
            except Exception as e:
                print(f"✗ Error moving {filename}: {e}")
        else:
            skipped_files.append(filename)
    
    return moved_files, skipped_files

def create_requirements_txt():
    """Create a requirements.txt file"""
    requirements = [
        "streamlit>=1.28.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "plotly>=5.14.0",
        "openpyxl>=3.1.0",
        "pytest>=7.3.0",
        "python-dateutil>=2.8.0",
        "pytz>=2023.3"
    ]
    
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    print("✓ Created requirements.txt")

def create_gitignore():
    """Create a .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv/

# Virtual Environment
bin/
include/
lib/
lib64/
share/
pyvenv.cfg

# Data files (comment out if you want to track these)
# *.csv
# *.xlsx
# *.xls

# IDE
.vscode/
.idea/
*.swp
*.swo
*.swn

# OS
.DS_Store
Thumbs.db
desktop.ini

# Logs
*.log
logs/

# Pytest
.pytest_cache/
.coverage
htmlcov/

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Environment variables
.env
.env.local

# Backup files
*_BACKUP/
*.bak
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("✓ Created .gitignore")

def create_readme():
    """Create an enhanced README.md"""
    readme_content = """# Paul Quinn College IT Analytics Suite

A comprehensive IT spend management and analytics dashboard for Paul Quinn College.

## Project Structure

```
Paul-Quinn-IT-Dashboard/
├── src/                      # Source code
│   ├── alerts/              # Alert and notification scripts
│   ├── dashboard/           # Streamlit dashboard application
│   ├── data_processing/     # Data analysis and processing
│   ├── utils/              # Utility functions and mock data generators
│   └── tests/              # Unit tests
├── data/                    # Data files
│   ├── raw/                # Original data files
│   ├── processed/          # Processed data
│   └── mock/               # Mock/test data
├── docs/                   # Documentation
├── config/                 # Configuration files
└── notebooks/              # Jupyter notebooks for analysis
```

## Features

- **Multi-Persona Views**: Tailored dashboards for CFO, CIO, and CTO
- **Budget Analysis**: Track IT spending across categories with variance analysis
- **Contract Management**: Monitor active contracts, expiration alerts, and renewal tracking
- **Project Tracking**: Real-time project status, timelines, and budget monitoring
- **Risk Assessment**: Identify and manage IT-related risks
- **ROI Calculations**: Measure return on IT investments

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Texasdada13/paul-quinn-it-dashboard.git
   cd paul-quinn-it-dashboard
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Dashboard
```bash
streamlit run src/dashboard/app.py
```

### Running Alert Scripts
```bash
python src/alerts/cfo_contract_expiration_alerts_script.py
```

## Development

- Add new features in the appropriate subdirectory under `src/`
- Place test files in `src/tests/`
- Update documentation in `docs/`

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## License

[Your License Here]
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    print("✓ Created README.md")

def create_movement_report():
    """Create a report of what was moved"""
    report = {
        "timestamp": str(Path.cwd()),
        "current_directory": str(Path.cwd()),
        "actions_taken": []
    }
    
    with open("reorganization_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("✓ Created reorganization report")

def main():
    """Main function to orchestrate the reorganization"""
    print("🚀 Starting project reorganization...\n")
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}\n")
    
    # Confirm before proceeding
    response = input("Are you in the Paul-Quinn-IT-Spend-GitHub directory? (yes/no): ")
    if response.lower() != "yes":
        print("Please navigate to the correct directory first.")
        return
    
    print("\nThis script will:")
    print("1. Create a new directory structure")
    print("2. Move files to organized locations")
    print("3. Create requirements.txt and .gitignore")
    print("4. Update README.md")
    print("\nYour original files will be MOVED (not copied).")
    
    confirm = input("\nProceed with reorganization? (yes/no): ")
    if confirm.lower() != "yes":
        print("Reorganization cancelled.")
        return
    
    print("\n" + "="*50 + "\n")
    
    # Execute reorganization
    print("📁 Creating directory structure...")
    create_directory_structure()
    
    print("\n📄 Moving files...")
    moved_files, skipped_files = move_files()
    
    print("\n📝 Creating configuration files...")
    create_requirements_txt()
    create_gitignore()
    create_readme()
    create_movement_report()
    
    print("\n" + "="*50)
    print("✅ Reorganization complete!")
    
    if skipped_files:
        print(f"\n⚠️  Files not found (skipped): {len(skipped_files)}")
        for file in skipped_files[:5]:  # Show first 5
            print(f"   - {file}")
        if len(skipped_files) > 5:
            print(f"   ... and {len(skipped_files) - 5} more")
    
    print("\n📋 Next steps:")
    print("1. Review the new structure")
    print("2. Update import statements in Python files")
    print("3. Test that everything still works")
    print("4. Commit changes to Git")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Simple script to organize Paul Quinn IT project files
"""

import os
import shutil
from pathlib import Path

def create_folders():
    """Create the organized folder structure"""
    folders = [
        "src/data_processing",
        "src/dashboard", 
        "src/utils",
        "src/tests",
        "data/raw",
        "data/processed",
        "data/mock",
        "docs",
        "config"
    ]
    
    print("Creating folders...")
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {folder}")

def organize_files():
    """Move files to their appropriate locations"""
    
    # Define where each file should go
    file_moves = {
        # Data processing scripts
        "analyze_robust_data.py": "src/data_processing/",
        "data_requirements_checklist.py": "src/data_processing/",
        "export_analytics.py": "src/data_processing/",
        
        # Dashboard files
        "it_dashboard_app_fixed.py": "src/dashboard/app.py",  # Rename to app.py
        
        # Utility scripts
        "generate_robust_mock_data.py": "src/utils/",
        "generate_robust_mock_data_fixed.py": "src/utils/",
        "generate_usage_roi_data.py": "src/utils/",
        "create_collection_template.py": "src/utils/",
        
        # Test files
        "simple_etl_test.py": "src/tests/",
        "debug_paths.py": "src/tests/",
        "simple_project_etl.py": "src/tests/",
        
        # Data files
        "PQC_Data_Collection_Template.xlsx": "data/raw/",
        "PQC_Robust_Mock_Data.xlsx": "data/mock/",
        "PQC_Usage_Efficiency_ROI_Data.xlsx": "data/mock/",
        "paul_quinn_data_requirements.csv": "data/raw/",
        
        # Config files
        "config.toml": "config/",
        "requirements.txt": "./"  # Keep in root
    }
    
    print("\nMoving files...")
    for source, destination in file_moves.items():
        if os.path.exists(source):
            try:
                # Handle renaming case
                if destination.endswith('.py'):
                    dest_path = destination
                else:
                    dest_path = os.path.join(destination, source)
                
                # Create destination directory if needed
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Move the file
                shutil.move(source, dest_path)
                print(f"✓ Moved {source} → {dest_path}")
            except Exception as e:
                print(f"✗ Error moving {source}: {e}")
        else:
            print(f"- Skipped {source} (not found)")

def create_init_files():
    """Create __init__.py files for Python packages"""
    init_locations = [
        "src/__init__.py",
        "src/data_processing/__init__.py",
        "src/dashboard/__init__.py",
        "src/utils/__init__.py",
        "src/tests/__init__.py"
    ]
    
    print("\nCreating __init__.py files...")
    for init_file in init_locations:
        Path(init_file).touch()
        print(f"✓ Created {init_file}")

def create_readme():
    """Create a basic README.md file"""
    readme_content = """# Paul Quinn College IT Analytics Dashboard

## Project Structure

```
├── src/
│   ├── dashboard/          # Streamlit dashboard app
│   ├── data_processing/    # Data analysis scripts  
│   ├── utils/             # Utility functions
│   └── tests/             # Test files
├── data/
│   ├── raw/               # Original data files
│   ├── processed/         # Processed data
│   └── mock/              # Mock/test data
├── docs/                  # Documentation
├── config/                # Configuration files
└── requirements.txt       # Python dependencies
```

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the dashboard:
   ```bash
   python -m streamlit run src/dashboard/app.py
   ```

## Features

- IT spend tracking and analysis
- Multi-persona dashboards (CFO, CIO, CTO)
- Budget vs actual reporting
- Vendor management
- Project tracking
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    print("\n✓ Created README.md")

def main():
    """Main function"""
    print("🚀 Organizing Paul Quinn IT Project\n")
    
    # Confirm we're in the right directory
    current_files = os.listdir('.')
    if 'analyze_robust_data.py' not in current_files:
        print("❌ Error: Not in the correct directory!")
        print("Please run this script from the Paul-Quinn-IT-Spend-GitHub folder")
        return
    
    # Create backup reminder
    print("⚠️  This will reorganize your files!")
    print("Make sure you have a backup of your work.")
    
    response = input("\nContinue? (yes/no): ")
    if response.lower() != 'yes':
        print("Cancelled.")
        return
    
    # Run organization steps
    create_folders()
    organize_files()
    create_init_files()
    create_readme()
    
    print("\n✅ Organization complete!")
    print("\nNext steps:")
    print("1. Check the new folder structure with: ls -la")
    print("2. Update any import statements in your Python files")
    print("3. Test the dashboard with: python -m streamlit run src/dashboard/app.py")

if __name__ == "__main__":
    main()
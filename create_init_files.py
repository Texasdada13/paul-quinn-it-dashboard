"""
Create __init__.py files for proper Python imports
"""

import os
from pathlib import Path

def create_init_files():
    """Create __init__.py files in all necessary directories"""
    
    # Directories that need __init__.py files
    directories = [
        'src',
        'src/metrics',
        'src/metrics/cfo',
        'src/metrics/cio', 
        'src/metrics/cto',
        'src/dashboard',
        'src/data_processing',
        'src/utils',
        'src/tests',
        'src/hbcu_modules'  # This is where your HBCU metrics actually are
    ]
    
    # Remove the empty hbcu folder if you want
    # directories.remove('src/metrics/hbcu')
    
    for directory in directories:
        dir_path = Path(directory)
        if dir_path.exists():
            init_file = dir_path / '__init__.py'
            if not init_file.exists():
                init_file.touch()
                print(f"✓ Created {init_file}")
            else:
                print(f"  {init_file} already exists")
        else:
            print(f"✗ Directory {directory} does not exist")

if __name__ == "__main__":
    print("Creating __init__.py files...")
    create_init_files()
    print("\nDone! All __init__.py files have been created.")
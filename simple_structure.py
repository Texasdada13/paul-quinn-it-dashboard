#!/usr/bin/env python3
"""
Condensed Project Structure Mapper - Only shows key directories and files
"""

import os
from datetime import datetime

def should_skip_file(filename):
    """Files/folders to skip"""
    skip_patterns = [
        '.git', '__pycache__', '.DS_Store', 'Thumbs.db',
        '.pyc', '.pyo', '.pyd', '.so', '.egg-info',
        'node_modules', '.vscode', '.idea'
    ]
    return any(pattern in filename for pattern in skip_patterns)

def map_key_structure(path, output_file, prefix="", max_depth=3, current_depth=0):
    """Map only key directories and important files"""
    if current_depth > max_depth:
        return
    
    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        return
    
    # Key directories to always show
    key_dirs = ['src', 'metrics', 'dashboard', 'cio', 'cto', 'cfo', 'data']
    
    folders = [item for item in items if os.path.isdir(os.path.join(path, item)) 
               and not should_skip_file(item)]
    
    # Important files to show
    important_extensions = ['.py', '.csv', '.xlsx', '.json', '.toml', '.txt', '.md']
    important_names = ['requirements.txt', 'config.toml', 'README.md']
    
    files = [item for item in items if os.path.isfile(os.path.join(path, item)) 
             and not should_skip_file(item) 
             and (any(item.endswith(ext) for ext in important_extensions) 
                  or item in important_names)]
    
    # Show folders (prioritize key ones)
    priority_folders = [f for f in folders if f in key_dirs]
    other_folders = [f for f in folders if f not in key_dirs]
    
    for folder in priority_folders + other_folders[:3]:  # Limit to key + 3 others
        folder_path = os.path.join(path, folder)
        output_file.write(f"{prefix}├── {folder}/\n")
        map_key_structure(folder_path, output_file, prefix + "│   ", max_depth, current_depth + 1)
    
    # Show important files (limit to 10 most important)
    python_files = [f for f in files if f.endswith('.py')][:5]
    data_files = [f for f in files if f.endswith(('.csv', '.xlsx'))][:3]
    config_files = [f for f in files if f in important_names]
    
    key_files = config_files + python_files + data_files
    
    for filename in key_files:
        output_file.write(f"{prefix}├── {filename}\n")

def main():
    """Create condensed project structure"""
    project_root = os.getcwd()
    project_name = os.path.basename(project_root)
    
    output_filename = "project_structure_condensed.txt"
    
    print(f"Creating condensed structure map: {output_filename}")
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"CONDENSED PROJECT STRUCTURE - {project_name}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"{project_name}/\n")
        map_key_structure(project_root, f)
        
        # Key file summary
        f.write("\n" + "=" * 60 + "\n")
        f.write("KEY FILES FOUND:\n")
        f.write("=" * 60 + "\n")
        
        key_files_to_find = [
            'fully_integrated_dashboard.py',
            'dashboard_metric_loader.py', 
            'metric_registry.py',
            'generate_all_cio_metrics.py',
            'generate_cto_data.py'
        ]
        
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if not should_skip_file(d)][:2]  # Limit depth
            
            for file in files:
                if file in key_files_to_find:
                    rel_path = os.path.relpath(os.path.join(root, file), project_root)
                    f.write(f"✓ {rel_path}\n")
        
        # Count by type
        f.write("\nFILE TYPE SUMMARY:\n")
        
        py_count = csv_count = xlsx_count = 0
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if not should_skip_file(d)]
            for file in files:
                if file.endswith('.py'):
                    py_count += 1
                elif file.endswith('.csv'):
                    csv_count += 1
                elif file.endswith('.xlsx'):
                    xlsx_count += 1
        
        f.write(f"Python files: {py_count}\n")
        f.write(f"CSV files: {csv_count}\n") 
        f.write(f"Excel files: {xlsx_count}\n")
    
    print(f"Done! File size: {os.path.getsize(output_filename)} bytes")

if __name__ == "__main__":
    main()
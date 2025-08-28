#!/usr/bin/env python3
"""
Project Structure Mapper
Generates a comprehensive map of your project's file and folder structure
"""

import os
import sys
from datetime import datetime

def get_file_info(filepath):
    """Get basic file information"""
    try:
        size = os.path.getsize(filepath)
        # Convert size to readable format
        if size > 1024 * 1024:
            size_str = f"{size / (1024*1024):.1f}MB"
        elif size > 1024:
            size_str = f"{size / 1024:.1f}KB"
        else:
            size_str = f"{size}B"
        
        # Get file extension
        _, ext = os.path.splitext(filepath)
        return size_str, ext.lower()
    except:
        return "0B", ""

def should_skip_file(filename):
    """Files/folders to skip for cleaner output"""
    skip_patterns = [
        '.git', '__pycache__', '.DS_Store', 'Thumbs.db',
        '.pyc', '.pyo', '.pyd', '.so', '.egg-info',
        'node_modules', '.vscode', '.idea'
    ]
    return any(pattern in filename for pattern in skip_patterns)

def map_directory(path, output_file, prefix="", max_depth=10, current_depth=0):
    """Recursively map directory structure"""
    if current_depth > max_depth:
        return
    
    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        output_file.write(f"{prefix}[Permission Denied]\n")
        return
    
    folders = [item for item in items if os.path.isdir(os.path.join(path, item)) and not should_skip_file(item)]
    files = [item for item in items if os.path.isfile(os.path.join(path, item)) and not should_skip_file(item)]
    
    # Process folders first
    for i, folder in enumerate(folders):
        folder_path = os.path.join(path, folder)
        is_last_folder = (i == len(folders) - 1) and len(files) == 0
        
        if is_last_folder:
            output_file.write(f"{prefix}└── 📁 {folder}/\n")
            new_prefix = prefix + "    "
        else:
            output_file.write(f"{prefix}├── 📁 {folder}/\n")
            new_prefix = prefix + "│   "
        
        map_directory(folder_path, output_file, new_prefix, max_depth, current_depth + 1)
    
    # Process files
    for i, filename in enumerate(files):
        filepath = os.path.join(path, filename)
        size_str, ext = get_file_info(filepath)
        
        # Choose icon based on file type
        if ext in ['.py']:
            icon = "🐍"
        elif ext in ['.csv']:
            icon = "📊"
        elif ext in ['.json']:
            icon = "📋"
        elif ext in ['.md', '.txt']:
            icon = "📝"
        elif ext in ['.xlsx', '.xls']:
            icon = "📈"
        elif ext in ['.yml', '.yaml', '.toml']:
            icon = "⚙️"
        elif ext in ['.sh', '.bat']:
            icon = "🔧"
        else:
            icon = "📄"
        
        is_last = (i == len(files) - 1)
        connector = "└──" if is_last else "├──"
        
        output_file.write(f"{prefix}{connector} {icon} {filename} ({size_str})\n")

def main():
    """Main function to create project structure map"""
    # Get the current working directory
    project_root = os.getcwd()
    project_name = os.path.basename(project_root)
    
    # Create output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"project_structure_{timestamp}.txt"
    
    print(f"Mapping project structure for: {project_root}")
    print(f"Output will be saved to: {output_filename}")
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        # Write header
        f.write("=" * 80 + "\n")
        f.write(f"PROJECT STRUCTURE MAP\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Project Root: {project_root}\n")
        f.write(f"Project Name: {project_name}\n")
        f.write("=" * 80 + "\n\n")
        
        # Write directory tree
        f.write(f"🏗️ {project_name}/\n")
        map_directory(project_root, f)
        
        # Write summary
        f.write("\n" + "=" * 80 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 80 + "\n")
        
        # Count files by type
        file_counts = {}
        total_files = 0
        
        for root, dirs, files in os.walk(project_root):
            # Skip hidden/system directories
            dirs[:] = [d for d in dirs if not should_skip_file(d)]
            
            for file in files:
                if not should_skip_file(file):
                    total_files += 1
                    _, ext = os.path.splitext(file)
                    ext = ext.lower()
                    file_counts[ext] = file_counts.get(ext, 0) + 1
        
        f.write(f"Total Files: {total_files}\n\n")
        f.write("File Types:\n")
        
        for ext, count in sorted(file_counts.items(), key=lambda x: x[1], reverse=True):
            ext_display = ext if ext else "(no extension)"
            f.write(f"  {ext_display}: {count} files\n")
        
        # Look for specific project files
        f.write("\nKey Project Files Found:\n")
        key_files = [
            'requirements.txt', 'environment.yml', 'config.toml',
            'dashboard_metric_loader.py', 'fully_integrated_dashboard.py',
            'metric_registry.py', 'generate_all_cio_metrics.py'
        ]
        
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if not should_skip_file(d)]
            
            for file in files:
                if file in key_files:
                    rel_path = os.path.relpath(os.path.join(root, file), project_root)
                    f.write(f"  ✓ {rel_path}\n")
    
    print(f"\n✅ Project structure mapped successfully!")
    print(f"📁 Output saved to: {output_filename}")
    print(f"📏 You can now share this file to show your project structure")
    
    # Also print first few lines to console
    print(f"\n📋 Preview of structure:")
    with open(output_filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[:20]:  # Show first 20 lines
            print(line.rstrip())
    
    if len(lines) > 20:
        print("... (truncated, see full output in file)")

if __name__ == "__main__":
    main()
    
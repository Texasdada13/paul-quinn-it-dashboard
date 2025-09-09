#!/usr/bin/env python3
"""
Fixed Dashboard Comparison Tool
Automatically finds your dashboard files regardless of where you run it from
"""

import difflib
import os
from pathlib import Path

def find_dashboard_files():
    """Find the dashboard files automatically"""
    
    # Possible locations to check
    locations = [
        Path("."),  # Current directory
        Path("src/dashboard"),  # Standard location
        Path("../dashboard"),  # If running from src
        Path("../../dashboard"),  # If running from deeper
    ]
    
    files_found = {}
    
    for location in locations:
        if location.exists():
            # Look for the dashboard files
            main_file = location / "fully_integrated_dashboard.py"
            ai_file = location / "withAI_Updates_fully_integrated_dashboard.py"
            
            if main_file.exists():
                files_found['main'] = main_file
            if ai_file.exists():
                files_found['ai'] = ai_file
    
    return files_found

def list_available_files():
    """List all Python files we can find"""
    print("📁 Searching for Python files...")
    
    locations = [Path("."), Path("src/dashboard")]
    
    for location in locations:
        if location.exists():
            print(f"\n📂 In {location}:")
            py_files = list(location.glob("*.py"))
            if py_files:
                for f in py_files:
                    print(f"   - {f.name}")
            else:
                print("   (no .py files found)")

def quick_compare(file1_path: Path, file2_path: Path):
    """Show side-by-side differences between two files"""
    
    print(f"📊 Comparing:")
    print(f"   File 1: {file1_path}")
    print(f"   File 2: {file2_path}")
    
    # Read files
    try:
        content1 = file1_path.read_text(encoding='utf-8').splitlines()
        content2 = file2_path.read_text(encoding='utf-8').splitlines()
    except Exception as e:
        print(f"❌ Error reading files: {e}")
        return
    
    # Create HTML diff
    diff = difflib.HtmlDiff()
    html_diff = diff.make_file(
        content1, content2,
        fromdesc=str(file1_path),
        todesc=str(file2_path),
        context=True,
        numlines=3
    )
    
    # Save HTML comparison
    output_file = Path("dashboard_comparison.html")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_diff)
    
    print(f"✅ Comparison saved to: {output_file.absolute()}")
    print("🌐 Open in browser to see visual differences")
    
    # Also show key differences in terminal
    print("\n📊 Key Differences Found:")
    print("=" * 50)
    
    differ = difflib.unified_diff(
        content1, content2,
        fromfile=str(file1_path),
        tofile=str(file2_path),
        lineterm='',
        n=1
    )
    
    ai_related = []
    all_additions = []
    
    for line in differ:
        if line.startswith('+') and not line.startswith('+++'):
            addition = line[1:].strip()
            all_additions.append(addition)
            
            if any(keyword in addition.lower() for keyword in ['ai', 'optimization', 'intelligence', 'strategic']):
                ai_related.append(addition)
    
    print(f"📈 Total additions in AI file: {len(all_additions)}")
    
    if ai_related:
        print(f"🤖 AI-related additions found: {len(ai_related)}")
        for i, line in enumerate(ai_related[:10], 1):  # Show first 10
            print(f"  {i}. {line[:80]}...")  # Truncate long lines
        
        if len(ai_related) > 10:
            print(f"  ... and {len(ai_related) - 10} more AI-related lines")
    else:
        print("ℹ️  No obvious AI-related differences found in quick scan")
    
    # Show some sample additions
    if all_additions:
        print(f"\n📝 Sample additions (first 5):")
        for i, line in enumerate(all_additions[:5], 1):
            print(f"  {i}. {line[:80]}...")

def main():
    """Main function"""
    print("🔄 Dashboard Comparison Tool")
    print("=" * 50)
    
    # Find files
    files_found = find_dashboard_files()
    
    if 'main' not in files_found:
        print("❌ Cannot find 'fully_integrated_dashboard.py'")
        list_available_files()
        return
    
    if 'ai' not in files_found:
        print("❌ Cannot find 'withAI_Updates_fully_integrated_dashboard.py'")
        list_available_files()
        return
    
    # Compare the files
    quick_compare(files_found['main'], files_found['ai'])

if __name__ == "__main__":
    main()
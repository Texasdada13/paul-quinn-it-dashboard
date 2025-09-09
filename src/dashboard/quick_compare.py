#!/usr/bin/env python3
"""
Quick Dashboard Comparison Tool
Simple script to show what's different between your two dashboard files
"""

import difflib
from pathlib import Path

def quick_compare(file1: str, file2: str):
    """Show side-by-side differences between two files"""
    
    # Read files
    content1 = Path(file1).read_text().splitlines()
    content2 = Path(file2).read_text().splitlines()
    
    # Create HTML diff
    diff = difflib.HtmlDiff()
    html_diff = diff.make_file(
        content1, content2,
        fromdesc=file1,
        todesc=file2,
        context=True,
        numlines=3
    )
    
    # Save HTML comparison
    with open('dashboard_comparison.html', 'w') as f:
        f.write(html_diff)
    
    print("✅ Comparison saved to: dashboard_comparison.html")
    print("🌐 Open in browser to see visual differences")
    
    # Also show key differences in terminal
    print("\n📊 Key Differences Found:")
    print("=" * 50)
    
    differ = difflib.unified_diff(
        content1, content2,
        fromfile=file1,
        tofile=file2,
        lineterm='',
        n=1
    )
    
    ai_related = []
    for line in differ:
        if line.startswith('+') and any(keyword in line.lower() for keyword in ['ai', 'optimization', 'intelligence']):
            ai_related.append(line[1:].strip())
    
    if ai_related:
        print("🤖 AI-related additions found:")
        for i, line in enumerate(ai_related[:10], 1):  # Show first 10
            print(f"  {i}. {line}")
        
        if len(ai_related) > 10:
            print(f"  ... and {len(ai_related) - 10} more")
    else:
        print("ℹ️  No obvious AI-related differences found in quick scan")

if __name__ == "__main__":
    # Auto-detect file locations
    import os
    
    # Check if we're in the right directory
    dashboard_dir = Path("src/dashboard") if Path("src/dashboard").exists() else Path(".")
    
    file1 = dashboard_dir / "fully_integrated_dashboard.py"
    file2 = dashboard_dir / "withAI_Updates_fully_integrated_dashboard.py"
    
    # Verify files exist
    if not file1.exists():
        print(f"❌ Cannot find: {file1}")
        print("📁 Available files:")
        for f in dashboard_dir.glob("*.py"):
            print(f"   - {f.name}")
        exit(1)
    
    if not file2.exists():
        print(f"❌ Cannot find: {file2}")
        print("📁 Available files:")
        for f in dashboard_dir.glob("*.py"):
            print(f"   - {f.name}")
        exit(1)
    
    quick_compare(str(file1), str(file2))
#!/usr/bin/env python3
"""
Copy AI Modules from withAI setup to your preferred dashboard
Simple file copying approach
"""

import shutil
from pathlib import Path

def copy_ai_modules():
    """Copy the AI modules that make 8504 work"""
    
    print("📋 Copying AI modules for full functionality...")
    
    # Files we need to copy to get 8504's features working in 8505
    files_to_copy = [
        # The enhanced metric registry (this is key!)
        "withAI_metric_registry.py",
        
        # AI optimization modules (if they exist)
        "ai_optimization_engine.py",
        "metric_intelligence.py"
    ]
    
    copied_files = []
    missing_files = []
    
    for file_name in files_to_copy:
        source_file = Path(file_name)
        
        if source_file.exists():
            # Make a backup first
            backup_name = f"{file_name}_original_backup"
            if Path(backup_name).exists():
                print(f"⚠️  Backup already exists: {backup_name}")
            else:
                try:
                    if Path(file_name.replace("withAI_", "")).exists():
                        shutil.copy2(file_name.replace("withAI_", ""), backup_name)
                        print(f"📦 Backup created: {backup_name}")
                except:
                    pass
            
            copied_files.append(file_name)
            print(f"✅ Found: {file_name}")
        else:
            missing_files.append(file_name)
            print(f"❌ Missing: {file_name}")
    
    return copied_files, missing_files

def update_dashboard_imports():
    """Update the dashboard to use the withAI modules"""
    
    dashboard_file = Path("fully_integrated_dashboard_with_AI.py")
    
    if not dashboard_file.exists():
        print("❌ Dashboard file not found")
        return False
    
    content = dashboard_file.read_text(encoding='utf-8')
    
    # Replace the import line to use withAI_metric_registry instead
    old_import = "from metric_registry import metric_registry, cfo_metrics, cio_metrics, cto_metrics"
    new_import = "from withAI_metric_registry import metric_registry, cfo_metrics, cio_metrics, cto_metrics"
    
    if old_import in content:
        content = content.replace(old_import, new_import)
        print("✅ Updated import to use withAI_metric_registry")
    else:
        print("⚠️  Import line not found - may already be updated")
    
    # Save the updated file
    dashboard_file.write_text(content, encoding='utf-8')
    print(f"✅ Updated: {dashboard_file}")
    return True

def main():
    """Main execution"""
    print("🔄 AI Module Copy Process")
    print("=" * 40)
    
    # Step 1: Copy AI modules
    copied, missing = copy_ai_modules()
    
    if not copied:
        print("\n❌ No AI modules found to copy")
        print("Make sure you're running this in the same directory as withAI_metric_registry.py")
        return
    
    # Step 2: Update dashboard imports
    print(f"\n🔗 Updating dashboard imports...")
    if update_dashboard_imports():
        print("✅ Dashboard updated successfully")
    else:
        print("❌ Failed to update dashboard")
        return
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"✅ Copied {len(copied)} AI modules")
    if missing:
        print(f"⚠️  Missing {len(missing)} optional modules")
    
    print(f"\n🚀 Next steps:")
    print(f"1. Restart your dashboard: streamlit run fully_integrated_dashboard_with_AI.py --server.port 8505")
    print(f"2. Check CTO section for the advanced visualizations")
    print(f"3. If you get import errors, the missing modules need to be created")

if __name__ == "__main__":
    main()
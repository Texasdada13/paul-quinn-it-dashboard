#!/usr/bin/env python3
"""
Fix AI Imports and Flags
Add missing AI imports and flags to enable full AI functionality
"""

from pathlib import Path

def fix_ai_imports():
    """Add missing AI imports and flags to the dashboard"""
    
    dashboard_file = Path("fully_integrated_dashboard_with_AI.py")
    
    if not dashboard_file.exists():
        print("❌ fully_integrated_dashboard_with_AI.py not found")
        return False
    
    print("🔧 Fixing AI imports and flags...")
    
    with open(dashboard_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if AI imports already exist
    if 'AI_FEATURES_AVAILABLE' in content:
        print("ℹ️  AI features flag already exists")
        if 'OptimizationDashboard' in content:
            print("ℹ️  OptimizationDashboard import already exists")
            print("✅ AI imports appear to be already configured")
            return True
    
    # Add missing AI imports after the HBCU integration block
    ai_import_block = '''
# AI Enhancement imports
try:
    from ai_optimization_engine import OptimizationDashboard, AIOptimizationEngine
    from metric_intelligence import MetricIntelligenceEngine, analyze_single_metric
    AI_FEATURES_AVAILABLE = True
    print("AI optimization features loaded successfully")
except ImportError as e:
    print(f"AI features not available: {e}")
    AI_FEATURES_AVAILABLE = False
'''
    
    # Find where to insert (after HBCU_INTEGRATION_AVAILABLE section)
    insert_point = content.find('print(f"HBCU_INTEGRATION_AVAILABLE: {HBCU_INTEGRATION_AVAILABLE}")')
    
    if insert_point != -1:
        # Find the end of that line
        insert_point = content.find('\n', insert_point) + 1
        content = content[:insert_point] + ai_import_block + content[insert_point:]
        print("✅ Added AI imports and flags after HBCU section")
    else:
        # Fallback: add after page configuration
        insert_point = content.find('st.set_page_config(')
        if insert_point != -1:
            # Find the end of the page config block
            insert_point = content.find(')', insert_point) + 1
            insert_point = content.find('\n', insert_point) + 1
            content = content[:insert_point] + ai_import_block + content[insert_point:]
            print("✅ Added AI imports and flags after page config")
        else:
            print("❌ Could not find suitable insertion point")
            return False
    
    # Save the updated file
    with open(dashboard_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Dashboard updated: {dashboard_file}")
    return True

def verify_ai_setup():
    """Verify that AI modules are available"""
    print("\n🔍 Verifying AI module availability...")
    
    modules_to_check = [
        "ai_optimization_engine.py",
        "metric_intelligence.py", 
        "withAI_metric_registry.py"
    ]
    
    all_found = True
    for module in modules_to_check:
        if Path(module).exists():
            print(f"✅ Found: {module}")
        else:
            print(f"❌ Missing: {module}")
            all_found = False
    
    return all_found

def main():
    """Main execution"""
    print("🚀 AI Import Fixer")
    print("=" * 30)
    
    # Verify AI modules exist
    if not verify_ai_setup():
        print("\n⚠️  Some AI modules are missing")
        print("Make sure you've run the copy_ai_modules.py script first")
        return
    
    # Fix the imports
    if fix_ai_imports():
        print("\n✅ AI imports fixed successfully!")
        print("\n📋 Next steps:")
        print("1. Restart your dashboard:")
        print("   streamlit run fully_integrated_dashboard_with_AI.py --server.port 8505")
        print("2. Check that AI tabs now show 'AI optimization features loaded successfully'")
        print("3. Go to CTO > AI Operations tab to see advanced visualizations")
        print("\n💡 The AI Operations tab should now have:")
        print("   - AI-powered infrastructure analysis")
        print("   - Asset lifecycle management")
        print("   - Capacity planning metrics")
        print("   - Performance optimization recommendations")
    else:
        print("\n❌ Failed to fix AI imports")
        print("Check the dashboard file structure and try again")

if __name__ == "__main__":
    main()
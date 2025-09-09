#!/usr/bin/env python3
"""
Dashboard Structure Analysis
"""

def analyze_dashboard():
    """Analyze the current dashboard structure"""
    
    try:
        with open("fully_integrated_dashboard_with_AI.py", 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ fully_integrated_dashboard_with_AI.py not found")
        return
    
    print("🔍 Dashboard Structure Analysis")
    print("=" * 40)
    
    # Find all tab names
    import re
    tabs = re.findall(r'elif tab_name == "(.*?)":', content)
    print(f"📋 Found {len(tabs)} tabs:")
    for i, tab in enumerate(tabs, 1):
        print(f"  {i}. {tab}")
    
    # Find CTO section
    cto_start = content.find('elif persona == "CTO - Technology Operator":')
    cto_end = content.find('elif persona == "Project Manager View":')
    
    if cto_start != -1 and cto_end != -1:
        cto_section = content[cto_start:cto_end]
        print(f"\n🖥️ CTO section found ({len(cto_section)} characters)")
        
        # Find CTO tabs
        cto_tabs = re.findall(r'"([^"]*)".*?\[\]', cto_section)
        print(f"📊 CTO tabs found:")
        for tab in cto_tabs:
            if any(keyword in tab for keyword in ['Infrastructure', 'Cloud', 'AI', 'Security', 'All']):
                print(f"  - {tab}")
    else:
        print("❌ CTO section not found")
    
    # Check for AI-related content
    ai_mentions = content.count('AI')
    optimization_mentions = content.count('optimization')
    print(f"\n🤖 AI references: {ai_mentions}")
    print(f"⚙️ Optimization references: {optimization_mentions}")
    
    # Check import statements
    if 'AI_FEATURES_AVAILABLE' in content:
        print("✅ AI features flag found")
    else:
        print("❌ AI features flag not found")
    
    if 'OptimizationDashboard' in content:
        print("✅ OptimizationDashboard import found")
    else:
        print("❌ OptimizationDashboard import not found")

if __name__ == "__main__":
    analyze_dashboard()
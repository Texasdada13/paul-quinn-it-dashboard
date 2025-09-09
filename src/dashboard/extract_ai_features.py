#!/usr/bin/env python3
"""
Targeted AI Feature Extractor
Extracts specific AI optimization tabs from withAI_Updates file
"""

import re
from pathlib import Path

def extract_ai_tabs():
    """Extract AI optimization tab content from your withAI file"""
    
    # Read your withAI file
    ai_file = Path("src/dashboard/withAI_Updates_fully_integrated_dashboard.py")
    if not ai_file.exists():
        ai_file = Path("withAI_Updates_fully_integrated_dashboard.py")
    
    if not ai_file.exists():
        print("❌ Cannot find withAI_Updates_fully_integrated_dashboard.py")
        return
    
    content = ai_file.read_text(encoding='utf-8')
    
    # Extract AI imports
    ai_imports = """# AI Enhancement imports
try:
    from ai_optimization_engine import OptimizationDashboard, AIOptimizationEngine
    from metric_intelligence import MetricIntelligenceEngine, analyze_single_metric
    AI_FEATURES_AVAILABLE = True
    print("AI optimization features loaded successfully")
except ImportError as e:
    print(f"AI features not available: {e}")
    AI_FEATURES_AVAILABLE = False"""
    
    # Extract CFO AI tab content
    cfo_ai_pattern = r'elif tab_name == "🤖 AI Optimization":(.*?)elif tab_name == "🏛️ Grant Compliance":'
    cfo_match = re.search(cfo_ai_pattern, content, re.DOTALL)
    cfo_ai_content = cfo_match.group(1).strip() if cfo_match else ""
    
    # Extract CIO AI tab content  
    cio_ai_pattern = r'elif tab_name == "🤖 AI Strategic Optimization":(.*?)elif tab_name == "📊 Performance & Risk":'
    cio_match = re.search(cio_ai_pattern, content, re.DOTALL)
    cio_ai_content = cio_match.group(1).strip() if cio_match else ""
    
    # Extract CTO AI tab content
    cto_ai_pattern = r'elif tab_name == "🤖 AI Operational Optimization":(.*?)elif tab_name == "🔒 Security & Quality":'
    cto_match = re.search(cto_ai_pattern, content, re.DOTALL)
    cto_ai_content = cto_match.group(1).strip() if cto_match else ""
    
    return {
        'imports': ai_imports,
        'cfo_tab': cfo_ai_content,
        'cio_tab': cio_ai_content, 
        'cto_tab': cto_ai_content
    }

def create_ai_component(ai_content):
    """Create standalone AI component file"""
    
    component_code = f'''"""
AI Optimization Component for Paul Quinn College Dashboard
Extracted from withAI_Updates_fully_integrated_dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

{ai_content['imports']}

def render_cfo_ai_optimization():
    """Render CFO AI Optimization tab"""
    {ai_content['cfo_tab']}

def render_cio_ai_optimization():
    """Render CIO AI Strategic Optimization tab"""
    {ai_content['cio_tab']}

def render_cto_ai_optimization():
    """Render CTO AI Operational Optimization tab"""
    {ai_content['cto_tab']}

def render_ai_tab_for_persona(persona):
    """Main function to render AI tab based on persona"""
    if persona == 'cfo':
        render_cfo_ai_optimization()
    elif persona == 'cio':
        render_cio_ai_optimization()
    elif persona == 'cto':
        render_cto_ai_optimization()
    else:
        st.info("AI optimization not available for this persona")

if __name__ == "__main__":
    st.title("AI Optimization Component Test")
    persona = st.selectbox("Select Persona", ["cfo", "cio", "cto"])
    render_ai_tab_for_persona(persona)
'''
    
    # Save component
    with open("ai_optimization_component.py", 'w', encoding='utf-8') as f:
        f.write(component_code)
    
    print("✅ AI component created: ai_optimization_component.py")
    return "ai_optimization_component.py"

def integrate_ai_into_main():
    """Integrate AI tabs into your main dashboard"""
    
    # Read your main file
    main_file = Path("src/dashboard/fully_integrated_dashboard.py")
    if not main_file.exists():
        main_file = Path("fully_integrated_dashboard.py")
    
    if not main_file.exists():
        print("❌ Cannot find fully_integrated_dashboard.py")
        return
    
    content = main_file.read_text(encoding='utf-8')
    
    # 1. Add AI import at the top
    ai_import_line = "from ai_optimization_component import render_ai_tab_for_persona"
    
    # Find where to insert import (after existing imports)
    import_insertion = content.find('# Initialize session state')
    if import_insertion == -1:
        import_insertion = content.find('st.set_page_config')
    
    content = content[:import_insertion] + ai_import_line + "\n\n" + content[import_insertion:]
    
    # 2. Add AI tabs to each persona
    # CFO AI tab
    cfo_tab_addition = ', "🤖 AI Optimization"'
    cfo_pattern = r'("📃 Contracts & Vendors", \[.*?\])'
    content = re.sub(r'("📃 Contracts & Vendors", \[.*?\])', 
                    r'\1,\n            ("🤖 AI Optimization", []),', content)
    
    # CIO AI tab
    content = re.sub(r'("💼 Business Analysis", \[.*?\])', 
                    r'\1,\n            ("🤖 AI Strategic Optimization", []),', content)
    
    # CTO AI tab  
    content = re.sub(r'("☁️ Cloud & Assets", \[.*?\])', 
                    r'\1,\n            ("🤖 AI Operational Optimization", []),', content)
    
    # 3. Add AI tab handling for each persona
    ai_tab_handlers = '''
                elif tab_name == "🤖 AI Optimization":
                    render_ai_tab_for_persona('cfo')
                
                elif tab_name == "🤖 AI Strategic Optimization":
                    render_ai_tab_for_persona('cio')
                
                elif tab_name == "🤖 AI Operational Optimization":
                    render_ai_tab_for_persona('cto')'''
    
    # Insert AI handlers before the "All Metrics" tab
    content = re.sub(r'(elif tab_name == "📋 All Metrics":)', 
                    ai_tab_handlers + r'\n                \1', content)
    
    # Save updated file
    output_file = "fully_integrated_dashboard_with_AI.py"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated dashboard created: {output_file}")
    return output_file

def main():
    """Main execution"""
    print("🤖 AI Feature Extractor for Paul Quinn Dashboard")
    print("=" * 55)
    
    # Extract AI content
    print("🔍 Extracting AI features...")
    ai_content = extract_ai_tabs()
    
    if not ai_content or not ai_content['cfo_tab']:
        print("❌ Could not extract AI content")
        return
    
    print("✅ AI features extracted successfully")
    print(f"   - CFO AI tab: {len(ai_content['cfo_tab'])} characters")
    print(f"   - CIO AI tab: {len(ai_content['cio_tab'])} characters") 
    print(f"   - CTO AI tab: {len(ai_content['cto_tab'])} characters")
    
    # Create AI component
    print("\n🔧 Creating AI component...")
    component_file = create_ai_component(ai_content)
    
    # Integrate into main dashboard
    print("\n🔗 Integrating into main dashboard...")
    integrated_file = integrate_ai_into_main()
    
    print("\n✅ Integration complete!")
    print(f"📁 Files created:")
    print(f"   - {component_file} (standalone AI component)")
    print(f"   - {integrated_file} (integrated dashboard)")
    print(f"\n🚀 Test with:")
    print(f"   streamlit run {integrated_file}")
    print(f"   streamlit run {component_file}")

if __name__ == "__main__":
    main()
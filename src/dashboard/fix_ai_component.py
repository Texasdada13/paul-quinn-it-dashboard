#!/usr/bin/env python3
"""
Quick fix for the AI component indentation issue
"""

def fix_ai_component():
    """Fix the indentation in ai_optimization_component.py"""
    
    # Create a clean, working AI component
    clean_component = '''"""
AI Optimization Component for Paul Quinn College Dashboard
Extracted from withAI_Updates_fully_integrated_dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# AI Enhancement imports
try:
    from ai_optimization_engine import OptimizationDashboard, AIOptimizationEngine
    from metric_intelligence import MetricIntelligenceEngine, analyze_single_metric
    AI_FEATURES_AVAILABLE = True
    print("AI optimization features loaded successfully")
except ImportError as e:
    print(f"AI features not available: {e}")
    AI_FEATURES_AVAILABLE = False

def render_cfo_ai_optimization():
    """Render CFO AI Optimization tab"""
    if AI_FEATURES_AVAILABLE:
        st.markdown("### AI-Powered Financial Optimization")
        
        # Create demo data for AI analysis
        cfo_ai_data = {
            'contract_data': pd.DataFrame({
                'Vendor': ['Microsoft', 'Adobe', 'AWS', 'Microsoft', 'Salesforce'],
                'Annual Spend': [150000, 80000, 200000, 90000, 120000],
                'Days Until Expiry': [45, 120, 200, 30, 180]
            }),
            'budget_data': pd.DataFrame({
                'Budget Category': ['Software', 'Hardware', 'Cloud', 'Consulting'],
                'Initial Budget': [500000, 300000, 400000, 200000],
                'Actual Spend': [420000, 280000, 450000, 160000]
            })
        }
        
        # Render AI optimization dashboard
        optimization_dashboard = OptimizationDashboard()
        optimization_dashboard.render_optimization_dashboard('cfo', cfo_ai_data)
        
    else:
        st.warning("AI features not available. Please install required AI modules.")
        
        # Show demo content
        st.markdown("#### Demo: AI Optimization Potential")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Potential Savings", "$450K", "+15%")
        with col2:
            st.metric("Optimization Score", "8.2/10", "+0.8")
        with col3:
            st.metric("AI Confidence", "87%", "+5%")

def render_cio_ai_optimization():
    """Render CIO AI Strategic Optimization tab"""
    st.markdown("### AI-Powered Strategic Optimization")
    st.info("CIO AI optimization features coming soon...")

def render_cto_ai_optimization():
    """Render CTO AI Operational Optimization tab"""
    st.markdown("### AI-Powered Operational Optimization")
    st.info("CTO AI optimization features coming soon...")

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
    
    # Save the fixed component
    with open("ai_optimization_component.py", 'w', encoding='utf-8') as f:
        f.write(clean_component)
    
    print("✅ Fixed ai_optimization_component.py")

if __name__ == "__main__":
    fix_ai_component()
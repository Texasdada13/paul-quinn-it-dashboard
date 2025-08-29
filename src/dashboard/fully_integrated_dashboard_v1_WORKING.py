"""
Paul Quinn College IT Analytics Suite - Fully Integrated Dashboard
Dynamically loads and displays all metrics from the metrics folder
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os
import sys

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our metric registry and loader
try:
    from metric_registry import metric_registry, cfo_metrics, cio_metrics, cto_metrics
    from dashboard_metric_loader import dashboard_loader, PM_METRICS_AVAILABLE, PM_METRICS
    METRICS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import metric modules: {e}")
    METRICS_AVAILABLE = False
    PM_METRICS_AVAILABLE = False
    PM_METRICS = {}

try:
    from hbcu_metrics_integration import HBCUMetricsIntegrator, integrate_hbcu_metrics_into_persona
    HBCU_INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import HBCU integration: {e}")
    HBCU_INTEGRATION_AVAILABLE = False
    
print(f"HBCU_INTEGRATION_AVAILABLE: {HBCU_INTEGRATION_AVAILABLE}")

# Page configuration
st.set_page_config(
    page_title="PQC IT Analytics Suite - Fully Integrated",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1e3d59;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: 600;
    }
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .integrated-badge {
        background-color: #17a2b8;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    .metric-available {
        color: #28a745;
        font-weight: bold;
    }
    .metric-unavailable {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_persona' not in st.session_state:
    st.session_state.current_persona = 'CFO'

if 'metrics_loaded' not in st.session_state:
    st.session_state.metrics_loaded = False
    
# Initialize HBCU integrator
if HBCU_INTEGRATION_AVAILABLE:
    hbcu_integrator = HBCUMetricsIntegrator()
else:
    hbcu_integrator = None


# Sidebar navigation
st.sidebar.markdown("### 🎓 Paul Quinn College")
st.sidebar.markdown("**IT Analytics Suite**")
st.sidebar.markdown("<span class='integrated-badge'>FULLY INTEGRATED</span>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Persona selection
persona = st.sidebar.selectbox(
    "Select Persona View",
    [
        "CFO - Financial Steward", 
        "CIO - Strategic Partner", 
        "CTO - Technology Operator", 
        "Project Manager View",
        "HBCU Institutional View"
    ]
)

# Extract persona key
persona_key = persona.split(' - ')[0].lower()

# Display metrics availability
if METRICS_AVAILABLE:
    st.sidebar.markdown("### 📊 Metrics Status")
    available_metrics = metric_registry.get_available_metrics(persona_key)
    st.sidebar.markdown(f"<span class='metric-available'>✅ {len(available_metrics)} metrics loaded</span>", 
                       unsafe_allow_html=True)
else:
    st.sidebar.markdown("<span class='metric-unavailable'>⚠️ Metrics not loaded</span>", 
                       unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Actions")

# Refresh metrics button
if st.sidebar.button("🔄 Refresh Metrics"):
    if METRICS_AVAILABLE:
        # Force reload of metrics
        metric_registry._discover_metrics()
        st.sidebar.success("Metrics refreshed!")
        st.rerun()
    else:
        st.sidebar.error("Metric system not available")

if st.sidebar.button("📊 Generate Report"):
    st.sidebar.success("Report generated!")

if st.sidebar.button("📧 Email Dashboard"):
    st.sidebar.success("Dashboard emailed!")

# Add HBCU quick stats
if HBCU_INTEGRATION_AVAILABLE and hbcu_integrator:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### HBCU Quick Stats")
    
    col1 = st.sidebar.columns(1)[0]
    with col1:
        st.metric("Students Served", "5,800", "↑ 3.2%")
        st.metric("Cost/Student", "$8,224", "↓ $426") 
        st.metric("Grant Compliance", "94%", "↑ 2%")
        st.metric("Tech Graduation", "78%", "↑ 5%")


# Main content
st.markdown("<h1 class='main-header'>🎓 Paul Quinn College IT Analytics Suite <span class='integrated-badge'>FULLY INTEGRATED</span></h1>", 
           unsafe_allow_html=True)

# Display content based on persona
if persona == "CFO - Financial Steward":
    st.markdown("### CFO Dashboard - Financial Overview & Optimization")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    # Try to load actual metrics for the summary
    if METRICS_AVAILABLE:
        budget_data, _ = cfo_metrics.get_budget_variance_data()
        contract_data, _ = cfo_metrics.get_contract_alerts()
        
        if budget_data is not None:
            total_budget = budget_data['Initial Budget'].sum()
            total_actual = budget_data['Actual Spend'].sum()
            variance_pct = ((total_actual - total_budget) / total_budget * 100) if total_budget > 0 else 0
        else:
            total_budget = 2800000
            variance_pct = 5.2
        
        if contract_data is not None:
            at_risk_contracts = len(contract_data[contract_data['Days Until Expiry'] < 90])
        else:
            at_risk_contracts = 3
    else:
        total_budget = 2800000
        variance_pct = 5.2
        at_risk_contracts = 3
    
    with col1:
        st.metric("Total IT Budget", f"${total_budget/1000000:.1f}M", f"{variance_pct:+.1f}%", 
                 help="Year-over-year change")
    with col2:
        st.metric("YTD Spend", "$1.9M", "-3%", help="68% of annual budget")
    with col3:
        st.metric("Cost Savings", "$340K", "+12%", help="Through optimization initiatives")
    with col4:
        st.metric("Contracts at Risk", at_risk_contracts, delta_color="inverse", 
                 help="Expiring within 90 days")
    
    # Dynamic tabs based on available metrics
    if METRICS_AVAILABLE and persona_key in ['cfo']:
        # CFO-specific tab configuration
        tab_config = [
            ("📊 Budget Analysis", ["cfo_budget_vs_actual", "cfo_total_it_spend_breakdown"]),
            ("📃 Contracts & Vendors", ["cfo_contract_expiration_alerts", "cfo_vendor_spend_optimization"]),
            ("🏛️ Grant Compliance", ["cfo_grant_compliance"]),
            ("📈 ROI & Benchmarking", ["cfo_student_success_roi", "cfo_hbcu_peer_benchmarking"]),
            ("📋 All Metrics", [])  # Will show all available metrics
        ]
        
        tab_names = [config[0] for config in tab_config]
        tabs = st.tabs(tab_names)
        
        # Display content in each tab
        for idx, (tab, (tab_name, metrics_list)) in enumerate(zip(tabs, tab_config)):
            with tab:
                if tab_name == "📊 Budget Analysis":
                    # Budget variance analysis
                    if "cfo_budget_vs_actual" in available_metrics:
                        dashboard_loader.display_cfo_budget_variance(st.container())
                    else:
                        st.info("Budget variance metrics not available")
                    
                    # Total IT spend breakdown
                    if "cfo_total_it_spend_breakdown" in available_metrics:
                        st.markdown("---")
                        dashboard_loader.display_generic_metric('cfo', 'cfo_total_it_spend_breakdown', st.container())
                
                elif tab_name == "📃 Contracts & Vendors":
                    # Contract expiration alerts
                    if "cfo_contract_expiration_alerts" in available_metrics:
                        dashboard_loader.display_cfo_contract_alerts(st.container())
                    else:
                        st.info("Contract expiration metrics not available")
                    
                    # Vendor spend optimization
                    if "cfo_vendor_spend_optimization" in available_metrics:
                        st.markdown("---")
                        dashboard_loader.display_generic_metric('cfo', 'cfo_vendor_spend_optimization', st.container())
                
                elif tab_name == "🏛️ Grant Compliance":
                    if "cfo_grant_compliance" in available_metrics:
                        dashboard_loader.display_cfo_grant_compliance(st.container())
                    else:
                        st.info("Grant compliance metrics not available")
                
                elif tab_name == "📈 ROI & Benchmarking":
                    col1, col2 = st.columns(2)
                    with col1:
                        if "cfo_student_success_roi" in available_metrics:
                            dashboard_loader.display_generic_metric('cfo', 'cfo_student_success_roi', st.container())
                    with col2:
                        if "cfo_hbcu_peer_benchmarking" in available_metrics:
                            dashboard_loader.display_generic_metric('cfo', 'cfo_hbcu_peer_benchmarking', st.container())
                
                elif tab_name == "📋 All Metrics":
                    dashboard_loader.display_metric_summary('cfo')
                    
                    # Display all available metrics
                    st.markdown("---")
                    st.subheader("All Available CFO Metrics")
                    
                    # Define metrics already shown in other tabs
                    shown_metrics = [
                        "cfo_budget_vs_actual", "cfo_total_it_spend_breakdown",
                        "cfo_contract_expiration_alerts", "cfo_vendor_spend_optimization",
                        "cfo_grant_compliance", "cfo_student_success_roi", "cfo_hbcu_peer_benchmarking"
                    ]
                    
                    # Only show metrics not already displayed

                    for metric in available_metrics:
                        if metric not in shown_metrics:
                            with st.expander(f"📊 {metric.replace('_', ' ').title()}"):
                                dashboard_loader.display_generic_metric('cfo', metric, st.container())
    else:
        # Fallback to static content if metrics not available
        st.warning("Metric system not available. Showing demo content.")
        tabs = st.tabs(["📊 Budget Analysis", "💰 Cost Optimization", "📈 Benchmarking", "📑 Reports"])

    if HBCU_INTEGRATION_AVAILABLE and hbcu_integrator:
        st.markdown("---")
        hbcu_integrator.render_hbcu_dashboard_section('cfo')
        
elif persona == "CIO - Strategic Partner":
    st.markdown("### CIO Dashboard - Strategic IT Portfolio Management")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Digital Transformation", "65%", "+15%", help="Progress on digital initiatives")
    with col2:
        st.metric("Project Success Rate", "87%", "+5%", help="Projects completed on time/budget")
    with col3:
        st.metric("Innovation Index", "7.8/10", "+0.6", help="Innovation maturity score")
    with col4:
        st.metric("Business Alignment", "92%", "+3%", help="IT-Business alignment score")
    
    # Dynamic tabs for CIO
    if METRICS_AVAILABLE and persona_key == 'cio':
        tab_config = [
            ("🎯 Strategic Portfolio", ["digital_transformation_metrics", "strategic_alignment_metrics"]),
            ("💼 Business Analysis", ["business_unit_it_spend", "app_cost_analysis_metrics"]),
            ("📊 Performance & Risk", ["risk_metrics", "vendor_metrics"]),
            ("📋 All Metrics", [])
        ]
        
        tab_names = [config[0] for config in tab_config]
        tabs = st.tabs(tab_names)
        
        available_cio_metrics = metric_registry.get_available_metrics('cio')
        
        for tab, (tab_name, metrics_list) in zip(tabs, tab_config):
            with tab:
                if tab_name == "📋 All Metrics":
                    dashboard_loader.display_metric_summary('cio')
                    st.markdown("---")
                    
                    for metric in available_cio_metrics:
                        with st.expander(f"📊 {metric.replace('_', ' ').title()}"):
                            dashboard_loader.display_generic_metric('cio', metric, st.container())
                else:
                    for metric in metrics_list:
                        if metric in available_cio_metrics:
                            dashboard_loader.display_generic_metric('cio', metric, st.container())
                            st.markdown("---")

    # Add this after your existing CIO tabs
    if HBCU_INTEGRATION_AVAILABLE and hbcu_integrator:
        st.markdown("---")
        hbcu_integrator.render_hbcu_dashboard_section('cio')
        
elif persona == "CTO - Technology Operator":
    st.markdown("### CTO Dashboard - Technical Operations & Infrastructure")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("System Uptime", "99.8%", "+0.2%", help="Last 30 days")
    with col2:
        st.metric("Incident Resolution", "2.4 hrs", "-0.6 hrs", help="Average resolution time")
    with col3:
        st.metric("Cloud Utilization", "78%", "+5%", help="Resource utilization")
    with col4:
        st.metric("Security Score", "A-", "↑", help="Security posture rating")
    
    # Dynamic tabs for CTO
    if METRICS_AVAILABLE and persona_key == 'cto':
        tab_config = [
            ("🖥️ Infrastructure", ["infrastructure_performance_metrics", "system_utilization_metrics"]),
            ("☁️ Cloud & Assets", ["cloud_cost_optimization_metrics", "asset_lifecycle_management_metrics", 
                                  "capacity_planning_metrics"]),
            ("🔒 Security & Quality", ["security_metrics_and_response", "technical_debt_metrics", 
                                      "tech_stack_health_metrics"]),
            ("📋 All Metrics", [])
        ]
        
        tab_names = [config[0] for config in tab_config]
        tabs = st.tabs(tab_names)
        
        available_cto_metrics = metric_registry.get_available_metrics('cto')
        
        for tab, (tab_name, metrics_list) in zip(tabs, tab_config):
            with tab:
                if tab_name == "📋 All Metrics":
                    dashboard_loader.display_metric_summary('cto')
                    st.markdown("---")
                    
                    for metric in available_cto_metrics:
                        with st.expander(f"📊 {metric.replace('_', ' ').title()}"):
                            dashboard_loader.display_generic_metric('cto', metric, st.container())
                else:
                    for metric in metrics_list:
                        if metric in available_cto_metrics:
                            dashboard_loader.display_generic_metric('cto', metric, st.container())
                            st.markdown("---")

    # Add this after your existing CTO tabs
    if HBCU_INTEGRATION_AVAILABLE and hbcu_integrator:
        st.markdown("---")
        hbcu_integrator.render_hbcu_dashboard_section('cto')

elif persona == "Project Manager View":
    st.markdown("### Project Management Dashboard")
    

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Projects", "8", "", help="Currently in progress")
    with col2:
        st.metric("On Schedule", "87%", "+5%", help="Projects on track")
    with col3:
        st.metric("Resource Utilization", "92%", "+3%", help="Team capacity")
    with col4:
        st.metric("Portfolio Health", "8.1/10", "+0.3", help="Overall health score")
    
    # Dynamic tabs for PM
    if METRICS_AVAILABLE:
        # First fix the persona_key mapping
        pm_persona = 'pm'  # Map to PM
        
        tab_config = [
            ("📊 Project Portfolio", ["project_charter_metrics", "project_portfolio_dashboard_metrics"]),
            ("📈 Performance & Budget", ["project_timeline_budget_performance"]),
            ("📋 Requirements & RAID", ["requirements_traceability_matrix", "raid_log_metrics"]),
            ("👥 Resources & Communication", ["resource_allocation_metrics", "stakeholder_communication_metrics"]),
            ("📋 All Metrics", [])
        ]
        
        tab_names = [config[0] for config in tab_config]
        tabs = st.tabs(tab_names)
        
        # Get available PM metrics
        available_pm_metrics = list(PM_METRICS.keys()) if PM_METRICS_AVAILABLE else []
        
        for tab, (tab_name, metrics_list) in zip(tabs, tab_config):
            with tab:
                if tab_name == "📋 All Metrics":
                    if PM_METRICS_AVAILABLE:
                        st.subheader("All Available PM Metrics")
                        for metric in available_pm_metrics:
                            with st.expander(f"📊 {metric.replace('_', ' ').title()}"):
                                dashboard_loader.display_generic_metric('pm', metric, st.container())
                    else:
                        st.warning("PM metrics not available")
                else:
                    for metric in metrics_list:
                        if PM_METRICS_AVAILABLE and metric in available_pm_metrics:
                            dashboard_loader.display_generic_metric('pm', metric, st.container())
                            st.markdown("---")
                        else:
                            st.info(f"Metric {metric} not available")
    else:
        st.warning("Metric system not available. Please check PM module integration.")

elif persona == "HBCU Institutional View":
    if HBCU_INTEGRATION_AVAILABLE and hbcu_integrator:
        hbcu_integrator.render_institutional_hbcu_view()
        
        # Additional institutional analysis
        st.markdown("---")
        st.markdown("## Institutional Benchmarking")
        
        # Benchmark comparison tabs
        tab1, tab2, tab3 = st.tabs(["Mission Alignment", "Financial Efficiency", "Student Outcomes"])
        
        with tab1:
            st.markdown("### Mission-Critical Investment Analysis")
            st.info("Mission alignment analysis would go here")
        
        with tab2:
            st.markdown("### Financial Efficiency vs Peer HBCUs")
            st.info("Financial efficiency analysis would go here")
        
        with tab3:
            st.markdown("### Technology Impact on Student Success")
            st.info("Student outcomes analysis would go here")
    else:
        st.error("HBCU integration module not available")
    

# Footer with metrics summary
st.markdown("---")

# Display overall metrics availability
if METRICS_AVAILABLE:
    with st.expander("📊 System Metrics Overview"):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            cfo_count = len(metric_registry.get_available_metrics('cfo'))
            st.metric("CFO Metrics", cfo_count)
        
        with col2:
            cio_count = len(metric_registry.get_available_metrics('cio'))
            st.metric("CIO Metrics", cio_count)
        
        with col3:
            cto_count = len(metric_registry.get_available_metrics('cto'))
            st.metric("CTO Metrics", cto_count)
        
        with col4:
            total_count = cfo_count + cio_count + cto_count
            st.metric("Total Metrics", total_count)

st.markdown(
    """
    <div style='text-align: center; color: #666; margin-top: 2rem;'>
        <p>Paul Quinn College IT Analytics Suite - Fully Integrated Edition | Built with Streamlit | © 2024</p>
        <p style='font-size: 0.8rem;'>Dynamically loading metrics from src/metrics folder</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Debug information (can be removed in production)
if st.checkbox("🔧 Show Debug Info", value=False):
    st.markdown("### Debug Information")
    
    if METRICS_AVAILABLE:
        st.write("Metric Registry Status: ✅ Active")
        
        # Show loaded metrics
        for persona in ['cfo', 'cio', 'cto']:
            with st.expander(f"{persona.upper()} Metrics"):
                metrics = metric_registry.get_available_metrics(persona)
                for metric in metrics:
                    info = metric_registry.get_metric_info(persona, metric)
                    st.write(f"- {metric}: ", 
                           "📄" if info['data_path'] else "❌",
                           "🔧" if info['module_path'] else "❌",
                           "📜" if info['script_path'] else "❌")
    else:
        st.write("Metric Registry Status: ❌ Not Available")
        st.write("Check that metric_registry.py and dashboard_metric_loader.py are in the same directory")
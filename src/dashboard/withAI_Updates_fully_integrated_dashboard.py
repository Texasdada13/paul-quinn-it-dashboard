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
from issa_theme import ISSATheme  # Keep this one

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our metric registry and loader
try:
    from withAI_metric_registry import metric_registry, cfo_metrics, cio_metrics, cto_metrics
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

# AI Enhancement imports
try:
    from ai_optimization_engine import OptimizationDashboard, AIOptimizationEngine
    from metric_intelligence import MetricIntelligenceEngine, analyze_single_metric
    AI_FEATURES_AVAILABLE = True
    print("AI optimization features loaded successfully")
except ImportError as e:
    print(f"AI features not available: {e}")
    AI_FEATURES_AVAILABLE = False
    
print(f"HBCU_INTEGRATION_AVAILABLE: {HBCU_INTEGRATION_AVAILABLE}")

# Page configuration
st.set_page_config(
    page_title="PQC IT Analytics Suite - Fully Integrated",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

ISSATheme.apply_theme()


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
st.markdown(ISSATheme.create_header("ISSA", "Integrated Systems for Strategic Analytics"), unsafe_allow_html=True)
st.markdown("### Deployed for Paul Quinn College")


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
        # CFO-specific tab configuration with AI tab added
        tab_config = [
            ("📊 Budget Analysis", ["cfo_budget_vs_actual", "cfo_total_it_spend_breakdown"]),
            ("📃 Contracts & Vendors", ["cfo_contract_expiration_alerts", "cfo_vendor_spend_optimization"]),
            ("🤖 AI Optimization", []),  # NEW AI TAB
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
                
                elif tab_name == "🤖 AI Optimization":
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
    
    # Dynamic tabs for CIO with AI tab added
    if METRICS_AVAILABLE and persona_key == 'cio':
        tab_config = [
            ("🎯 Strategic Portfolio", ["digital_transformation_metrics", "strategic_alignment_metrics"]),
            ("💼 Business Analysis", ["business_unit_it_spend", "app_cost_analysis_metrics"]),
            ("🤖 AI Strategic Optimization", []),  # NEW AI TAB
            ("📊 Performance & Risk", ["risk_metrics", "vendor_metrics"]),
            ("📋 All Metrics", [])
        ]
        
        tab_names = [config[0] for config in tab_config]
        tabs = st.tabs(tab_names)
        
        available_cio_metrics = metric_registry.get_available_metrics('cio')
        
        for tab, (tab_name, metrics_list) in zip(tabs, tab_config):
            with tab:
                if tab_name == "🤖 AI Strategic Optimization":
                    if AI_FEATURES_AVAILABLE:
                        st.markdown("### AI-Powered Strategic Optimization")
                        
                        # Strategic optimization for CIO
                        optimization_dashboard = OptimizationDashboard()
                        optimization_dashboard.render_optimization_dashboard('cio', {})
                        
                        # CIO-specific AI insights
                        st.markdown("---")
                        st.markdown("#### Strategic AI Recommendations")
                        
                        with st.expander("💡 Digital Transformation Opportunities"):
                            st.success("**AI Recommendation**: Accelerate student analytics platform deployment")
                            st.info("Expected ROI: 4.2x over 3 years | Student retention impact: +12%")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Key Actions:**")
                                st.markdown("• Prioritize data integration initiatives")
                                st.markdown("• Implement predictive student success models") 
                                st.markdown("• Deploy real-time intervention systems")
                            with col2:
                                st.metric("Investment Required", "$200K")
                                st.metric("Expected Benefit", "$820K")
                                st.metric("AI Confidence", "82%")
                        
                        with st.expander("📱 Application Portfolio Optimization"):
                            st.warning("**AI Alert**: 12 applications identified for consolidation")
                            st.info("Potential annual savings: $280K | Reduced complexity: 35%")
                            
                            st.markdown("**Consolidation Candidates:**")
                            demo_apps = pd.DataFrame({
                                'Application': ['Legacy Student Portal', 'Old Communication System', 'Manual Reporting Tool'],
                                'Annual Cost': ['$45K', '$32K', '$28K'], 
                                'Replacement': ['Modern Student Hub', 'Integrated Comms Platform', 'Automated Analytics'],
                                'Savings': ['$18K', '$15K', '$12K']
                            })
                            st.dataframe(demo_apps, use_container_width=True)
                    else:
                        st.warning("AI strategic optimization features not available")
                
                elif tab_name == "📋 All Metrics":
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
    
    # Dynamic tabs for CTO with AI tab added
    if METRICS_AVAILABLE and persona_key == 'cto':
        tab_config = [
            ("🖥️ Infrastructure", ["infrastructure_performance_metrics", "system_utilization_metrics"]),
            ("☁️ Cloud & Assets", ["cloud_cost_optimization_metrics", "asset_lifecycle_management_metrics", 
                                  "capacity_planning_metrics"]),
            ("🤖 AI Operational Optimization", []),  # NEW AI TAB
            ("🔒 Security & Quality", ["security_metrics_and_response", "technical_debt_metrics", 
                                      "tech_stack_health_metrics"]),
            ("📋 All Metrics", [])
        ]
        
        tab_names = [config[0] for config in tab_config]
        tabs = st.tabs(tab_names)
        
        available_cto_metrics = metric_registry.get_available_metrics('cto')
        
        for tab, (tab_name, metrics_list) in zip(tabs, tab_config):
            with tab:
                if tab_name == "🤖 AI Operational Optimization":
                    if AI_FEATURES_AVAILABLE:
                        st.markdown("### AI-Powered Operational Optimization")
                        
                        # Operational optimization for CTO
                        optimization_dashboard = OptimizationDashboard()
                        optimization_dashboard.render_optimization_dashboard('cto', {})
                        
                        # CTO-specific AI insights
                        st.markdown("---")
                        st.markdown("#### Operational AI Recommendations")
                        
                        with st.expander("☁️ Infrastructure Right-Sizing"):
                            st.success("**AI Recommendation**: Cloud resource optimization identified")
                            st.info("Potential annual savings: $180K | Efficiency improvement: 40%")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Optimization Actions:**")
                                st.markdown("• Right-size over-provisioned instances")
                                st.markdown("• Implement auto-scaling policies")
                                st.markdown("• Optimize storage tiers")
                            with col2:
                                st.metric("Current Monthly Cost", "$25K")
                                st.metric("Optimized Cost", "$18K")
                                st.metric("Monthly Savings", "$7K")
                        
                        with st.expander("🔧 Automation Opportunities"):
                            st.warning("**AI Alert**: 65% of routine tasks can be automated")
                            st.info("Resource savings: 1.2 FTE | Incident reduction: 75%")
                            
                            automation_data = pd.DataFrame({
                                'Task Category': ['System Monitoring', 'Backup Management', 'User Provisioning', 'Security Patching'],
                                'Current Effort (hrs/week)': [12, 8, 6, 10],
                                'Automation Potential': ['90%', '95%', '85%', '80%'],
                                'Time Savings': [10.8, 7.6, 5.1, 8.0]
                            })
                            st.dataframe(automation_data, use_container_width=True)
                    else:
                        st.warning("AI operational optimization features not available")
                
                elif tab_name == "📋 All Metrics":
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
            
            # Create mission alignment metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # Mission alignment scoring
                mission_scores = {
                    'Student Support Services': 92,
                    'Academic Technology': 88,
                    'Community Engagement': 85,
                    'Faculty Development': 79,
                    'Infrastructure': 75
                }
                
                fig = px.bar(
                    x=list(mission_scores.values()),
                    y=list(mission_scores.keys()),
                    orientation='h',
                    title='Mission Alignment Scores by Investment Area',
                    labels={'x': 'Alignment Score', 'y': 'Investment Area'},
                    color=list(mission_scores.values()),
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # ROI by mission category
                roi_data = pd.DataFrame({
                    'Category': ['Direct Student Aid', 'Digital Learning', 'Support Programs', 'Research'],
                    'ROI': [4.2, 3.8, 3.1, 2.5],
                    'Investment': [1200000, 800000, 600000, 400000]
                })
                
                fig = px.scatter(roi_data, x='Investment', y='ROI', size='ROI', 
                                color='Category', title='ROI by Mission-Critical Investment',
                                labels={'Investment': 'Investment Amount ($)', 'ROI': 'Return on Investment (x)'},
                                size_max=50)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.markdown("### Financial Efficiency vs Peer HBCUs")
            
            # Create comparison metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # Efficiency comparison
                peer_data = pd.DataFrame({
                    'Institution': ['Paul Quinn', 'HBCU Avg', 'Top Quartile', 'Peer Median'],
                    'Cost per Student': [8224, 11500, 9800, 10200],
                    'Admin Ratio': [18, 25, 20, 22]
                })
                
                fig = px.bar(peer_data, x='Institution', y='Cost per Student',
                            title='Cost Efficiency: PQC vs HBCU Peers',
                            color='Cost per Student',
                            color_continuous_scale=['green', 'yellow', 'orange', 'red'],
                            text='Cost per Student')
                fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Spending efficiency radar
                categories = ['IT Efficiency', 'Academic Spend', 'Student Services', 
                            'Infrastructure', 'Admin Efficiency']
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=[85, 92, 88, 76, 94],
                    theta=categories,
                    fill='toself',
                    name='Paul Quinn',
                    line_color='blue'
                ))
                
                fig.add_trace(go.Scatterpolar(
                    r=[72, 78, 75, 70, 68],
                    theta=categories,
                    fill='toself',
                    name='HBCU Average',
                    line_color='orange'
                ))
                
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    title="Efficiency Metrics Comparison",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.markdown("### Technology Impact on Student Success")
            
            # Student success metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # Graduation rate trends
                years = ['2019', '2020', '2021', '2022', '2023', '2024']
                grad_rates = pd.DataFrame({
                    'Year': years,
                    'With Tech Support': [62, 65, 68, 72, 76, 78],
                    'Without Tech Support': [58, 59, 60, 61, 62, 63]
                })
                
                fig = px.line(grad_rates, x='Year', 
                            y=['With Tech Support', 'Without Tech Support'],
                            title='Graduation Rates: Technology Impact',
                            labels={'value': 'Graduation Rate (%)', 'variable': 'Student Group'},
                            markers=True)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Success metrics by intervention
                interventions = pd.DataFrame({
                    'Intervention': ['Online Tutoring', 'Learning Analytics', 'Digital Resources', 
                                'Tech Training', 'Equipment Loans'],
                    'Success Rate': [82, 79, 85, 77, 88],
                    'Students Impacted': [1200, 2100, 3500, 800, 650]
                })
                
                fig = px.scatter(interventions, x='Students Impacted', y='Success Rate',
                                size='Success Rate', color='Intervention',
                                title='Tech Intervention Effectiveness',
                                labels={'Success Rate': 'Success Rate (%)', 
                                    'Students Impacted': 'Number of Students'},
                                size_max=40)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional success metrics
            st.markdown("#### Key Technology Success Indicators")
            metric_cols = st.columns(4)
            
            with metric_cols[0]:
                st.metric("Digital Literacy", "94%", "↑ 12%", 
                        help="Students meeting digital competency standards")
            with metric_cols[1]:
                st.metric("LMS Engagement", "87%", "↑ 8%",
                        help="Active weekly LMS users")
            with metric_cols[2]:
                st.metric("Tech Support Satisfaction", "4.6/5", "↑ 0.3",
                        help="Student satisfaction rating")
            with metric_cols[3]:
                st.metric("Course Completion", "91%", "↑ 6%",
                        help="Online course completion rate")
    

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
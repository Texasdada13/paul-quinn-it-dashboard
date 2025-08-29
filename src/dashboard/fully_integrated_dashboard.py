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

ISSATheme.apply_theme()


# ============================================================================
# ENHANCED CSS STYLING - Add near top of file after imports
# ============================================================================

st.markdown("""
    <style>
    /* Global Improvements */
    .main-header {
        font-size: 2.5rem;
        color: #1e3d59;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1e3d59 0%, #288FFA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Enhanced Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 1px solid #e9ecef;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    div[data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #288FFA, #4FC3F7);
    }
    
    /* Enhanced Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #223A5E 0%, #1a2f4a 100%);
    }
    
    section[data-testid="stSidebar"] .stMetric {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 0.5rem;
        margin: 0.25rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: #f8f9fa;
        padding: 4px;
        border-radius: 12px;
        border: none;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #666;
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #288FFA 0%, #4FC3F7 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(40, 143, 250, 0.3);
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #288FFA 0%, #4FC3F7 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(40, 143, 250, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(40, 143, 250, 0.4);
    }
    
    /* Status Indicators */
    .status-good { color: #28a745; font-weight: bold; }
    .status-warning { color: #ffc107; font-weight: bold; }
    .status-danger { color: #dc3545; font-weight: bold; }
    .status-info { color: #17a2b8; font-weight: bold; }
    
    /* Enhanced Info Boxes */
    .info-box {
        background: linear-gradient(135deg, #e8f4f8 0%, #f8f9fa 100%);
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #f8f9fa 100%);
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #f8f9fa 100%);
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .danger-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f8f9fa 100%);
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Optimization Highlight */
    .optimization-highlight {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-weight: 600;
    }
    
    .integrated-badge {
        background-color: #17a2b8;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.8rem;
        margin-left: 0.5rem;
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



# ============================================================================
# ENHANCED SIDEBAR NAVIGATION - Replace your sidebar section
# ============================================================================

st.sidebar.markdown("### 🎓 Paul Quinn College")
st.sidebar.markdown("**ISSA** - *Integrated Systems for Strategic Analytics*")
st.sidebar.markdown("<span class='integrated-badge'>AI-POWERED OPTIMIZATION</span>", unsafe_allow_html=True)

# Add executive summary in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Executive Summary")

# Dynamic metrics based on current persona
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

# Show key metrics for current persona
if persona.startswith("CFO"):
    st.sidebar.metric("Total IT Budget", "$2.8M", "↑ 5.2%")
    st.sidebar.metric("Potential Savings", "$340K", "Identified")
    st.sidebar.metric("Risk Contracts", "13", "Expiring <90d")
elif persona.startswith("CIO"):
    st.sidebar.metric("Digital Progress", "65%", "↑ 15%")
    st.sidebar.metric("Project Success", "87%", "↑ 5%")
    st.sidebar.metric("Innovation Score", "7.8/10", "↑ 0.6")
elif persona.startswith("CTO"):
    st.sidebar.metric("System Uptime", "99.8%", "↑ 0.2%")
    st.sidebar.metric("Cloud Efficiency", "78%", "↑ 5%")
    st.sidebar.metric("Security Score", "A-", "Excellent")

st.sidebar.markdown("---")

# Enhanced Quick Actions Section
st.sidebar.markdown("### ⚡ Quick Actions")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("📊 Generate Report", use_container_width=True):
        st.sidebar.success("Report queued!")
        
with col2:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.sidebar.success("Data refreshed!")

col3, col4 = st.sidebar.columns(2)        
with col3:
    if st.button("📧 Email Summary", use_container_width=True):
        st.sidebar.success("Summary sent!")
        
with col4:
    if st.button("⚠️ View Alerts", use_container_width=True):
        st.sidebar.info("3 items need attention")

# AI Insights Section - NEW
st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 AI Insights")

if persona.startswith("CFO"):
    st.sidebar.markdown("💡 **Top Opportunity**")
    st.sidebar.markdown("Consolidate Microsoft licenses")
    st.sidebar.markdown("*Potential: $45K annual savings*")
    
    st.sidebar.markdown("⚠️ **Action Required**")
    st.sidebar.markdown("3 contracts expire in 30 days")
    st.sidebar.markdown("*Risk: $240K in spend*")
    
elif persona.startswith("CIO"):
    st.sidebar.markdown("💡 **Strategic Priority**")
    st.sidebar.markdown("Student analytics platform")
    st.sidebar.markdown("*ROI: 4.2x over 3 years*")
    
    st.sidebar.markdown("📈 **Portfolio Health**")
    st.sidebar.markdown("87% projects on track")
    st.sidebar.markdown("*Above industry average*")

# System Status
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 System Status")

# Show metrics availability
if METRICS_AVAILABLE:
    available_count = sum(len(metric_registry.get_available_metrics(p)) for p in ['cfo', 'cio', 'cto'])
    st.sidebar.markdown(f"<span class='status-good'>✅ **{available_count} Metrics Active**</span>", 
                       unsafe_allow_html=True)
    
    # Show data freshness
    st.sidebar.markdown("📅 **Data Updated:** 2 hours ago")
    st.sidebar.markdown("🔄 **Next Refresh:** 10:00 PM")
else:
    st.sidebar.markdown("<span class='status-danger'>❌ **Metrics Offline**</span>", 
                       unsafe_allow_html=True)

# HBCU Quick Stats (if available)
if HBCU_INTEGRATION_AVAILABLE and hbcu_integrator:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏛️ HBCU Context")
    
    st.sidebar.metric("Students Served", "5,800", "↑ 3.2%")
    st.sidebar.metric("Cost per Student", "$8,224", "40% below avg") 
    st.sidebar.metric("Mission Alignment", "94%", "Excellent")

# ============================================================================
# MAIN HEADER - Enhanced
# ============================================================================

st.markdown(ISSATheme.create_header("ISSA", "Integrated Systems for Strategic Analytics"), unsafe_allow_html=True)
st.markdown("### Deployed for Paul Quinn College")


# ============================================================================
# ENHANCED CFO DASHBOARD SECTION - Complete Implementation
# ============================================================================

if persona == "CFO - Financial Steward":
    st.markdown("### 💰 CFO Dashboard - Financial Overview & Strategic Optimization")
    
    # Enhanced Executive Summary Row
    st.markdown("#### 📊 Executive Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
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
            at_risk_contracts = 13
    else:
        total_budget = 2800000
        variance_pct = 5.2
        at_risk_contracts = 13
    
    with col1:
        st.metric(
            "💼 Total IT Budget", 
            f"${total_budget/1000000:.1f}M", 
            f"{variance_pct:+.1f}% YoY",
            help="Annual IT budget with year-over-year variance"
        )
    with col2:
        st.metric(
            "📈 YTD Spend", 
            "$1.9M", 
            "-3% vs plan",
            help="68% of annual budget consumed"
        )
    with col3:
        st.metric(
            "💡 Identified Savings", 
            "$340K", 
            "+12% opportunity",
            help="AI-identified cost optimization opportunities"
        )
    with col4:
        st.metric(
            "⚠️ Contract Risk", 
            str(at_risk_contracts), 
            "Expiring <90d",
            delta_color="inverse",
            help="Contracts requiring immediate attention"
        )
    with col5:
        st.metric(
            "🎯 ROI Score", 
            "87%", 
            "+5% improved",
            help="Technology investment return score"
        )
    
    # AI Insights Alert Bar
    st.markdown("---")
    st.markdown(
        """
        <div class="optimization-highlight">
            🤖 <strong>AI Recommendation:</strong> Consolidate 3 Microsoft contracts for $45K annual savings. 
            Negotiate Adobe renewal early for 15% discount. Review cloud spend for $28K monthly optimization.
            <span style="float: right;">
                <button style="background: rgba(255,255,255,0.2); border: 1px solid white; color: white; padding: 4px 8px; border-radius: 4px; cursor: pointer;">View Details →</button>
            </span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Enhanced Tab Configuration
    if METRICS_AVAILABLE and persona_key in ['cfo']:
        tab_config = [
            ("📊 Budget Analysis", ["cfo_budget_vs_actual", "cfo_total_it_spend_breakdown"]),
            ("📃 Contract Intelligence", ["cfo_contract_expiration_alerts", "cfo_vendor_spend_optimization"]),
            ("🤖 AI Optimization", []),  # NEW AI TAB
            ("🏛️ Grant & Compliance", ["cfo_grant_compliance"]),
            ("📈 ROI & Benchmarking", ["cfo_student_success_roi", "cfo_hbcu_peer_benchmarking"]),
            ("📋 Executive Summary", [])
        ]
        
        tab_names = [config[0] for config in tab_config]
        tabs = st.tabs(tab_names)
        
        available_metrics = metric_registry.get_available_metrics('cfo')
        
        for idx, (tab, (tab_name, metrics_list)) in enumerate(zip(tabs, tab_config)):
            with tab:
                if tab_name == "📊 Budget Analysis":
                    # Enhanced Budget Analysis
                    st.markdown("### 💰 Budget Performance Analysis")
                    
                    # Quick action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button("📥 Export Budget Report"):
                            st.success("Budget report exported!")
                    with col2:
                        if st.button("📊 Variance Drill-Down"):
                            st.info("Loading detailed variance analysis...")
                    with col3:
                        if st.button("🔄 Refresh Budget Data"):
                            st.success("Budget data refreshed!")
                    with col4:
                        if st.button("📧 Email Stakeholders"):
                            st.success("Budget summary sent!")
                    
                    st.markdown("---")
                    
                    # Budget variance analysis with enhancements
                    if "cfo_budget_vs_actual" in available_metrics:
                        dashboard_loader.display_cfo_budget_variance(st.container())
                    else:
                        # Fallback enhanced visualization
                        st.info("📊 **Enhanced Budget Visualization Loading...**")
                        st.markdown("*Showing demo budget analysis with variance alerts*")
                    
                    # Total IT spend breakdown
                    if "cfo_total_it_spend_breakdown" in available_metrics:
                        st.markdown("---")
                        st.markdown("### 📊 IT Spend Breakdown & Trends")
                        dashboard_loader.display_generic_metric('cfo', 'cfo_total_it_spend_breakdown', st.container())
                
                elif tab_name == "📃 Contract Intelligence":
                    st.markdown("### 📋 Smart Contract Management")
                    
                    # Contract action dashboard
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(
                            """
                            <div class="danger-box">
                                <h4>🚨 Urgent Action Required</h4>
                                <p><strong>3 contracts</strong> expire in 30 days</p>
                                <p>Total Value: <strong>$240K</strong></p>
                                <button style="width:100%; background:#dc3545; color:white; border:none; padding:8px; border-radius:4px;">Review Now</button>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    with col2:
                        st.markdown(
                            """
                            <div class="warning-box">
                                <h4>⚠️ Renewal Opportunities</h4>
                                <p><strong>8 contracts</strong> up for renewal</p>
                                <p>Negotiation Potential: <strong>$85K</strong></p>
                                <button style="width:100%; background:#ffc107; color:black; border:none; padding:8px; border-radius:4px;">Plan Strategy</button>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    with col3:
                        st.markdown(
                            """
                            <div class="success-box">
                                <h4>✅ Optimization Ready</h4>
                                <p><strong>12 vendors</strong> consolidation potential</p>
                                <p>Estimated Savings: <strong>$120K</strong></p>
                                <button style="width:100%; background:#28a745; color:white; border:none; padding:8px; border-radius:4px;">Start Process</button>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("---")
                    
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
                    st.markdown("### 🤖 AI-Powered Financial Optimization")
                    
                    # AI Insights Dashboard
                    st.markdown("#### 💡 Intelligent Recommendations")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("##### 🎯 Top Opportunities")
                        
                        opportunities = [
                            {
                                "title": "Microsoft License Consolidation",
                                "savings": "$45,000 annually",
                                "confidence": "92%",
                                "timeline": "2-3 months",
                                "action": "Consolidate 3 separate Microsoft agreements"
                            },
                            {
                                "title": "Cloud Resource Optimization", 
                                "savings": "$28,000 annually",
                                "confidence": "87%",
                                "timeline": "1 month",
                                "action": "Rightsize AWS instances and eliminate unused storage"
                            },
                            {
                                "title": "Software License Audit",
                                "savings": "$15,000 annually", 
                                "confidence": "94%",
                                "timeline": "2 weeks",
                                "action": "Remove unused Adobe and Microsoft licenses"
                            }
                        ]
                        
                        for i, opp in enumerate(opportunities):
                            st.markdown(
                                f"""
                                <div class="info-box">
                                    <h4>💰 {opp['title']}</h4>
                                    <p><strong>Savings:</strong> {opp['savings']}</p>
                                    <p><strong>Confidence:</strong> {opp['confidence']}</p>
                                    <p><strong>Timeline:</strong> {opp['timeline']}</p>
                                    <p><em>{opp['action']}</em></p>
                                    <button style="background:#288FFA; color:white; border:none; padding:6px 12px; border-radius:4px; margin-top:8px;">Implement</button>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    
                    with col2:
                        st.markdown("##### 📊 Predictive Analytics")
                        
                        # Budget variance prediction
                        st.markdown("**Q4 Budget Variance Forecast:**")
                        st.progress(0.23, text="23% likelihood of overrun in Infrastructure")
                        
                        st.markdown("**Contract Renewal Risk Assessment:**")
                        st.progress(0.67, text="67% chance of price increase on renewals")
                        
                        st.markdown("**Optimization Impact Projection:**")
                        st.progress(0.89, text="89% confidence in $340K total savings")
                        
                        st.markdown("---")
                        
                        st.markdown("**🎯 Strategic Recommendations:**")
                        st.markdown("• **Rebalance Portfolio:** Move 15% from hardware to cloud")
                        st.markdown("• **Vendor Strategy:** Consolidate from 23 to 15 vendors")
                        st.markdown("• **Investment Timing:** Delay ERP upgrade 6 months")
                        st.markdown("• **Grant Opportunity:** Apply for $200K digital equity grant")
                    
                    # Implementation Tracking
                    st.markdown("---")
                    st.markdown("#### 📈 Optimization Tracking")
                    
                    tracking_data = pd.DataFrame({
                        'Initiative': ['License Consolidation', 'Cloud Optimization', 'Vendor Reduction', 'Contract Negotiation'],
                        'Target Savings': [45000, 28000, 35000, 67000],
                        'Actual Savings': [42000, 31000, 28000, 45000],
                        'Status': ['Completed', 'In Progress', 'Planning', 'Completed']
                    })
                    
                    st.dataframe(
                        tracking_data.style.format({
                            'Target Savings': '${:,.0f}',
                            'Actual Savings': '${:,.0f}'
                        }),
                        use_container_width=True
                    )
                
                elif tab_name == "🏛️ Grant & Compliance":
                    st.markdown("### 🏛️ Grant Management & Compliance Dashboard")
                    
                    if "cfo_grant_compliance" in available_metrics:
                        dashboard_loader.display_cfo_grant_compliance(st.container())
                    else:
                        st.info("Grant compliance metrics not available")
                
                elif tab_name == "📈 ROI & Benchmarking":
                    st.markdown("### 📈 Return on Investment & Peer Benchmarking")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if "cfo_student_success_roi" in available_metrics:
                            dashboard_loader.display_generic_metric('cfo', 'cfo_student_success_roi', st.container())
                        else:
                            st.markdown("#### 🎓 Student Success ROI")
                            st.metric("Technology Impact on Retention", "12%", "↑ 3%")
                            st.metric("Cost per Graduate (Tech)", "$2,840", "↓ $320")
                            st.metric("Digital Engagement Score", "87%", "↑ 15%")
                            
                    with col2:
                        if "cfo_hbcu_peer_benchmarking" in available_metrics:
                            dashboard_loader.display_generic_metric('cfo', 'cfo_hbcu_peer_benchmarking', st.container())
                        else:
                            st.markdown("#### 🏫 HBCU Peer Comparison")
                            st.metric("IT Spend per Student", "$8,224", "15% below peer avg")
                            st.metric("Technology Efficiency Rank", "2nd", "of 12 peer HBCUs")
                            st.metric("Innovation Index", "8.1/10", "↑ 0.6")
                
                elif tab_name == "📋 Executive Summary":
                    st.markdown("### 📋 Executive Summary & Action Items")
                    
                    # Executive KPI Dashboard
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### 💰 Financial Performance")
                        st.metric("Budget Utilization", "68%", "On track")
                        st.metric("Cost Optimization", "$340K", "Identified")
                        st.metric("Contract Risk", "Medium", "13 expiring")
                        
                    with col2:
                        st.markdown("#### 🎯 Strategic Alignment") 
                        st.metric("Mission Support Score", "94%", "Excellent")
                        st.metric("Student Success Impact", "87%", "↑ 12%")
                        st.metric("Innovation Investment", "23%", "↑ 5%")
                        
                    with col3:
                        st.markdown("#### 📊 Operational Excellence")
                        st.metric("Vendor Performance", "8.2/10", "Good")
                        st.metric("Compliance Rate", "96%", "↑ 2%")
                        st.metric("Process Efficiency", "91%", "↑ 8%")
                    
                    st.markdown("---")
                    
                    # Action Items
                    st.markdown("#### ⚡ Priority Action Items")
                    
                    action_items = [
                        {"priority": "🔴 High", "item": "Review 3 contracts expiring in 30 days", "owner": "Procurement", "due": "This week"},
                        {"priority": "🟡 Medium", "item": "Negotiate Microsoft license consolidation", "owner": "IT/Finance", "due": "Next month"},
                        {"priority": "🟢 Low", "item": "Audit unused software licenses", "owner": "IT", "due": "Q4"},
                        {"priority": "🔴 High", "item": "Prepare grant compliance report", "owner": "Finance", "due": "2 weeks"}
                    ]
                    
                    for item in action_items:
                        st.markdown(
                            f"""
                            <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 4px solid {'#dc3545' if 'High' in item['priority'] else '#ffc107' if 'Medium' in item['priority'] else '#28a745'};">
                                <strong>{item['priority']}</strong> - {item['item']}<br>
                                <small><strong>Owner:</strong> {item['owner']} | <strong>Due:</strong> {item['due']}</small>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
    
    # Add HBCU Integration if available
    if HBCU_INTEGRATION_AVAILABLE and hbcu_integrator:
        st.markdown("---")
        hbcu_integrator.render_hbcu_dashboard_section('cfo')
                
elif persona == "CIO - Strategic Partner":
    st.markdown("### 🎯 CIO Dashboard - Strategic IT Portfolio Management")
    
    # Enhanced Executive Summary Row
    st.markdown("#### 📊 Strategic Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "🎯 Digital Transformation", 
            "65%", 
            "+15% progress",
            help="Overall digital transformation completion"
        )
    with col2:
        st.metric(
            "📈 Project Success Rate", 
            "87%", 
            "+5% improved",
            help="Projects completed on time and budget"
        )
    with col3:
        st.metric(
            "💡 Innovation Index", 
            "7.8/10", 
            "+0.6 growth",
            help="Technology innovation maturity score"
        )
    with col4:
        st.metric(
            "🔄 Business Alignment", 
            "92%", 
            "+3% improved",
            help="IT-Business strategic alignment score"
        )
    with col5:
        st.metric(
            "📊 Portfolio Health", 
            "A-", 
            "Excellent",
            help="Overall IT portfolio performance rating"
        )
    
    # AI Strategic Insights Alert Bar
    st.markdown("---")
    st.markdown(
        """
        <div class="optimization-highlight">
            🤖 <strong>Strategic AI Recommendation:</strong> Prioritize student analytics platform for 4.2x ROI. 
            Consolidate app portfolio (12 redundant systems identified). Accelerate cloud migration for $180K savings.
            <span style="float: right;">
                <button style="background: rgba(255,255,255,0.2); border: 1px solid white; color: white; padding: 4px 8px; border-radius: 4px; cursor: pointer;">View Strategy →</button>
            </span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Enhanced Tab Configuration for CIO
    if METRICS_AVAILABLE:
        tab_config = [
            ("🎯 Strategic Portfolio", ["digital_transformation_metrics", "strategic_alignment_metrics"]),
            ("💼 Business Analysis", ["business_unit_it_spend", "app_cost_analysis_metrics"]),
            ("🤖 AI Strategy", []),  # NEW AI STRATEGY TAB
            ("⚠️ Risk & Vendor Management", ["risk_metrics", "vendor_metrics"]),
            ("📈 Performance Dashboard", ["project_performance", "innovation_metrics"]),
            ("📋 Executive Brief", [])
        ]
        
        tab_names = [config[0] for config in tab_config]
        tabs = st.tabs(tab_names)
        
        available_cio_metrics = metric_registry.get_available_metrics('cio') if hasattr(metric_registry, 'get_available_metrics') else []
        
        for idx, (tab, (tab_name, metrics_list)) in enumerate(zip(tabs, tab_config)):
            with tab:
                if tab_name == "🎯 Strategic Portfolio":
                    st.markdown("### 🎯 Digital Transformation & Strategic Alignment")
                    
                    # Strategic action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button("📊 Portfolio Review", key="cio_portfolio"):
                            st.success("Portfolio analysis initiated!")
                    with col2:
                        if st.button("🎯 Strategy Update", key="cio_strategy"):
                            st.info("Strategic roadmap updating...")
                    with col3:
                        if st.button("📈 Progress Report", key="cio_progress"):
                            st.success("Progress report generated!")
                    with col4:
                        if st.button("📧 Stakeholder Brief", key="cio_brief"):
                            st.success("Executive brief sent!")
                    
                    st.markdown("---")
                    
                    # Digital transformation progress
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 🚀 Digital Transformation Progress")
                        
                        # Transformation areas with progress
                        transformation_areas = [
                            ("Student Experience Platform", 85, "success"),
                            ("Faculty Digital Tools", 72, "success"),
                            ("Administrative Systems", 45, "warning"),
                            ("Data Analytics Infrastructure", 60, "info"),
                            ("Cloud Migration", 38, "warning")
                        ]
                        
                        for area, progress, status in transformation_areas:
                            st.markdown(f"**{area}**")
                            st.progress(progress/100, text=f"{progress}% Complete")
                            st.markdown("")
                    
                    with col2:
                        st.markdown("#### 📊 Strategic Alignment Metrics")
                        
                        alignment_metrics = [
                            ("Mission Alignment Score", "94%", "↑ 3%"),
                            ("Student Success Impact", "87%", "↑ 12%"),
                            ("Faculty Satisfaction", "82%", "↑ 8%"),
                            ("Process Efficiency", "78%", "↑ 15%"),
                            ("Innovation Investment", "23%", "↑ 5%")
                        ]
                        
                        for metric, value, delta in alignment_metrics:
                            st.metric(metric, value, delta)
                    
                    # Load actual metrics if available
                    if "digital_transformation_metrics" in available_cio_metrics:
                        st.markdown("---")
                        dashboard_loader.display_generic_metric('cio', 'digital_transformation_metrics', st.container())
                
                elif tab_name == "💼 Business Analysis":
                    st.markdown("### 💼 Business Unit IT Investment Analysis")
                    
                    # Business unit spending overview
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(
                            """
                            <div class="info-box">
                                <h4>📚 Academic Affairs</h4>
                                <p><strong>Annual Spend:</strong> $1.2M</p>
                                <p><strong>Key Systems:</strong> LMS, SIS</p>
                                <p><strong>ROI Score:</strong> 4.2x</p>
                                <button style="width:100%; background:#17a2b8; color:white; border:none; padding:8px; border-radius:4px;">Analyze Spend</button>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    
                    with col2:
                        st.markdown(
                            """
                            <div class="success-box">
                                <h4>👥 Student Services</h4>
                                <p><strong>Annual Spend:</strong> $850K</p>
                                <p><strong>Key Systems:</strong> CRM, Portal</p>
                                <p><strong>ROI Score:</strong> 3.8x</p>
                                <button style="width:100%; background:#28a745; color:white; border:none; padding:8px; border-radius:4px;">Optimize Portfolio</button>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    
                    with col3:
                        st.markdown(
                            """
                            <div class="warning-box">
                                <h4>💰 Finance & Admin</h4>
                                <p><strong>Annual Spend:</strong> $650K</p>
                                <p><strong>Key Systems:</strong> ERP, HR</p>
                                <p><strong>ROI Score:</strong> 2.1x</p>
                                <button style="width:100%; background:#ffc107; color:black; border:none; padding:8px; border-radius:4px;">Review Efficiency</button>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("---")
                    
                    # Application portfolio analysis
                    st.markdown("#### 📱 Application Portfolio Health")
                    
                    # Load actual metrics if available
                    if "business_unit_it_spend" in available_cio_metrics:
                        dashboard_loader.display_generic_metric('cio', 'business_unit_it_spend', st.container())
                    else:
                        st.info("Business unit spend analysis loading...")
                    
                    if "app_cost_analysis_metrics" in available_cio_metrics:
                        st.markdown("---")
                        dashboard_loader.display_generic_metric('cio', 'app_cost_analysis_metrics', st.container())
                
                elif tab_name == "🤖 AI Strategy":
                    st.markdown("### 🤖 AI-Powered Strategic Intelligence")
                    
                    # Strategic AI Dashboard
                    st.markdown("#### 💡 Strategic Recommendations")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("##### 🎯 Priority Initiatives")
                        
                        strategic_opportunities = [
                            {
                                "title": "Student Analytics Platform",
                                "impact": "4.2x ROI, +12% retention",
                                "investment": "$200K",
                                "timeline": "6 months",
                                "priority": "high"
                            },
                            {
                                "title": "Application Portfolio Rationalization",
                                "impact": "$280K annual savings",
                                "investment": "$150K",
                                "timeline": "9 months",
                                "priority": "high"
                            },
                            {
                                "title": "Faculty Digital Experience Hub",
                                "impact": "85% satisfaction boost",
                                "investment": "$120K",
                                "timeline": "4 months",
                                "priority": "medium"
                            }
                        ]
                        
                        for opp in strategic_opportunities:
                            priority_color = "#dc3545" if opp["priority"] == "high" else "#ffc107"
                            st.markdown(
                                f"""
                                <div class="info-box" style="border-left-color: {priority_color};">
                                    <h4>🚀 {opp['title']}</h4>
                                    <p><strong>Impact:</strong> {opp['impact']}</p>
                                    <p><strong>Investment:</strong> {opp['investment']}</p>
                                    <p><strong>Timeline:</strong> {opp['timeline']}</p>
                                    <button style="background:#288FFA; color:white; border:none; padding:6px 12px; border-radius:4px; margin-top:8px;">Initiate Project</button>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    
                    with col2:
                        st.markdown("##### 📊 Strategic Analytics")
                        
                        # Strategic forecasting
                        st.markdown("**Digital Transformation Forecast:**")
                        st.progress(0.78, text="78% completion by Q4 2025")
                        
                        st.markdown("**Innovation Pipeline Health:**")
                        st.progress(0.85, text="85% of initiatives on track")
                        
                        st.markdown("**Business Value Realization:**")
                        st.progress(0.92, text="92% confidence in projected outcomes")
                        
                        st.markdown("---")
                        
                        st.markdown("**🎯 Strategic Focus Areas:**")
                        st.markdown("• **Student Success Technology:** AI-powered retention tools")
                        st.markdown("• **Operational Excellence:** Process automation & efficiency")
                        st.markdown("• **Innovation Culture:** Faculty digital fluency programs")
                        st.markdown("• **Data-Driven Decisions:** Analytics infrastructure expansion")
                    
                    # Strategic Portfolio Tracking
                    st.markdown("---")
                    st.markdown("#### 📈 Strategic Initiative Tracking")
                    
                    portfolio_data = pd.DataFrame({
                        'Initiative': ['Student Success Platform', 'Digital Campus', 'Faculty Tools', 'Admin Modernization'],
                        'Budget': [500000, 750000, 300000, 450000],
                        'Progress': [85, 45, 72, 30],
                        'Business Value': ['High', 'High', 'Medium', 'Medium'],
                        'Risk Level': ['Low', 'Medium', 'Low', 'High']
                    })
                    
                    st.dataframe(
                        portfolio_data.style.format({
                            'Budget': '${:,.0f}',
                            'Progress': '{:.0f}%'
                        }),
                        use_container_width=True
                    )
                
                elif tab_name == "⚠️ Risk & Vendor Management":
                    st.markdown("### ⚠️ Strategic Risk & Vendor Portfolio Management")
                    
                    # Risk assessment dashboard
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 🎯 Strategic Risk Assessment")
                        
                        risk_categories = [
                            ("Technology Debt", "Medium", "warning"),
                            ("Vendor Concentration", "High", "danger"),
                            ("Cybersecurity Posture", "Low", "success"),
                            ("Skills Gap", "Medium", "warning"),
                            ("Budget Variance", "Low", "success")
                        ]
                        
                        for risk, level, status in risk_categories:
                            color_map = {"success": "#28a745", "warning": "#ffc107", "danger": "#dc3545"}
                            st.markdown(
                                f"""
                                <div style="background: #f8f9fa; padding: 8px; margin: 4px 0; border-radius: 4px; border-left: 3px solid {color_map[status]};">
                                    <strong>{risk}:</strong> <span style="color: {color_map[status]};">{level} Risk</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    
                    with col2:
                        st.markdown("#### 🏢 Vendor Performance Scorecard")
                        
                        vendor_metrics = [
                            ("Strategic Vendors", "8", "Active relationships"),
                            ("Contract Value", "$2.1M", "Annual commitment"),
                            ("Performance Score", "8.2/10", "Above target"),
                            ("Innovation Index", "7.5/10", "Good partnership"),
                            ("Risk Mitigation", "94%", "Excellent coverage")
                        ]
                        
                        for metric, value, description in vendor_metrics:
                            st.metric(metric, value, description)
                    
                    # Load actual risk metrics
                    if "risk_metrics" in available_cio_metrics:
                        st.markdown("---")
                        dashboard_loader.display_generic_metric('cio', 'risk_metrics', st.container())
                
                elif tab_name == "📈 Performance Dashboard":
                    st.markdown("### 📈 Strategic Performance & Innovation Metrics")
                    
                    # Performance overview
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### 🎯 Project Performance")
                        st.metric("On-Time Delivery", "87%", "↑ 5%")
                        st.metric("Budget Adherence", "91%", "↑ 3%")
                        st.metric("Stakeholder Satisfaction", "8.4/10", "↑ 0.6")
                        
                    with col2:
                        st.markdown("#### 💡 Innovation Metrics")
                        st.metric("New Initiatives", "12", "This quarter")
                        st.metric("Innovation Investment", "23%", "Of total budget")
                        st.metric("Success Rate", "78%", "Above industry")
                        
                    with col3:
                        st.markdown("#### 📊 Business Impact")
                        st.metric("Process Efficiency", "+15%", "Improvement")
                        st.metric("User Adoption", "89%", "Platform usage")
                        st.metric("Business Value", "$1.2M", "Realized benefits")
                
                elif tab_name == "📋 Executive Brief":
                    st.markdown("### 📋 Executive Strategic Brief")
                    
                    # Executive summary cards
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### 🎯 Strategic Progress")
                        st.metric("Transformation Status", "65%", "On track")
                        st.metric("Business Alignment", "92%", "Excellent")
                        st.metric("Innovation Pipeline", "Strong", "12 initiatives")
                        
                    with col2:
                        st.markdown("#### 💰 Investment Performance")
                        st.metric("Portfolio ROI", "3.4x", "Above target")
                        st.metric("Cost Optimization", "12%", "Efficiency gain")
                        st.metric("Budget Utilization", "91%", "Optimal")
                        
                    with col3:
                        st.markdown("#### ⚠️ Risk & Opportunities")
                        st.metric("Risk Profile", "Moderate", "Well managed")
                        st.metric("Vendor Performance", "8.2/10", "Strong")
                        st.metric("Strategic Opportunities", "3", "High impact")
                    
                    st.markdown("---")
                    
                    # Strategic action items
                    st.markdown("#### ⚡ Strategic Action Items")
                    
                    strategic_actions = [
                        {"priority": "🔴 High", "item": "Approve student analytics platform funding", "owner": "Executive Team", "due": "Next board meeting"},
                        {"priority": "🟡 Medium", "item": "Complete application portfolio assessment", "owner": "IT Leadership", "due": "End of quarter"},
                        {"priority": "🟢 Low", "item": "Update digital transformation roadmap", "owner": "Strategy Team", "due": "Next month"},
                        {"priority": "🔴 High", "item": "Address vendor concentration risk", "owner": "Procurement", "due": "2 weeks"}
                    ]
                    
                    for item in strategic_actions:
                        priority_colors = {"🔴 High": "#dc3545", "🟡 Medium": "#ffc107", "🟢 Low": "#28a745"}
                        color = priority_colors.get(item['priority'], '#17a2b8')
                        
                        st.markdown(
                            f"""
                            <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 4px solid {color};">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <strong style="color: {color};">{item['priority']}</strong> - {item['item']}
                                        <br><small><strong>Owner:</strong> {item['owner']} | <strong>Due:</strong> {item['due']}</small>
                                    </div>
                                    <button style="background: {color}; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; font-size: 12px; font-weight: 600;">Track</button>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
        
        else:
            # Fallback for no metrics
            st.markdown("### 🎯 CIO Strategic Dashboard")
            
            # Basic CIO metrics if no advanced system available
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Digital Progress", "65%", "↑ 15%")
            with col2:
                st.metric("Project Success", "87%", "↑ 5%")
            with col3:
                st.metric("Innovation Score", "7.8/10", "↑ 0.6")
            with col4:
                st.metric("Business Alignment", "92%", "↑ 3%")
            
            st.info("Enhanced CIO metrics loading... Please check metric configuration.")
    
    # Add HBCU Integration if available
    if HBCU_INTEGRATION_AVAILABLE and hbcu_integrator:
        st.markdown("---")
        hbcu_integrator.render_hbcu_dashboard_section('cio')

elif persona == "CTO - Technology Operator":
    st.markdown("### ⚙️ CTO Dashboard - Technical Operations & Infrastructure Excellence")
    
    # Enhanced Executive Summary Row
    st.markdown("#### 📊 Operational Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "🔧 System Uptime", 
            "99.8%", 
            "+0.2% improved",
            help="Infrastructure availability last 30 days"
        )
    with col2:
        st.metric(
            "⚡ Incident Resolution", 
            "2.4 hrs", 
            "-0.6 hrs faster",
            help="Average resolution time"
        )
    with col3:
        st.metric(
            "☁️ Cloud Efficiency", 
            "78%", 
            "+5% optimized",
            help="Resource utilization optimization"
        )
    with col4:
        st.metric(
            "🔒 Security Score", 
            "A-", 
            "Excellent rating",
            help="Security posture assessment"
        )
    with col5:
        st.metric(
            "💰 Cost Optimization", 
            "$180K", 
            "Annual savings",
            help="Infrastructure cost reductions achieved"
        )
    
    # AI Operations Alert Bar
    st.markdown("---")
    st.markdown(
        """
        <div class="optimization-highlight">
            🤖 <strong>Operations AI Alert:</strong> Cloud rightsizing opportunity: $28K monthly savings identified. 
            Security patch cycle optimization ready. Automated backup verification deployment recommended.
            <span style="float: right;">
                <button style="background: rgba(255,255,255,0.2); border: 1px solid white; color: white; padding: 4px 8px; border-radius: 4px; cursor: pointer;">Deploy Changes →</button>
            </span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Enhanced Tab Configuration for CTO
    if METRICS_AVAILABLE:
        tab_config = [
            ("🖥️ Infrastructure & Performance", ["infrastructure_performance_metrics", "system_utilization_metrics"]),
            ("☁️ Cloud & Asset Management", ["cloud_cost_optimization_metrics", "asset_lifecycle_management_metrics"]),
            ("🤖 AI Operations", []),  # NEW AI OPERATIONS TAB
            ("🔒 Security & Compliance", ["security_metrics_and_response", "compliance_monitoring"]),
            ("⚡ Automation & Efficiency", ["automation_metrics", "technical_debt_metrics"]),
            ("📋 Operations Summary", [])
        ]
        
        tab_names = [config[0] for config in tab_config]
        tabs = st.tabs(tab_names)
        
        available_cto_metrics = metric_registry.get_available_metrics('cto') if hasattr(metric_registry, 'get_available_metrics') else []
        
        for idx, (tab, (tab_name, metrics_list)) in enumerate(zip(tabs, tab_config)):
            with tab:
                if tab_name == "🖥️ Infrastructure & Performance":
                    st.markdown("### 🖥️ Infrastructure Health & Performance Monitoring")
                    
                    # Infrastructure action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button("📊 Health Check", key="cto_health"):
                            st.success("Infrastructure scan initiated!")
                    with col2:
                        if st.button("⚡ Performance Tune", key="cto_performance"):
                            st.info("Performance optimization starting...")
                    with col3:
                        if st.button("🔄 System Refresh", key="cto_refresh"):
                            st.success("System metrics updated!")
                    with col4:
                        if st.button("📈 Capacity Report", key="cto_capacity"):
                            st.success("Capacity analysis generated!")
                    
                    st.markdown("---")
                    
                    # Infrastructure status overview
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 🖥️ System Performance Status")
                        
                        # System performance indicators
                        performance_systems = [
                            ("Production Servers", 99.9, "success"),
                            ("Database Cluster", 99.7, "success"),
                            ("Web Applications", 98.5, "warning"),
                            ("Network Infrastructure", 99.8, "success"),
                            ("Storage Systems", 97.2, "warning")
                        ]
                        
                        for system, uptime, status in performance_systems:
                            color_map = {"success": "#28a745", "warning": "#ffc107", "danger": "#dc3545"}
                            st.markdown(f"**{system}**")
                            st.progress(uptime/100, text=f"{uptime}% Uptime")
                            st.markdown("")
                    
                    with col2:
                        st.markdown("#### 📊 Resource Utilization")
                        
                        resource_metrics = [
                            ("CPU Utilization", "68%", "↑ 5%"),
                            ("Memory Usage", "72%", "↑ 3%"),
                            ("Storage Capacity", "45%", "↑ 8%"),
                            ("Network Bandwidth", "34%", "↓ 2%"),
                            ("Backup Success Rate", "100%", "Stable")
                        ]
                        
                        for metric, value, delta in resource_metrics:
                            st.metric(metric, value, delta)
                    
                    # Load actual metrics if available
                    if "infrastructure_performance_metrics" in available_cto_metrics:
                        st.markdown("---")
                        dashboard_loader.display_generic_metric('cto', 'infrastructure_performance_metrics', st.container())
                
                elif tab_name == "☁️ Cloud & Asset Management":
                    st.markdown("### ☁️ Cloud Optimization & Asset Lifecycle Management")
                    
                    # Cloud cost overview
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(
                            """
                            <div class="success-box">
                                <h4>💰 Cost Optimization</h4>
                                <p><strong>Monthly Savings:</strong> $28K</p>
                                <p><strong>Rightsizing:</strong> 23 instances</p>
                                <p><strong>Efficiency:</strong> +18%</p>
                                <button style="width:100%; background:#28a745; color:white; border:none; padding:8px; border-radius:4px;">Apply Changes</button>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    
                    with col2:
                        st.markdown(
                            """
                            <div class="info-box">
                                <h4>📊 Resource Analytics</h4>
                                <p><strong>Utilization:</strong> 78% avg</p>
                                <p><strong>Peak Load:</strong> 94%</p>
                                <p><strong>Idle Resources:</strong> 12%</p>
                                <button style="width:100%; background:#17a2b8; color:white; border:none; padding:8px; border-radius:4px;">Analyze Usage</button>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    
                    with col3:
                        st.markdown(
                            """
                            <div class="warning-box">
                                <h4>🔄 Asset Lifecycle</h4>
                                <p><strong>End of Life:</strong> 8 servers</p>
                                <p><strong>Refresh Needed:</strong> $120K</p>
                                <p><strong>Timeline:</strong> Q2 2025</p>
                                <button style="width:100%; background:#ffc107; color:black; border:none; padding:8px; border-radius:4px;">Plan Refresh</button>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("---")
                    
                    # Asset management tracking
                    st.markdown("#### 📊 Asset Portfolio Overview")
                    
                    # Load actual cloud metrics
                    if "cloud_cost_optimization_metrics" in available_cto_metrics:
                        dashboard_loader.display_generic_metric('cto', 'cloud_cost_optimization_metrics', st.container())
                    else:
                        st.info("Cloud optimization metrics loading...")
                    
                    if "asset_lifecycle_management_metrics" in available_cto_metrics:
                        st.markdown("---")
                        dashboard_loader.display_generic_metric('cto', 'asset_lifecycle_management_metrics', st.container())
                
                elif tab_name == "🤖 AI Operations":
                    st.markdown("### 🤖 AI-Powered Operations Intelligence")
                    
                    # AI Operations Dashboard
                    st.markdown("#### 💡 Intelligent Operations Recommendations")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("##### 🎯 Optimization Opportunities")
                        
                        ops_opportunities = [
                            {
                                "title": "Cloud Resource Rightsizing",
                                "impact": "$28K monthly savings",
                                "effort": "Low",
                                "timeline": "1 week",
                                "confidence": "94%"
                            },
                            {
                                "title": "Automated Backup Verification",
                                "impact": "99.9% reliability guarantee",
                                "effort": "Medium", 
                                "timeline": "2 weeks",
                                "confidence": "91%"
                            },
                            {
                                "title": "Predictive Maintenance System",
                                "impact": "75% reduction in downtime",
                                "effort": "High",
                                "timeline": "3 months",
                                "confidence": "87%"
                            }
                        ]
                        
                        for opp in ops_opportunities:
                            effort_color = {"Low": "#28a745", "Medium": "#ffc107", "High": "#dc3545"}[opp["effort"]]
                            st.markdown(
                                f"""
                                <div class="info-box" style="border-left-color: {effort_color};">
                                    <h4>⚙️ {opp['title']}</h4>
                                    <p><strong>Impact:</strong> {opp['impact']}</p>
                                    <p><strong>Effort:</strong> {opp['effort']}</p>
                                    <p><strong>Timeline:</strong> {opp['timeline']}</p>
                                    <p><strong>Confidence:</strong> {opp['confidence']}</p>
                                    <button style="background:#288FFA; color:white; border:none; padding:6px 12px; border-radius:4px; margin-top:8px;">Deploy</button>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    
                    with col2:
                        st.markdown("##### 📊 Predictive Operations Analytics")
                        
                        # Predictive metrics
                        st.markdown("**System Failure Prediction:**")
                        st.progress(0.15, text="15% probability of hardware failure next 30 days")
                        
                        st.markdown("**Capacity Planning Forecast:**")
                        st.progress(0.82, text="82% capacity utilization projected for Q4")
                        
                        st.markdown("**Security Threat Assessment:**")
                        st.progress(0.08, text="8% elevated threat level - normal range")
                        
                        st.markdown("---")
                        
                        st.markdown("**🎯 Automated Operations Status:**")
                        st.markdown("• **Backup Automation:** 100% scheduled tasks successful")
                        st.markdown("• **Patch Management:** 94% systems up to date")
                        st.markdown("• **Monitoring Coverage:** 98% infrastructure monitored")
                        st.markdown("• **Incident Response:** 2.4 hour average resolution")
                    
                    # Operations Automation Tracking
                    st.markdown("---")
                    st.markdown("#### 📈 Automation Implementation Status")
                    
                    automation_data = pd.DataFrame({
                        'Process': ['Backup Verification', 'Patch Management', 'Monitoring Alerts', 'Capacity Scaling'],
                        'Automation Level': [95, 87, 100, 72],
                        'Time Savings': ['40 hrs/week', '25 hrs/week', '30 hrs/week', '15 hrs/week'],
                        'Status': ['Active', 'Active', 'Active', 'In Progress']
                    })
                    
                    st.dataframe(automation_data, use_container_width=True)
                
                elif tab_name == "🔒 Security & Compliance":
                    st.markdown("### 🔒 Security Posture & Compliance Monitoring")
                    
                    # Security overview
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 🛡️ Security Metrics")
                        
                        security_metrics = [
                            ("Security Score", "A-", "Excellent"),
                            ("Vulnerability Count", "3", "↓ 12 resolved"),
                            ("Patch Compliance", "94%", "↑ 3%"),
                            ("Access Control", "98%", "Strong"),
                            ("Incident Response", "2.1 hrs", "↓ 0.8 hrs")
                        ]
                        
                        for metric, value, delta in security_metrics:
                            st.metric(metric, value, delta)
                    
                    with col2:
                        st.markdown("#### 📊 Compliance Status")
                        
                        compliance_areas = [
                            ("FERPA Compliance", 98, "success"),
                            ("SOC 2 Controls", 94, "success"),
                            ("Data Protection", 92, "success"),
                            ("Access Reviews", 87, "warning"),
                            ("Security Training", 95, "success")
                        ]
                        
                        for area, score, status in compliance_areas:
                            st.markdown(f"**{area}**")
                            st.progress(score/100, text=f"{score}% Compliant")
                            st.markdown("")
                    
                    # Load security metrics if available
                    if "security_metrics_and_response" in available_cto_metrics:
                        st.markdown("---")
                        dashboard_loader.display_generic_metric('cto', 'security_metrics_and_response', st.container())
                
                elif tab_name == "⚡ Automation & Efficiency":
                    st.markdown("### ⚡ Automation Status & Technical Debt Management")
                    
                    # Efficiency overview
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### 🤖 Automation Progress")
                        st.metric("Processes Automated", "23", "↑ 7 new")
                        st.metric("Time Savings", "110 hrs/week", "↑ 25 hrs")
                        st.metric("Error Reduction", "87%", "↑ 12%")
                        
                    with col2:
                        st.markdown("#### 🔧 Technical Debt")
                        st.metric("Debt Score", "Medium", "Improving")
                        st.metric("Legacy Systems", "4", "↓ 2 retired")
                        st.metric("Code Quality", "B+", "↑ Grade")
                        
                    with col3:
                        st.markdown("#### ⚡ Efficiency Gains")
                        st.metric("Productivity", "+40%", "Team output")
                        st.metric("Response Time", "65% faster", "Issue resolution")
                        st.metric("Resource Optimization", "78%", "Utilization")
                    
                    # Technical debt breakdown
                    st.markdown("---")
                    st.markdown("#### 📊 Technical Debt Analysis")
                    
                    debt_data = pd.DataFrame({
                        'System': ['Student Portal', 'Legacy Database', 'Backup Scripts', 'Monitoring Tools'],
                        'Debt Level': ['Low', 'High', 'Medium', 'Low'],
                        'Modernization Cost': [25000, 150000, 45000, 15000],
                        'Business Impact': ['Low', 'High', 'Medium', 'Low'],
                        'Priority': ['Medium', 'High', 'Medium', 'Low']
                    })
                    
                    st.dataframe(
                        debt_data.style.format({
                            'Modernization Cost': '${:,.0f}'
                        }),
                        use_container_width=True
                    )
                
                elif tab_name == "📋 Operations Summary":
                    st.markdown("### 📋 Operations Executive Summary")
                    
                    # Operations summary cards
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### 🖥️ Infrastructure Health")
                        st.metric("Overall Uptime", "99.8%", "Excellent")
                        st.metric("Performance Score", "A-", "Above target")
                        st.metric("Capacity Utilization", "78%", "Optimal")
                        
                    with col2:
                        st.markdown("#### 💰 Cost Management")
                        st.metric("Budget Adherence", "96%", "On track")
                        st.metric("Optimization Savings", "$180K", "Annual")
                        st.metric("Cloud Efficiency", "78%", "Improving")
                        
                    with col3:
                        st.markdown("#### 🔒 Security & Risk")
                        st.metric("Security Posture", "A-", "Strong")
                        st.metric("Compliance Rate", "94%", "Excellent")
                        st.metric("Incident Count", "2", "Low impact")
                    
                    st.markdown("---")
                    
                    # Operations action items
                    st.markdown("#### ⚡ Critical Operations Items")
                    
                    operations_actions = [
                        {"priority": "🔴 High", "item": "Complete server refresh planning", "owner": "Infrastructure Team", "due": "End of week"},
                        {"priority": "🟡 Medium", "item": "Deploy cloud rightsizing recommendations", "owner": "Cloud Team", "due": "Next month"},
                        {"priority": "🟢 Low", "item": "Update disaster recovery documentation", "owner": "Operations", "due": "Next quarter"},
                        {"priority": "🔴 High", "item": "Resolve security vulnerability findings", "owner": "Security Team", "due": "48 hours"}
                    ]
                    
                    for item in operations_actions:
                        priority_colors = {"🔴 High": "#dc3545", "🟡 Medium": "#ffc107", "🟢 Low": "#28a745"}
                        color = priority_colors.get(item['priority'], '#17a2b8')
                        
                        st.markdown(
                            f"""
                            <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 4px solid {color};">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <strong style="color: {color};">{item['priority']}</strong> - {item['item']}
                                        <br><small><strong>Owner:</strong> {item['owner']} | <strong>Due:</strong> {item['due']}</small>
                                    </div>
                                    <button style="background: {color}; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; font-size: 12px; font-weight: 600;">Execute</button>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
        
        else:
            # Fallback for no metrics
            st.markdown("### ⚙️ CTO Operations Dashboard")
            
            # Basic CTO metrics if no advanced system available
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("System Uptime", "99.8%", "+0.2%")
            with col2:
                st.metric("Incident Resolution", "2.4 hrs", "-0.6 hrs")
            with col3:
                st.metric("Cloud Utilization", "78%", "+5%")
            with col4:
                st.metric("Security Score", "A-", "Excellent")
            
            st.info("Enhanced CTO metrics loading... Please check metric configuration.")
    
    # Add HBCU Integration if available
    if HBCU_INTEGRATION_AVAILABLE and hbcu_integrator:
        st.markdown("---")
        hbcu_integrator.render_hbcu_dashboard_section('cto')


elif persona == "Project Manager View":
    st.markdown("### 📋 Project Management Dashboard - Portfolio & Delivery Excellence")
    
    # Enhanced Executive Summary Row
    st.markdown("#### 📊 Project Portfolio Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "📊 Active Projects", 
            "8", 
            "2 new this quarter",
            help="Currently active project initiatives"
        )
    with col2:
        st.metric(
            "⏰ On Schedule", 
            "87%", 
            "+5% improved",
            help="Projects meeting timeline commitments"
        )
    with col3:
        st.metric(
            "👥 Resource Utilization", 
            "92%", 
            "+3% optimized",
            help="Team capacity and allocation efficiency"
        )
    with col4:
        st.metric(
            "💰 Budget Performance", 
            "96%", 
            "On target",
            help="Projects within budget parameters"
        )
    with col5:
        st.metric(
            "📈 Portfolio Health", 
            "8.1/10", 
            "+0.3 improved",
            help="Overall portfolio performance score"
        )

    # Project Management AI Insights
    st.markdown("---")
    st.markdown(
        """
        <div class="optimization-highlight">
            🤖 <strong>PM AI Insight:</strong> Student Portal project shows 85% completion with early delivery potential. 
            Resource reallocation from Infrastructure project could accelerate Digital Learning initiative by 3 weeks.
            <span style="float: right;">
                <button style="background: rgba(255,255,255,0.2); border: 1px solid white; color: white; padding: 4px 8px; border-radius: 4px; cursor: pointer;">Optimize Schedule →</button>
            </span>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Enhanced PM Tab Configuration
    if PM_METRICS_AVAILABLE:
        tab_config = [
            ("📊 Portfolio Dashboard", ["project_portfolio_dashboard_metrics", "project_charter_metrics"]),
            ("⏰ Timeline & Budget", ["project_timeline_budget_performance"]),
            ("📋 Requirements & RAID", ["requirements_traceability_matrix", "raid_log_metrics"]),
            ("🤖 AI Project Intelligence", []),  # NEW AI TAB
            ("👥 Resources & Communication", ["resource_allocation_metrics", "stakeholder_communication_metrics"]),
            ("📈 Executive Summary", [])
        ]
        
        tab_names = [config[0] for config in tab_config]
        tabs = st.tabs(tab_names)
        
        available_pm_metrics = list(PM_METRICS.keys()) if PM_METRICS_AVAILABLE else []
        
        for idx, (tab, (tab_name, metrics_list)) in enumerate(zip(tabs, tab_config)):
            with tab:
                if tab_name == "📊 Portfolio Dashboard":
                    st.markdown("### 📊 Project Portfolio Health Dashboard")
                    
                    # Portfolio action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button("📊 Portfolio Report", key="pm_portfolio"):
                            st.success("Portfolio report generated!")
                    with col2:
                        if st.button("🎯 Resource Review", key="pm_resources"):
                            st.info("Resource analysis initiated...")
                    with col3:
                        if st.button("⏰ Timeline Update", key="pm_timeline"):
                            st.success("Timeline data refreshed!")
                    with col4:
                        if st.button("📧 Status Update", key="pm_status"):
                            st.success("Stakeholder update sent!")
                    
                    st.markdown("---")
                    
                    # Project status overview
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 🎯 Project Status Overview")
                        
                        # Project status indicators
                        projects_status = [
                            ("Student Portal Upgrade", 85, "success", "Q4 2024"),
                            ("Digital Learning Platform", 72, "success", "Q1 2025"),
                            ("Infrastructure Modernization", 45, "warning", "Q2 2025"),
                            ("Data Analytics Implementation", 60, "info", "Q1 2025"),
                            ("Security Enhancement", 30, "warning", "Q3 2025")
                        ]
                        
                        for project, progress, status, timeline in projects_status:
                            color_map = {"success": "#28a745", "warning": "#ffc107", "info": "#17a2b8", "danger": "#dc3545"}
                            st.markdown(f"**{project}** (*{timeline}*)")
                            st.progress(progress/100, text=f"{progress}% Complete")
                            st.markdown("")
                    
                    with col2:
                        st.markdown("#### 📊 Key Performance Indicators")
                        
                        kpi_metrics = [
                            ("Project Velocity", "8.3", "Stories/Sprint"),
                            ("Stakeholder Satisfaction", "4.2/5", "Excellent rating"),
                            ("Quality Score", "94%", "Above target"),
                            ("Risk Mitigation", "89%", "Well managed"),
                            ("Change Request Rate", "12%", "Within tolerance")
                        ]
                        
                        for metric, value, description in kpi_metrics:
                            st.metric(metric, value, description)
                    
                    # Load actual PM metrics if available
                    if "project_portfolio_dashboard_metrics" in available_pm_metrics:
                        st.markdown("---")
                        dashboard_loader.display_generic_metric('pm', 'project_portfolio_dashboard_metrics', st.container())
                
                elif tab_name == "⏰ Timeline & Budget":
                    st.markdown("### ⏰ Project Timeline & Budget Performance")
                    
                    # Timeline and budget overview
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(
                            """
                            <div class="success-box">
                                <h4>✅ On Track Projects</h4>
                                <p><strong>Count:</strong> 5 projects</p>
                                <p><strong>Budget:</strong> $1.8M</p>
                                <p><strong>Timeline:</strong> Meeting milestones</p>
                                <button style="width:100%; background:#28a745; color:white; border:none; padding:8px; border-radius:4px;">View Details</button>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    
                    with col2:
                        st.markdown(
                            """
                            <div class="warning-box">
                                <h4>⚠️ At Risk Projects</h4>
                                <p><strong>Count:</strong> 2 projects</p>
                                <p><strong>Budget:</strong> $650K</p>
                                <p><strong>Delay Risk:</strong> 2-3 weeks</p>
                                <button style="width:100%; background:#ffc107; color:black; border:none; padding:8px; border-radius:4px;">Mitigate Risk</button>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    
                    with col3:
                        st.markdown(
                            """
                            <div class="info-box">
                                <h4>📈 Planned Projects</h4>
                                <p><strong>Count:</strong> 3 projects</p>
                                <p><strong>Budget:</strong> $950K</p>
                                <p><strong>Start:</strong> Q2 2025</p>
                                <button style="width:100%; background:#17a2b8; color:white; border:none; padding:8px; border-radius:4px;">Review Plans</button>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("---")
                    
                    # Timeline performance tracking
                    if "project_timeline_budget_performance" in available_pm_metrics:
                        dashboard_loader.display_generic_metric('pm', 'project_timeline_budget_performance', st.container())
                    else:
                        st.info("Timeline and budget performance metrics loading...")
                
                elif tab_name == "📋 Requirements & RAID":
                    st.markdown("### 📋 Requirements Traceability & RAID Management")
                    
                    # RAID overview
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 📊 RAID Log Summary")
                        
                        raid_summary = [
                            ("🔴 Risks", "8", "Active monitoring"),
                            ("⚡ Actions", "15", "In progress"),
                            ("❗ Issues", "3", "Being resolved"),
                            ("📝 Decisions", "12", "Documented")
                        ]
                        
                        for category, count, status in raid_summary:
                            st.metric(category, count, status)
                    
                    with col2:
                        st.markdown("#### 📊 Requirements Traceability")
                        
                        requirements_metrics = [
                            ("Total Requirements", "147", "Documented"),
                            ("Traced to Design", "92%", "Well linked"),
                            ("Test Coverage", "89%", "Good coverage"),
                            ("Change Requests", "8", "This quarter")
                        ]
                        
                        for metric, value, status in requirements_metrics:
                            st.metric(metric, value, status)
                    
                    # Load RAID and requirements metrics
                    if "raid_log_metrics" in available_pm_metrics:
                        st.markdown("---")
                        dashboard_loader.display_generic_metric('pm', 'raid_log_metrics', st.container())
                    
                    if "requirements_traceability_matrix" in available_pm_metrics:
                        st.markdown("---")
                        dashboard_loader.display_generic_metric('pm', 'requirements_traceability_matrix', st.container())
                
                elif tab_name == "🤖 AI Project Intelligence":
                    st.markdown("### 🤖 AI-Powered Project Intelligence")
                    
                    # AI Project Insights
                    st.markdown("#### 💡 Intelligent Project Recommendations")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("##### 🎯 Optimization Opportunities")
                        
                        project_opportunities = [
                            {
                                "title": "Resource Reallocation",
                                "impact": "3 weeks faster delivery",
                                "projects": "Digital Learning Platform",
                                "confidence": "89%",
                                "effort": "Low"
                            },
                            {
                                "title": "Parallel Task Execution",
                                "impact": "$25K budget savings",
                                "projects": "Infrastructure Modernization", 
                                "confidence": "82%",
                                "effort": "Medium"
                            },
                            {
                                "title": "Scope Optimization",
                                "impact": "15% efficiency gain",
                                "projects": "Security Enhancement",
                                "confidence": "91%",
                                "effort": "Low"
                            }
                        ]
                        
                        for opp in project_opportunities:
                            effort_color = {"Low": "#28a745", "Medium": "#ffc107", "High": "#dc3545"}[opp["effort"]]
                            st.markdown(
                                f"""
                                <div class="info-box" style="border-left-color: {effort_color};">
                                    <h4>🚀 {opp['title']}</h4>
                                    <p><strong>Impact:</strong> {opp['impact']}</p>
                                    <p><strong>Project:</strong> {opp['projects']}</p>
                                    <p><strong>Confidence:</strong> {opp['confidence']}</p>
                                    <button style="background:#288FFA; color:white; border:none; padding:6px 12px; border-radius:4px; margin-top:8px;">Apply</button>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    
                    with col2:
                        st.markdown("##### 📊 Predictive Project Analytics")
                        
                        # Project predictions
                        st.markdown("**Project Delivery Forecast:**")
                        st.progress(0.87, text="87% probability of on-time delivery")
                        
                        st.markdown("**Resource Optimization Potential:**")
                        st.progress(0.73, text="73% efficiency improvement possible")
                        
                        st.markdown("**Risk Probability Assessment:**")
                        st.progress(0.24, text="24% chance of scope creep - moderate risk")
                        
                        st.markdown("---")
                        
                        st.markdown("**🎯 AI Project Insights:**")
                        st.markdown("• **Critical Path:** Student Portal has 2-day buffer")
                        st.markdown("• **Resource Conflicts:** Q1 2025 peak capacity concern")
                        st.markdown("• **Quality Prediction:** 94% test coverage achievable")
                        st.markdown("• **Stakeholder Health:** 4.2/5 satisfaction maintained")
                    
                    # Project Health Tracking
                    st.markdown("---")
                    st.markdown("#### 📈 AI-Enhanced Project Tracking")
                    
                    project_health_data = pd.DataFrame({
                        'Project': ['Student Portal', 'Digital Learning', 'Infrastructure', 'Data Analytics'],
                        'Health Score': [9.2, 8.5, 6.8, 7.9],
                        'Delivery Confidence': ['95%', '87%', '68%', '82%'],
                        'Resource Health': ['Optimal', 'Good', 'Strained', 'Good'],
                        'Risk Level': ['Low', 'Low', 'Medium', 'Low']
                    })
                    
                    st.dataframe(project_health_data, use_container_width=True)
                
                elif tab_name == "👥 Resources & Communication":
                    st.markdown("### 👥 Resource Allocation & Stakeholder Communication")
                    
                    # Resource allocation overview
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### 👥 Team Allocation")
                        st.metric("Development Team", "92%", "Capacity")
                        st.metric("Design Resources", "78%", "Utilization")
                        st.metric("QA Team", "85%", "Allocation")
                        
                    with col2:
                        st.markdown("#### 📊 Communication Health")
                        st.metric("Stakeholder Engagement", "4.2/5", "Strong")
                        st.metric("Meeting Effectiveness", "87%", "Good")
                        st.metric("Communication Frequency", "Weekly", "Optimal")
                        
                    with col3:
                        st.markdown("#### 🎯 Delivery Metrics")
                        st.metric("Sprint Velocity", "8.3", "Points/Sprint")
                        st.metric("Feature Completion", "94%", "This quarter")
                        st.metric("Client Satisfaction", "4.4/5", "Excellent")
                    
                    # Load resource and communication metrics
                    if "resource_allocation_metrics" in available_pm_metrics:
                        st.markdown("---")
                        dashboard_loader.display_generic_metric('pm', 'resource_allocation_metrics', st.container())
                    
                    if "stakeholder_communication_metrics" in available_pm_metrics:
                        st.markdown("---")
                        dashboard_loader.display_generic_metric('pm', 'stakeholder_communication_metrics', st.container())
                
                elif tab_name == "📈 Executive Summary":
                    st.markdown("### 📈 Project Management Executive Summary")
                    
                    # Executive summary cards
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### 📊 Portfolio Performance")
                        st.metric("On-Time Delivery", "87%", "Above target")
                        st.metric("Budget Adherence", "96%", "Excellent")
                        st.metric("Quality Score", "94%", "High quality")
                        
                    with col2:
                        st.markdown("#### 👥 Team & Resources")
                        st.metric("Resource Utilization", "92%", "Optimal")
                        st.metric("Team Satisfaction", "4.3/5", "Strong")
                        st.metric("Skill Development", "89%", "Good progress")
                        
                    with col3:
                        st.markdown("#### 🎯 Business Value")
                        st.metric("Value Delivered", "$2.1M", "This quarter")
                        st.metric("ROI Achievement", "3.4x", "Above target")
                        st.metric("Stakeholder NPS", "+45", "Excellent")
                    
                    st.markdown("---")
                    
                    # Project management action items
                    st.markdown("#### ⚡ Critical PM Action Items")
                    
                    pm_actions = [
                        {"priority": "🔴 High", "item": "Resolve Infrastructure project resource conflict", "owner": "PM Lead", "due": "This week"},
                        {"priority": "🟡 Medium", "item": "Update Q1 project portfolio roadmap", "owner": "Portfolio Manager", "due": "End of month"},
                        {"priority": "🟢 Low", "item": "Complete stakeholder satisfaction survey", "owner": "PMO", "due": "Next quarter"},
                        {"priority": "🔴 High", "item": "Approve Digital Learning platform scope change", "owner": "Steering Committee", "due": "Next meeting"}
                    ]
                    
                    for item in pm_actions:
                        priority_colors = {"🔴 High": "#dc3545", "🟡 Medium": "#ffc107", "🟢 Low": "#28a745"}
                        color = priority_colors.get(item['priority'], '#17a2b8')
                        
                        st.markdown(
                            f"""
                            <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 4px solid {color};">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <strong style="color: {color};">{item['priority']}</strong> - {item['item']}
                                        <br><small><strong>Owner:</strong> {item['owner']} | <strong>Due:</strong> {item['due']}</small>
                                    </div>
                                    <button style="background: {color}; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; font-size: 12px; font-weight: 600;">Manage</button>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
        
        else:
            # Fallback for no PM metrics
            st.markdown("### 📋 Project Management Dashboard")
            
            # Basic PM metrics if no advanced system available
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Active Projects", "8", "")
            with col2:
                st.metric("On Schedule", "87%", "+5%")
            with col3:
                st.metric("Resource Utilization", "92%", "+3%")
            with col4:
                st.metric("Portfolio Health", "8.1/10", "+0.3")
            
            st.info("Enhanced PM metrics loading... Please check PM module integration.")
    
    else:
        # Fallback when PM metrics not available
        st.warning("PM metric system not available. Please check PM module integration.")
        
        # Show basic PM dashboard
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Projects", "8", "Currently in progress")
        with col2:
            st.metric("On Schedule", "87%", "+5% improved")
        with col3:
            st.metric("Resource Utilization", "92%", "+3% optimized")
        with col4:
            st.metric("Portfolio Health", "8.1/10", "+0.3 improved")

elif persona == "HBCU Institutional View":
    st.markdown("### 🎓 HBCU Institutional Performance Dashboard")
    st.markdown("*Paul Quinn College Mission-Aligned Analytics*")
    
    # Enhanced Executive Summary Row
    st.markdown("#### 📊 Institutional Excellence Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "👥 Students Served", 
            "5,800", 
            "+3.2% growth",
            help="Total undergraduate enrollment"
        )
    with col2:
        st.metric(
            "💰 Cost per Student", 
            "$8,224", 
            "40% below peer avg",
            help="Total cost of education per student"
        )
    with col3:
        st.metric(
            "📊 Mission Alignment", 
            "94%", 
            "Outstanding",
            help="Technology investments aligned with HBCU mission"
        )
    with col4:
        st.metric(
            "🎯 Student Success Rate", 
            "78%", 
            "+5% improved",
            help="Technology-enhanced graduation rate"
        )
    with col5:
        st.metric(
            "🏆 Peer Ranking", 
            "2nd", 
            "of 12 HBCUs",
            help="Technology efficiency ranking among peer institutions"
        )
    
    # HBCU Mission AI Insights
    st.markdown("---")
    st.markdown(
        """
        <div class="optimization-highlight">
            🤖 <strong>Institutional AI Insight:</strong> HBCU mission alignment at 94% - highest among peers. 
            Digital equity grant opportunity: $500K available for student success technology. 
            Current efficiency ranks 2nd among 12 peer HBCUs with 40% cost advantage.
            <span style="float: right;">
                <button style="background: rgba(255,255,255,0.2); border: 1px solid white; color: white; padding: 4px 8px; border-radius: 4px; cursor: pointer;">Apply for Grants →</button>
            </span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    if HBCU_INTEGRATION_AVAILABLE and hbcu_integrator:
        hbcu_integrator.render_institutional_hbcu_view()
        
        # Enhanced institutional analysis with improved structure
        st.markdown("---")
        st.markdown("## 📊 Institutional Benchmarking & Analysis")
        
        # Enhanced benchmark comparison tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎯 Mission Alignment", 
            "💰 Financial Efficiency", 
            "🎓 Student Outcomes",
            "📈 Strategic Summary"
        ])
        
        with tab1:
            st.markdown("### 🎯 Mission-Critical Investment Analysis")
            
            # Mission alignment action buttons
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("📊 Mission Report", key="hbcu_mission"):
                    st.success("Mission alignment report generated!")
            with col2:
                if st.button("🎯 Optimize Alignment", key="hbcu_optimize"):
                    st.info("Optimization analysis initiated...")
            with col3:
                if st.button("📈 Track Progress", key="hbcu_progress"):
                    st.success("Progress tracking updated!")
            with col4:
                if st.button("📧 Board Update", key="hbcu_board"):
                    st.success("Board update prepared!")
            
            st.markdown("---")
            
            # Create mission alignment metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # Mission alignment scoring with enhanced styling
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
                
                # Mission impact summary
                st.markdown("#### 🎯 Mission Impact Summary")
                impact_metrics = [
                    ("Direct Student Impact", "4,200 students", "+12%"),
                    ("Faculty Empowerment", "89% satisfaction", "+15%"),
                    ("Community Engagement", "45 partnerships", "+8%")
                ]
                
                for metric, value, change in impact_metrics:
                    st.metric(metric, value, change)
            
            with col2:
                # ROI by mission category with enhanced context
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
                
                # Strategic priorities
                st.markdown("#### 🚀 Strategic Priority Areas")
                st.markdown(
                    """
                    <div class="success-box">
                        <strong>Top Priority:</strong> Student Success Technology<br>
                        <small>ROI: 4.2x | Impact: 4,200 students</small>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                st.markdown(
                    """
                    <div class="info-box">
                        <strong>Growth Area:</strong> Digital Learning Platform<br>
                        <small>ROI: 3.8x | Potential: +25% engagement</small>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

        with tab2:
            st.markdown("### 💰 Financial Efficiency vs Peer HBCUs")
            
            # Financial efficiency overview
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(
                    """
                    <div class="success-box">
                        <h4>🏆 Cost Leadership</h4>
                        <p><strong>Per Student Cost:</strong> $8,224</p>
                        <p><strong>Peer Advantage:</strong> 40% lower</p>
                        <p><strong>Ranking:</strong> 2nd of 12</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown(
                    """
                    <div class="info-box">
                        <h4>📊 Efficiency Metrics</h4>
                        <p><strong>Admin Ratio:</strong> 18%</p>
                        <p><strong>Peer Average:</strong> 25%</p>
                        <p><strong>Savings:</strong> $420K annually</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            
            with col3:
                st.markdown(
                    """
                    <div class="warning-box">
                        <h4>🎯 Optimization Target</h4>
                        <p><strong>Current Score:</strong> 94/100</p>
                        <p><strong>Target:</strong> 98/100</p>
                        <p><strong>Gap:</strong> $85K potential</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            
            st.markdown("---")
            
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
            st.markdown("### 🎓 Technology Impact on Student Success")
            
            # Student success impact cards
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 📈 Graduation Impact")
                st.metric("Tech-Enhanced Rate", "78%", "+16% vs baseline")
                st.metric("Retention Rate", "89%", "+12% vs peers")
                st.metric("Student Satisfaction", "4.6/5", "Exceptional")
                
            with col2:
                st.markdown("#### 💻 Digital Engagement")
                st.metric("LMS Active Users", "94%", "Daily engagement")
                st.metric("Digital Literacy", "91%", "Above standard")
                st.metric("Online Course Success", "87%", "+8% improved")
                
            with col3:
                st.markdown("#### 🎯 Support Effectiveness")
                st.metric("Tech Support Usage", "78%", "High adoption")
                st.metric("Tutoring Success", "85%", "Strong outcomes")
                st.metric("Resource Access", "96%", "Excellent availability")
            
            st.markdown("---")
            
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
            st.markdown("#### 🏆 Key Technology Success Indicators")
            metric_cols = st.columns(4)
            
            with metric_cols[0]:
                st.metric("Digital Literacy", "94%", "+12%", 
                        help="Students meeting digital competency standards")
            with metric_cols[1]:
                st.metric("LMS Engagement", "87%", "+8%",
                        help="Active weekly LMS users")
            with metric_cols[2]:
                st.metric("Tech Support Satisfaction", "4.6/5", "+0.3",
                        help="Student satisfaction rating")
            with metric_cols[3]:
                st.metric("Course Completion", "91%", "+6%",
                        help="Online course completion rate")
        
        with tab4:
            st.markdown("### 📈 HBCU Strategic Excellence Summary")
            
            # Strategic summary overview
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 🎯 Mission Excellence")
                st.metric("Mission Alignment", "94%", "Outstanding")
                st.metric("Student Impact", "5,800", "Lives changed")
                st.metric("Community Engagement", "45", "Partnerships")
                
            with col2:
                st.markdown("#### 💰 Financial Leadership")
                st.metric("Cost Efficiency", "40%", "Below peers")
                st.metric("Resource Optimization", "$420K", "Annual savings")
                st.metric("ROI Achievement", "3.6x", "Above target")
                
            with col3:
                st.markdown("#### 🏆 Competitive Advantage")
                st.metric("Peer Ranking", "2nd", "of 12 HBCUs")
                st.metric("Innovation Score", "91%", "Leading edge")
                st.metric("Sustainability", "A-", "Long-term viable")
            
            st.markdown("---")
            
            # Strategic action items for HBCU context
            st.markdown("#### 🚀 Strategic HBCU Initiatives")
            
            hbcu_actions = [
                {"priority": "🔴 High", "item": "Apply for $500K digital equity grant", "owner": "Grants Team", "due": "Next month"},
                {"priority": "🟡 Medium", "item": "Expand peer HBCU technology collaboration", "owner": "Strategic Partnerships", "due": "Q2 2025"},
                {"priority": "🟢 Low", "item": "Document best practices for HBCU network", "owner": "IT Leadership", "due": "End of year"},
                {"priority": "🔴 High", "item": "Launch student success analytics platform", "owner": "Academic Affairs", "due": "Q1 2025"}
            ]
            
            for item in hbcu_actions:
                priority_colors = {"🔴 High": "#dc3545", "🟡 Medium": "#ffc107", "🟢 Low": "#28a745"}
                color = priority_colors.get(item['priority'], '#17a2b8')
                
                st.markdown(
                    f"""
                    <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 4px solid {color};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong style="color: {color};">{item['priority']}</strong> - {item['item']}
                                <br><small><strong>Owner:</strong> {item['owner']} | <strong>Due:</strong> {item['due']}</small>
                            </div>
                            <button style="background: {color}; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; font-size: 12px; font-weight: 600;">Execute</button>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # HBCU Network Insights
            st.markdown("---")
            st.markdown("#### 🌐 HBCU Network Excellence")
            
            network_insights = pd.DataFrame({
                'HBCU Institution': ['Paul Quinn College', 'Spelman College', 'Morehouse College', 'Howard University'],
                'Tech Efficiency Score': [94, 87, 82, 89],
                'Cost per Student': [8224, 12500, 11200, 15800],
                'Student Success Rate': [78, 84, 81, 86],
                'Innovation Index': [91, 88, 85, 92]
            })
            
            st.dataframe(
                network_insights.style.format({
                    'Cost per Student': '${:,.0f}'
                }),
                use_container_width=True
            )
    
    else:
        # Fallback when HBCU integration not available
        st.warning("HBCU institutional metrics integration not available.")
        
        # Basic institutional metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Students Served", "5,800", "+3.2%")
        with col2:
            st.metric("Cost per Student", "$8,224", "40% below avg")
        with col3:
            st.metric("Mission Alignment", "94%", "Outstanding")
        with col4:
            st.metric("Peer Ranking", "2nd", "of 12 HBCUs")

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
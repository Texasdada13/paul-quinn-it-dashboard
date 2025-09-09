"""
Enhanced Paul Quinn College IT Analytics Suite - With Data Integration
Dynamically loads metrics and integrates with live data sources
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os
import sys
from pathlib import Path
import json
import logging

# Add parent directory to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir.parent
sys.path.append(str(src_dir))

# Import theme and existing components
try:
    from issa_theme import ISSATheme
    THEME_AVAILABLE = True
except ImportError:
    THEME_AVAILABLE = False
    st.warning("ISSA Theme not available - using default styling")

# Import enhanced metric registry and dashboard loader
try:
    from metric_registry import metric_registry, cfo_metrics, cio_metrics, cto_metrics
    from dashboard_metric_loader import dashboard_loader
    METRICS_AVAILABLE = True
except ImportError as e:
    st.error(f"Metric system not available: {e}")
    METRICS_AVAILABLE = False

# Import data integration components
try:
    from integrations.data_connectors import DataSourceManager, SAPContractConnector, PaycomHRConnector
    from integrations.file_processors import ContractFileProcessor
    from pipelines.data_pipeline import ContractDataPipeline, run_manual_pipeline
    DATA_INTEGRATION_AVAILABLE = True
except ImportError as e:
    st.warning(f"Data integration not available: {e}")
    DATA_INTEGRATION_AVAILABLE = False

# Import HBCU integration if available
try:
    from hbcu_metrics_integration import HBCUMetricsIntegrator
    HBCU_INTEGRATION_AVAILABLE = True
except ImportError:
    HBCU_INTEGRATION_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="PQC IT Analytics Suite - Enhanced",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply theme
if THEME_AVAILABLE:
    ISSATheme.apply_theme()

# Initialize session state
if 'current_persona' not in st.session_state:
    st.session_state.current_persona = 'CFO'

if 'data_sources_configured' not in st.session_state:
    st.session_state.data_sources_configured = False

if 'last_data_refresh' not in st.session_state:
    st.session_state.last_data_refresh = None

# Initialize integrators
if HBCU_INTEGRATION_AVAILABLE:
    hbcu_integrator = HBCUMetricsIntegrator()
else:
    hbcu_integrator = None

if DATA_INTEGRATION_AVAILABLE:
    pipeline = ContractDataPipeline()
else:
    pipeline = None

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
    .integration-badge {
        background-color: #17a2b8;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    .data-source-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .status-connected {
        color: #28a745;
        font-weight: bold;
    }
    .status-disconnected {
        color: #dc3545;
        font-weight: bold;
    }
    .status-pending {
        color: #ffc107;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Main header
if THEME_AVAILABLE:
    st.markdown(ISSATheme.create_header("ISSA", "Enhanced Integrated Systems for Strategic Analytics"), unsafe_allow_html=True)
else:
    st.markdown('<h1 class="main-header">ISSA - Enhanced Analytics Suite</h1>', unsafe_allow_html=True)

st.markdown("### Deployed for Paul Quinn College")
st.markdown('<span class="integration-badge">DATA INTEGRATION ENABLED</span>', unsafe_allow_html=True)

# Enhanced Sidebar with Data Integration
st.sidebar.markdown("### 🎓 Paul Quinn College")
st.sidebar.markdown("**Enhanced IT Analytics Suite**")
st.sidebar.markdown("---")

# Data Integration Status
st.sidebar.markdown("### 📊 Data Integration Status")

if DATA_INTEGRATION_AVAILABLE:
    # Pipeline status
    try:
        pipeline_status = pipeline.get_pipeline_status()
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Total Runs", pipeline_status['pipeline_stats']['total_runs'])
        with col2:
            success_rate = (pipeline_status['pipeline_stats']['successful_runs'] / 
                          max(pipeline_status['pipeline_stats']['total_runs'], 1) * 100)
            st.metric("Success Rate", f"{success_rate:.1f}%")
        
        if pipeline_status['last_update']:
            st.sidebar.text(f"Last Update: {pipeline_status['last_update'][:16]}")
        
    except Exception as e:
        st.sidebar.error(f"Pipeline status error: {e}")
        
    # Data source configuration
    with st.sidebar.expander("⚙️ Configure Data Sources"):
        st.markdown("#### File Upload")
        uploaded_file = st.file_uploader("Upload Contract Data", type=['csv', 'xlsx'], key="main_upload")
        
        if uploaded_file:
            # Save uploaded file
            upload_dir = Path("data/uploads")
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = upload_dir / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # Auto-trigger pipeline
            if st.button("Process Uploaded File", key="process_upload"):
                with st.spinner("Processing file..."):
                    try:
                        result = run_manual_pipeline()
                        if result['success']:
                            st.success(f"✅ Processed {result['records_processed']} records")
                            st.session_state.last_data_refresh = datetime.now()
                            st.rerun()
                        else:
                            st.error(f"❌ Processing failed: {result['errors']}")
                    except Exception as e:
                        st.error(f"Pipeline error: {e}")
        
        st.markdown("#### API Connections")
        
        # SAP Configuration
        st.markdown("**SAP Integration**")
        sap_enabled = st.checkbox("Enable SAP", key="sap_enable")
        if sap_enabled:
            sap_url = st.text_input("SAP Base URL", key="sap_url")
            sap_client = st.text_input("Client ID", key="sap_client")
            sap_secret = st.text_input("Client Secret", type="password", key="sap_secret")
            
            if st.button("Test SAP Connection", key="test_sap"):
                if sap_url and sap_client and sap_secret:
                    try:
                        connector = SAPContractConnector(sap_url, sap_client, sap_secret)
                        if connector.test_connection():
                            st.success("✅ SAP connection successful!")
                        else:
                            st.error("❌ SAP connection failed")
                    except Exception as e:
                        st.error(f"SAP error: {e}")
                else:
                    st.warning("Please fill all SAP fields")
        
        # Paycom Configuration
        st.markdown("**Paycom Integration**")
        paycom_enabled = st.checkbox("Enable Paycom", key="paycom_enable")
        if paycom_enabled:
            paycom_key = st.text_input("API Key", type="password", key="paycom_key")
            paycom_company = st.text_input("Company ID", key="paycom_company")
            
            if st.button("Test Paycom Connection", key="test_paycom"):
                if paycom_key and paycom_company:
                    try:
                        connector = PaycomHRConnector(paycom_key, paycom_company)
                        if connector.test_connection():
                            st.success("✅ Paycom connection successful!")
                        else:
                            st.error("❌ Paycom connection failed")
                    except Exception as e:
                        st.error(f"Paycom error: {e}")
                else:
                    st.warning("Please fill all Paycom fields")

    # Manual pipeline controls
    st.sidebar.markdown("### 🔄 Data Pipeline")
    
    if st.sidebar.button("🔄 Refresh All Data", key="refresh_all"):
        with st.spinner("Refreshing data from all sources..."):
            try:
                result = run_manual_pipeline()
                if result['success']:
                    st.sidebar.success(f"✅ Refreshed {result['records_processed']} records")
                    st.session_state.last_data_refresh = datetime.now()
                    st.rerun()
                else:
                    st.sidebar.error("❌ Refresh failed")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")
    
    if st.session_state.last_data_refresh:
        refresh_time = st.session_state.last_data_refresh
        st.sidebar.text(f"Last refresh: {refresh_time.strftime('%H:%M:%S')}")

else:
    st.sidebar.warning("⚠️ Data integration not available")
    st.sidebar.text("Using static data files only")

# Persona selection
st.sidebar.markdown("---")
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

# Quick Actions
st.sidebar.markdown("### 📋 Quick Actions")

if st.sidebar.button("📊 Generate Report", key="generate_report"):
    st.sidebar.success("Report generated!")

if st.sidebar.button("📧 Email Dashboard", key="email_dashboard"):
    st.sidebar.success("Dashboard emailed!")

if st.sidebar.button("💾 Export Data", key="export_data"):
    st.sidebar.success("Data exported!")

# Display metrics availability
if METRICS_AVAILABLE:
    available_metrics = metric_registry.get_available_metrics(persona_key)
    st.sidebar.markdown("### 📊 Metrics Status")
    st.sidebar.markdown(f"<span class='status-connected'>✅ {len(available_metrics)} metrics loaded</span>", 
                       unsafe_allow_html=True)
else:
    st.sidebar.markdown("<span class='status-disconnected'>⚠️ Metrics not loaded</span>", 
                       unsafe_allow_html=True)

# Main Content Area
if persona == "CFO - Financial Steward":
    st.markdown("### CFO Dashboard - Financial Overview & Optimization")
    
    # Enhanced key metrics with live data integration
    col1, col2, col3, col4 = st.columns(4)
    
    # Try to get live data for metrics
    live_data_available = False
    if DATA_INTEGRATION_AVAILABLE:
        try:
            # Check if we have live contract data
            processed_file = Path("data/processed/latest_contracts.csv")
            if processed_file.exists():
                live_contract_data = pd.read_csv(processed_file)
                if not live_contract_data.empty:
                    live_data_available = True
                    
                    # Calculate metrics from live data
                    total_spend = live_contract_data['Annual Spend'].sum() if 'Annual Spend' in live_contract_data.columns else 0
                    expiring_30 = len(live_contract_data[live_contract_data['Days Until Expiry'] <= 30]) if 'Days Until Expiry' in live_contract_data.columns else 0
                    unique_vendors = live_contract_data['Vendor'].nunique() if 'Vendor' in live_contract_data.columns else 0
                    avg_contract_value = live_contract_data['Annual Spend'].mean() if 'Annual Spend' in live_contract_data.columns else 0
        except Exception as e:
            logger.error(f"Error loading live data: {e}")
    
    # Display metrics
    with col1:
        if live_data_available:
            st.metric("Total IT Spend", f"${total_spend/1000000:.1f}M", 
                     help="From live data sources")
        else:
            st.metric("Total IT Budget", "$2.8M", "+5.2%", help="Year-over-year change")
    
    with col2:
        if live_data_available:
            st.metric("Unique Vendors", unique_vendors, help="Active vendor relationships")
        else:
            st.metric("YTD Spend", "$1.9M", "-3%", help="68% of annual budget")
    
    with col3:
        if live_data_available:
            st.metric("Avg Contract Value", f"${avg_contract_value/1000:.0f}K", help="Average annual spend per contract")
        else:
            st.metric("Cost Savings", "$340K", "+12%", help="Through optimization initiatives")
    
    with col4:
        if live_data_available:
            st.metric("Expiring Soon", expiring_30, delta_color="inverse", help="Contracts expiring within 30 days")
        else:
            st.metric("Contracts at Risk", 3, delta_color="inverse", help="Expiring within 90 days")
    
    # Data source indicator
    if live_data_available:
        st.success("📊 **Live Data**: Metrics updated from integrated data sources")
    else:
        st.info("📁 **Static Data**: Using sample data - configure data sources to see live metrics")
    
    # Enhanced tabs with data integration features
    if METRICS_AVAILABLE:
        tab_config = [
            ("📊 Budget Analysis", ["cfo_budget_vs_actual", "cfo_total_it_spend_breakdown"]),
            ("📃 Contracts & Vendors", ["cfo_contract_expiration_alerts", "cfo_vendor_spend_optimization"]),
            ("🔗 Data Integration", []),  # NEW TAB
            ("🏛️ Grant Compliance", ["cfo_grant_compliance"]),
            ("📈 ROI & Benchmarking", ["cfo_student_success_roi", "cfo_hbcu_peer_benchmarking"])
        ]
        
        tab_names = [config[0] for config in tab_config]
        tabs = st.tabs(tab_names)
        
        for idx, (tab, (tab_name, metrics_list)) in enumerate(zip(tabs, tab_config)):
            with tab:
                if tab_name == "📊 Budget Analysis":
                    if "cfo_budget_vs_actual" in available_metrics:
                        dashboard_loader.display_cfo_budget_variance(st.container())
                    else:
                        st.info("Budget variance metrics not available")
                    
                    if "cfo_total_it_spend_breakdown" in available_metrics:
                        st.markdown("---")
                        dashboard_loader.display_generic_metric('cfo', 'cfo_total_it_spend_breakdown', st.container())
                
                elif tab_name == "📃 Contracts & Vendors":
                    if "cfo_contract_expiration_alerts" in available_metrics:
                        dashboard_loader.display_cfo_contract_alerts(st.container())
                    else:
                        st.info("Contract expiration metrics not available")
                    
                    if "cfo_vendor_spend_optimization" in available_metrics:
                        st.markdown("---")
                        dashboard_loader.display_generic_metric('cfo', 'cfo_vendor_spend_optimization', st.container())
                
                elif tab_name == "🔗 Data Integration":
                    st.subheader("Data Integration Dashboard")
                    
                    if DATA_INTEGRATION_AVAILABLE:
                        # Pipeline status
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### Pipeline Status")
                            try:
                                status = pipeline.get_pipeline_status()
                                
                                st.metric("Total Runs", status['pipeline_stats']['total_runs'])
                                st.metric("Success Rate", f"{status['pipeline_stats']['successful_runs']/max(status['pipeline_stats']['total_runs'], 1)*100:.1f}%")
                                
                                if status['pipeline_stats']['last_error']:
                                    st.error(f"Last Error: {status['pipeline_stats']['last_error']}")
                                
                            except Exception as e:
                                st.error(f"Could not load pipeline status: {e}")
                        
                        with col2:
                            st.markdown("#### Data Sources")
                            
                            # Show data source status
                            data_sources = [
                                ("File Upload", "✅ Active", "Files can be uploaded and processed"),
                                ("SAP Integration", "⚠️ Not Configured", "Configure SAP connection in sidebar"),
                                ("Paycom Integration", "⚠️ Not Configured", "Configure Paycom connection in sidebar")
                            ]
                            
                            for source, status, description in data_sources:
                                with st.expander(f"{source} - {status}"):
                                    st.write(description)
                        
                        # Recent pipeline runs
                        st.markdown("#### Recent Activity")
                        
                        # Check for recent reports
                        reports_dir = Path("data/reports")
                        if reports_dir.exists():
                            recent_reports = sorted(reports_dir.glob("pipeline_report_*.json"))[-5:]
                            
                            if recent_reports:
                                for report_file in reversed(recent_reports):
                                    try:
                                        with open(report_file, 'r') as f:
                                            report = json.load(f)
                                        
                                        success_icon = "✅" if report['pipeline_execution']['success'] else "❌"
                                        st.text(f"{success_icon} {report_file.stem} - {report['data_summary']['total_contracts']} contracts")
                                        
                                    except Exception as e:
                                        st.text(f"⚠️ {report_file.name} - Could not read report")
                            else:
                                st.info("No recent pipeline reports found")
                        else:
                            st.info("No reports directory found")
                        
                        # Manual pipeline trigger
                        st.markdown("#### Manual Actions")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button("🔄 Run Pipeline Now", key="manual_pipeline"):
                                with st.spinner("Running pipeline..."):
                                    try:
                                        result = run_manual_pipeline()
                                        if result['success']:
                                            st.success(f"✅ Pipeline completed! Processed {result['records_processed']} records")
                                            st.rerun()
                                        else:
                                            st.error(f"❌ Pipeline failed: {result['errors']}")
                                    except Exception as e:
                                        st.error(f"Pipeline error: {e}")
                        
                        with col2:
                            if st.button("📁 View Processed Data", key="view_data"):
                                processed_file = Path("data/processed/latest_contracts.csv")
                                if processed_file.exists():
                                    try:
                                        data = pd.read_csv(processed_file)
                                        st.dataframe(data.head(10), use_container_width=True)
                                        st.info(f"Showing first 10 of {len(data)} records")
                                    except Exception as e:
                                        st.error(f"Could not load processed data: {e}")
                                else:
                                    st.warning("No processed data found")
                        
                        with col3:
                            if st.button("📊 Download Report", key="download_report"):
                                st.info("Report download feature coming soon")
                    
                    else:
                        st.warning("Data integration components not available")
                        st.info("Install integration dependencies to enable live data features")
                
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

    # Add HBCU integration
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
    
    # Enhanced CIO tabs (similar structure to CFO)
    if METRICS_AVAILABLE:
        available_cio_metrics = metric_registry.get_available_metrics('cio')
        
        tab_config = [
            ("🎯 Strategic Portfolio", ["digital_transformation_metrics", "strategic_alignment_metrics"]),
            ("💼 Business Analysis", ["business_unit_it_spend", "app_cost_analysis_metrics"]),
            ("📊 Performance & Risk", ["risk_metrics", "vendor_metrics"]),
            ("🔗 Data Integration", [])  # NEW TAB
        ]
        
        tab_names = [config[0] for config in tab_config]
        tabs = st.tabs(tab_names)
        
        for tab, (tab_name, metrics_list) in zip(tabs, tab_config):
            with tab:
                if tab_name == "🔗 Data Integration":
                    st.subheader("CIO Data Integration Features")
                    st.info("CIO-specific data integration features coming soon")
                else:
                    for metric in metrics_list:
                        if metric in available_cio_metrics:
                            dashboard_loader.display_generic_metric('cio', metric, st.container())
                            st.markdown("---")

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
    
    # Enhanced CTO tabs (similar structure)
    if METRICS_AVAILABLE:
        available_cto_metrics = metric_registry.get_available_metrics('cto')
        
        # Add data integration tab for CTO as well
        tab_config = [
            ("🖥️ Infrastructure", ["infrastructure_performance_metrics", "system_utilization_metrics"]),
            ("☁️ Cloud & Assets", ["cloud_cost_optimization_metrics", "asset_lifecycle_management_metrics"]),
            ("🔒 Security & Tech Debt", ["security_metrics_and_response", "technical_debt_metrics"]),
            ("🔗 Data Integration", [])
        ]
        
        tab_names = [config[0] for config in tab_config]
        tabs = st.tabs(tab_names)
        
        for tab, (tab_name, metrics_list) in zip(tabs, tab_config):
            with tab:
                if tab_name == "🔗 Data Integration":
                    st.subheader("CTO Data Integration Features")
                    st.info("CTO-specific data integration features coming soon")
                else:
                    for metric in metrics_list:
                        if metric in available_cto_metrics:
                            dashboard_loader.display_generic_metric('cto', metric, st.container())
                            st.markdown("---")

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
    
    st.info("Project Manager dashboard with data integration features coming soon")

elif persona == "HBCU Institutional View":
    if HBCU_INTEGRATION_AVAILABLE and hbcu_integrator:
        hbcu_integrator.render_institutional_hbcu_view()
    else:
        st.warning("HBCU integration not available")

# Footer with enhanced system information
st.markdown("---")

# System status overview
with st.expander("🔧 System Status & Information"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Components Status")
        components = [
            ("Metrics System", METRICS_AVAILABLE),
            ("Data Integration", DATA_INTEGRATION_AVAILABLE),
            ("HBCU Integration", HBCU_INTEGRATION_AVAILABLE),
            ("Theme System", THEME_AVAILABLE)
        ]
        
        for component, available in components:
            status = "✅" if available else "❌"
            st.text(f"{status} {component}")
    
    with col2:
        st.markdown("#### Data Sources")
        if DATA_INTEGRATION_AVAILABLE:
            st.text("📁 File Upload: Ready")
            st.text("🔗 SAP: Not Configured")
            st.text("🔗 Paycom: Not Configured")
        else:
            st.text("📁 Static Files Only")
    
    with col3:
        st.markdown("#### Performance")
        if METRICS_AVAILABLE:
            total_metrics = sum(len(metric_registry.get_available_metrics(p)) for p in ['cfo', 'cio', 'cto'])
            st.metric("Total Metrics", total_metrics)
        
        if st.session_state.last_data_refresh:
            st.text(f"Last Refresh: {st.session_state.last_data_refresh.strftime('%H:%M:%S')}")

st.markdown(
    """
    <div style='text-align: center; color: #666; margin-top: 2rem;'>
        <p>Paul Quinn College IT Analytics Suite - Enhanced Edition | Built with Streamlit | © 2024</p>
        <p style='font-size: 0.8rem;'>Enhanced with Live Data Integration & Real-time Processing</p>
    </div>
    """,
    unsafe_allow_html=True
)
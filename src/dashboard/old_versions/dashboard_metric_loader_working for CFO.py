"""
Dashboard Metric Loader
Dynamically loads and displays metrics based on available modules
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Optional, Any
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DashboardMetricLoader:
    """Loads and displays metrics dynamically in Streamlit dashboard"""
    
    def __init__(self):
        try:
            from metric_registry import metric_registry, cfo_metrics, cio_metrics, cto_metrics
            self.registry = metric_registry
            self.cfo = cfo_metrics
            self.cio = cio_metrics
            self.cto = cto_metrics
            logger.info("Metric registries loaded successfully")
        except ImportError as e:
            logger.error(f"Failed to import metric registries: {e}")
            st.error("Failed to load metric registries. Please check your installation.")
            raise
    
    def display_cfo_budget_variance(self, tab):
        """Display CFO Budget Variance Analysis"""
        with tab:
            st.subheader("📊 Budget vs Actual Analysis with Variance Alerts")
            
            try:
                data, module = self.cfo.get_budget_variance_data()
                
                if data is not None and not data.empty:
                    # Summary metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    total_budget = data['Initial Budget'].sum()
                    total_actual = data['Actual Spend'].sum()
                    total_variance = data['Variance Amount'].sum()
                    variance_pct = (total_variance / total_budget * 100) if total_budget > 0 else 0
                    
                    with col1:
                        st.metric("Total Budget", f"${total_budget:,.0f}")
                    with col2:
                        st.metric("Total Actual", f"${total_actual:,.0f}")
                    with col3:
                        st.metric("Variance", f"${total_variance:,.0f}", f"{variance_pct:.1f}%")
                    with col4:
                        overruns = len(data[data['Variance Alert'] == 'Overrun'])
                        st.metric("Overruns", overruns, delta_color="inverse")
                    
                    # Variance by category chart
                    fig = px.bar(data, x='Budget Category', y='Variance Amount', 
                                color='Variance Alert',
                                color_discrete_map={'OK': 'green', 'Warning': 'yellow', 'Overrun': 'red'},
                                title="Budget Variance by Category")
                    st.plotly_chart(fig, use_container_width=True, key="cfo_budget_variance_chart")
                    
                    # Detailed table with alerts
                    st.subheader("Detailed Budget Analysis")
                    
                    # Filter options
                    col1, col2 = st.columns(2)
                    with col1:
                        period_filter = st.multiselect("Filter by Period", 
                                                     options=data['Period'].unique(),
                                                     default=data['Period'].unique(),
                                                     key="cfo_period_filter")
                    with col2:
                        alert_filter = st.multiselect("Filter by Alert Status",
                                                    options=data['Variance Alert'].unique(),
                                                    default=data['Variance Alert'].unique(),
                                                    key="cfo_alert_filter")
                    
                    filtered_data = data[
                        (data['Period'].isin(period_filter)) & 
                        (data['Variance Alert'].isin(alert_filter))
                    ]
                    
                    # Apply styling safely
                    def style_alerts(val):
                        if val == 'Overrun':
                            return 'background-color: #ffcccc'
                        elif val == 'Warning':
                            return 'background-color: #ffffcc'
                        return ''
                    
                    styled_df = filtered_data.style.map(
                        style_alerts,
                        subset=['Variance Alert']
                    )
                    
                    st.dataframe(styled_df, use_container_width=True)
                else:
                    st.warning("Budget variance data not available or empty")
            except Exception as e:
                logger.error(f"Error displaying budget variance: {e}")
                st.error(f"Error loading budget variance data: {str(e)}")
    
    def display_cfo_contract_alerts(self, tab):
        """Display CFO Contract Expiration Alerts"""
        with tab:
            st.subheader("🎯 Contract Expiration Alerts")
            
            try:
                data, module = self.cfo.get_contract_alerts()
                
                if data is not None and not data.empty:
                    # Alert summary
                    col1, col2, col3, col4 = st.columns(4)
                    
                    critical = len(data[data['Alert Status'] == 'Critical'])
                    warning = len(data[data['Alert Status'] == 'Warning'])
                    total_value = data[data['Alert Status'].isin(['Critical', 'Warning'])]['Annual Spend'].sum()
                    
                    with col1:
                        st.metric("Critical (<30 days)", critical, delta_color="inverse")
                    with col2:
                        st.metric("Warning (<90 days)", warning, delta_color="inverse")
                    with col3:
                        st.metric("At Risk Value", f"${total_value:,.0f}")
                    with col4:
                        st.metric("Total Contracts", len(data))
                    
                    # Timeline visualization - with better error handling
                    expiring_contracts = data[data['Days Until Expiry'] <= 180].copy()
                    
                    if not expiring_contracts.empty:
                        try:
                            # Ensure date columns are datetime
                            expiring_contracts['Contract Start Date'] = pd.to_datetime(expiring_contracts['Contract Start Date'])
                            expiring_contracts['Contract End Date'] = pd.to_datetime(expiring_contracts['Contract End Date'])
                            
                            fig = px.timeline(
                                expiring_contracts,
                                x_start='Contract Start Date',
                                x_end='Contract End Date',
                                y='Vendor',
                                color='Alert Status',
                                color_discrete_map={'Critical': 'red', 'Warning': 'orange', 'OK': 'green'},
                                title="Contract Timeline - Next 180 Days",
                                hover_data=['System/Product', 'Annual Spend', 'Days Until Expiry']
                            )
                            fig.update_yaxes(autorange="reversed")  # Reverse y-axis for better readability
                            st.plotly_chart(fig, use_container_width=True, key="cfo_contract_timeline")
                        except Exception as e:
                            logger.warning(f"Timeline visualization failed: {e}")
                            # Fallback to bar chart
                            fig = px.bar(expiring_contracts, 
                                       x='Vendor', 
                                       y='Days Until Expiry',
                                       color='Alert Status',
                                       color_discrete_map={'Critical': 'red', 'Warning': 'orange', 'OK': 'green'},
                                       title="Days Until Contract Expiry")
                            st.plotly_chart(fig, use_container_width=True, key="cfo_contract_bar")
                    
                    # Critical contracts table
                    st.subheader("⚠️ Contracts Requiring Immediate Attention")
                    critical_contracts = data[data['Alert Status'].isin(['Critical', 'Warning'])].sort_values('Days Until Expiry')
                    
                    if not critical_contracts.empty:
                        display_columns = ['Vendor', 'System/Product', 'Contract End Date', 
                                         'Days Until Expiry', 'Annual Spend', 'Renewal Option']
                        
                        # Add negotiation column if it exists
                        if 'Negotiation Recommended' in critical_contracts.columns:
                            display_columns.append('Negotiation Recommended')
                            
                            styled_df = critical_contracts[display_columns].style.map(
                                lambda x: 'color: red; font-weight: bold' if x == 'Yes' else '',
                                subset=['Negotiation Recommended']
                            )
                        else:
                            styled_df = critical_contracts[display_columns]
                        
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.success("No contracts require immediate attention")
                else:
                    st.warning("Contract data not available or empty")
            except Exception as e:
                logger.error(f"Error displaying contract alerts: {e}")
                st.error(f"Error loading contract data: {str(e)}")
    
    def display_cfo_grant_compliance(self, tab):
        """Display CFO Grant Compliance Dashboard"""
        with tab:
            st.subheader("🏛️ Grant Compliance Dashboard")
            
            try:
                data, module = self.cfo.get_grant_compliance_data()
                
                if data is not None and not data.empty:
                    # Compliance overview
                    col1, col2, col3, col4 = st.columns(4)
                    
                    avg_compliance = data['Compliance Rate (%)'].mean()
                    at_risk_grants = len(data[data['Risk Level'] != 'Low'])
                    total_awarded = data['Award Amount ($)'].sum()
                    total_unspent = data['Unspent Balance ($)'].sum()
                    
                    with col1:
                        st.metric("Avg Compliance Rate", f"{avg_compliance:.1f}%")
                    with col2:
                        st.metric("At-Risk Grants", at_risk_grants, delta_color="inverse")
                    with col3:
                        st.metric("Total Awarded", f"${total_awarded:,.0f}")
                    with col4:
                        st.metric("Unspent Balance", f"${total_unspent:,.0f}")
                    
                    # Compliance by grant
                    fig = px.bar(data, x='Grant Program/Source', y='Compliance Rate (%)',
                               color='Risk Level',
                               color_discrete_map={'Low': 'green', 'Moderate': 'yellow', 'High': 'red'},
                               title="Grant Compliance Rates")
                    fig.add_hline(y=95, line_dash="dash", line_color="red", 
                                annotation_text="Minimum Compliance Threshold")
                    st.plotly_chart(fig, use_container_width=True, key="cfo_grant_compliance_chart")
                    
                    # Risk matrix
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Spend category breakdown
                        st.subheader("Grant Spend Distribution")
                        if 'Permitted Spend Categories' in data.columns:
                            display_cols = ['Grant Program/Source', 'Permitted Spend Categories']
                            if 'Percent Used for Direct Instruction/Student' in data.columns:
                                display_cols.append('Percent Used for Direct Instruction/Student')
                            st.dataframe(data[display_cols], use_container_width=True)
                    
                    with col2:
                        # Compliance issues
                        st.subheader("Compliance Issues")
                        if 'Compliance Issues Flag' in data.columns:
                            issues = data[data['Compliance Issues Flag'] != 'None']
                            if not issues.empty:
                                display_cols = ['Grant Program/Source', 'Compliance Issues Flag']
                                if 'Issue Description/Status' in issues.columns:
                                    display_cols.append('Issue Description/Status')
                                if 'Corrective Actions (%)' in issues.columns:
                                    display_cols.append('Corrective Actions (%)')
                                st.dataframe(issues[display_cols], use_container_width=True)
                            else:
                                st.success("No active compliance issues")
                else:
                    st.warning("Grant compliance data not available or empty")
            except Exception as e:
                logger.error(f"Error displaying grant compliance: {e}")
                st.error(f"Error loading grant compliance data: {str(e)}")
    
    def display_metric_summary(self, persona: str):
        """Display a summary of all available metrics for a persona"""
        st.subheader(f"📋 Available {persona.upper()} Metrics")
        
        try:
            metrics = self.registry.get_available_metrics(persona)
            
            if metrics:
                # Create a summary dataframe
                summary_data = []
                for metric in metrics:
                    info = self.registry.get_metric_info(persona, metric)
                    summary_data.append({
                        'Metric': metric.replace('_', ' ').title(),
                        'Data Available': '✅' if info.get('data_path') else '❌',
                        'Module Ready': '✅' if info.get('module_path') else '❌',
                        'Script Available': '✅' if info.get('script_path') else '❌'
                    })
                
                summary_df = pd.DataFrame(summary_data)
                
                # Display metrics in a grid
                cols = st.columns(3)
                for idx, row in summary_df.iterrows():
                    col = cols[idx % 3]
                    with col:
                        status = "🟢" if row['Data Available'] == '✅' and row['Module Ready'] == '✅' else "🟡"
                        st.info(f"{status} **{row['Metric']}**")
            else:
                st.warning(f"No metrics found for {persona}")
        except Exception as e:
            logger.error(f"Error displaying metric summary: {e}")
            st.error(f"Error loading metric summary: {str(e)}")
    
    def create_dynamic_tabs(self, persona: str):
        """Create tabs dynamically based on available metrics"""
        try:
            available_metrics = self.registry.get_available_metrics(persona)
            
            if not available_metrics:
                st.warning(f"No metrics available for {persona}")
                return
            
            # Group metrics into logical categories
            tab_configs = {
                'cfo': {
                    'Financial Overview': ['cfo_budget_vs_actual', 'cfo_total_it_spend_breakdown'],
                    'Vendor Management': ['cfo_contract_expiration_alerts', 'cfo_vendor_spend_optimization'],
                    'Compliance': ['cfo_grant_compliance'],
                    'ROI & Performance': ['cfo_student_success_roi', 'cfo_hbcu_peer_benchmarking']
                },
                'cio': {
                    'Strategic Portfolio': ['digital_transformation_metrics', 'strategic_alignment_metrics'],
                    'Business Analysis': ['business_unit_it_spend', 'app_cost_analysis_metrics'],
                    'Risk & Vendor': ['risk_metrics', 'vendor_metrics']
                },
                'cto': {
                    'Infrastructure': ['infrastructure_performance_metrics', 'system_utilization_metrics'],
                    'Cloud & Assets': ['cloud_cost_optimization_metrics', 'asset_lifecycle_management_metrics'],
                    'Security & Tech Debt': ['security_metrics_and_response', 'technical_debt_metrics']
                }
            }
            
            tab_config = tab_configs.get(persona, {metric: [metric] for metric in available_metrics[:8]})
            
            # Filter tab config to only include available metrics
            filtered_tab_config = {}
            for tab_name, metrics in tab_config.items():
                available_in_tab = [m for m in metrics if m in available_metrics]
                if available_in_tab:
                    filtered_tab_config[tab_name] = available_in_tab
            
            if not filtered_tab_config:
                st.warning(f"No configured metrics found for {persona}")
                return
            
            # Create tabs
            tab_names = list(filtered_tab_config.keys())
            tabs = st.tabs(tab_names)
            
            # Display content in each tab
            for tab, tab_name in zip(tabs, tab_names):
                with tab:
                    st.header(tab_name)
                    
                    # Display metrics for this tab
                    for metric in filtered_tab_config[tab_name]:
                        # Call appropriate display function based on metric name
                        if metric == 'budget_vs_actual' and persona == 'cfo':
                            self.display_cfo_budget_variance(st.container())
                        elif metric == 'contract_expiration_alerts' and persona == 'cfo':
                            self.display_cfo_contract_alerts(st.container())
                        elif metric == 'grant_compliance' and persona == 'cfo':
                            self.display_cfo_grant_compliance(st.container())
                        else:
                            # Generic display for other metrics
                            self.display_generic_metric(persona, metric, st.container(), tab_name)
        except Exception as e:
            logger.error(f"Error creating dynamic tabs: {e}")
            st.error(f"Error loading dashboard tabs: {str(e)}")
    
    def display_generic_metric(self, persona: str, metric_name: str, container, tab_name: str = ""):
        """Generic metric display for metrics without specific handlers"""
        with container:
            # Add debug logging
            logger.info(f"Displaying metric: persona='{persona}', metric_name='{metric_name}', tab_name='{tab_name}'")
            st.subheader(f"📊 {metric_name.replace('_', ' ').title()}")
            
            try:
                # Try to load data
                data = self.registry.load_metric_data(persona, metric_name)
                
                if data is not None and not data.empty:
                    # Display summary stats
                    st.write(f"**Total Records:** {len(data):,}")
                    
                    # Display first few rows
                    with st.expander("View Sample Data", expanded=False):
                        st.dataframe(data.head(10), use_container_width=True)
                    
                    # Try to create a simple visualization
                    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
                    
                    if len(numeric_cols) >= 1:
                        # Create visualization options
                        viz_col1, viz_col2 = st.columns([2, 1])
                        
                        # Remove any persona prefix from metric_name if it exists
                        clean_metric_name = metric_name
                        if metric_name.startswith(f"{persona}_"):
                            clean_metric_name = metric_name[len(persona)+1:]
                            
                        # Create a unique key prefix including tab name
                        key_prefix = f"{persona}_{clean_metric_name}_{tab_name}" if tab_name else f"{persona}_{clean_metric_name}"
                        
                        with viz_col2:
                            chart_type = st.selectbox(
                                "Chart Type", 
                                ["Bar", "Line", "Scatter", "Box"],
                                key=f"{key_prefix}_chart_type"
                            )                        
                        with viz_col1:
                            if len(numeric_cols) >= 2 and chart_type in ["Scatter", "Line"]:
                                x_col = st.selectbox("X-axis", numeric_cols, key=f"{key_prefix}_x")
                                y_col = st.selectbox("Y-axis", [c for c in numeric_cols if c != x_col], key=f"{key_prefix}_y")
                                
                                if chart_type == "Scatter":
                                    fig = px.scatter(data, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
                                else:
                                    fig = px.line(data, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
                            else:
                                # For single numeric column or bar/box charts
                                col = st.selectbox("Select Column", numeric_cols, key=f"{key_prefix}_col")
                                
                                if chart_type == "Bar":
                                    fig = px.bar(data, y=col, title=f"Distribution of {col}")
                                elif chart_type == "Box":
                                    fig = px.box(data, y=col, title=f"Box Plot of {col}")
                                else:
                                    fig = px.line(data.reset_index(), x='index', y=col, title=f"Trend of {col}")
                            
                            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_chart_{chart_type}")
                    else:
                        st.info("No numeric columns available for visualization")
                        
                    # Show basic statistics
                    if numeric_cols:
                        with st.expander("View Statistics", expanded=False):
                            st.dataframe(data[numeric_cols].describe(), use_container_width=True)
                else:
                    st.info(f"No data available for {metric_name.replace('_', ' ').title()}")
            except Exception as e:
                logger.error(f"Error displaying generic metric {metric_name}: {e}")
                st.error(f"Error loading {metric_name}: {str(e)}")

# Create a singleton instance
dashboard_loader = DashboardMetricLoader()
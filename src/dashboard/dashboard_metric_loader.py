"""
Dashboard Metric Loader
Dynamically loads and displays metrics based on available modules
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from metric_registry import metric_registry, cfo_metrics, cio_metrics, cto_metrics

class DashboardMetricLoader:
    """Loads and displays metrics dynamically in Streamlit dashboard"""
    
    def __init__(self):
        self.registry = metric_registry
        self.cfo = cfo_metrics
        self.cio = cio_metrics
        self.cto = cto_metrics
    
    def display_cfo_budget_variance(self, tab):
        """Display CFO Budget Variance Analysis"""
        with tab:
            st.subheader("📊 Budget vs Actual Analysis with Variance Alerts")
            
            data, module = self.cfo.get_budget_variance_data()
            
            if data is not None:
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
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed table with alerts
                st.subheader("Detailed Budget Analysis")
                
                # Filter options
                col1, col2 = st.columns(2)
                with col1:
                    period_filter = st.multiselect("Filter by Period", 
                                                 options=data['Period'].unique(),
                                                 default=data['Period'].unique())
                with col2:
                    alert_filter = st.multiselect("Filter by Alert Status",
                                                options=data['Variance Alert'].unique(),
                                                default=data['Variance Alert'].unique())
                
                filtered_data = data[
                    (data['Period'].isin(period_filter)) & 
                    (data['Variance Alert'].isin(alert_filter))
                ]
                
                st.dataframe(
                    filtered_data.style.applymap(
                        lambda x: 'background-color: #ffcccc' if x == 'Overrun' else 
                                 'background-color: #ffffcc' if x == 'Warning' else '',
                        subset=['Variance Alert']
                    ),
                    use_container_width=True
                )
            else:
                st.warning("Budget variance data not available")
    
    def display_cfo_contract_alerts(self, tab):
        """Display CFO Contract Expiration Alerts"""
        with tab:
            st.subheader("🎯 Contract Expiration Alerts")
            
            data, module = self.cfo.get_contract_alerts()
            
            if data is not None:
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
                
                # Timeline visualization
                expiring_contracts = data[data['Days Until Expiry'] <= 180].copy()
                
                if not expiring_contracts.empty:
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
                    st.plotly_chart(fig, use_container_width=True)
                
                # Critical contracts table
                st.subheader("⚠️ Contracts Requiring Immediate Attention")
                critical_contracts = data[data['Alert Status'].isin(['Critical', 'Warning'])].sort_values('Days Until Expiry')
                
                if not critical_contracts.empty:
                    st.dataframe(
                        critical_contracts[['Vendor', 'System/Product', 'Contract End Date', 
                                          'Days Until Expiry', 'Annual Spend', 'Renewal Option', 
                                          'Negotiation Recommended']].style.applymap(
                            lambda x: 'color: red; font-weight: bold' if x == 'Yes' else '',
                            subset=['Negotiation Recommended']
                        ),
                        use_container_width=True
                    )
                else:
                    st.success("No contracts require immediate attention")
            else:
                st.warning("Contract data not available")
    
    def display_cfo_grant_compliance(self, tab):
        """Display CFO Grant Compliance Dashboard"""
        with tab:
            st.subheader("🏛️ Grant Compliance Dashboard")
            
            data, module = self.cfo.get_grant_compliance_data()
            
            if data is not None:
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
                st.plotly_chart(fig, use_container_width=True)
                
                # Risk matrix
                col1, col2 = st.columns(2)
                
                with col1:
                    # Spend category breakdown
                    st.subheader("Grant Spend Distribution")
                    if 'Permitted Spend Categories' in data.columns:
                        st.dataframe(data[['Grant Program/Source', 'Permitted Spend Categories', 
                                         'Percent Used for Direct Instruction/Student']],
                                   use_container_width=True)
                
                with col2:
                    # Compliance issues
                    st.subheader("Compliance Issues")
                    issues = data[data['Compliance Issues Flag'] != 'None']
                    if not issues.empty:
                        st.dataframe(issues[['Grant Program/Source', 'Compliance Issues Flag', 
                                           'Issue Description/Status', 'Corrective Actions (%)']],
                                   use_container_width=True)
                    else:
                        st.success("No active compliance issues")
            else:
                st.warning("Grant compliance data not available")
    
    def display_metric_summary(self, persona):
        """Display a summary of all available metrics for a persona"""
        st.subheader(f"📋 Available {persona.upper()} Metrics")
        
        metrics = self.registry.get_available_metrics(persona)
        
        if metrics:
            # Create a summary dataframe
            summary_data = []
            for metric in metrics:
                info = self.registry.get_metric_info(persona, metric)
                summary_data.append({
                    'Metric': metric.replace('_', ' ').title(),
                    'Data Available': '✅' if info['data_path'] else '❌',
                    'Module Ready': '✅' if info['module_path'] else '❌',
                    'Script Available': '✅' if info['script_path'] else '❌'
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
    
    def create_dynamic_tabs(self, persona):
        """Create tabs dynamically based on available metrics"""
        available_metrics = self.registry.get_available_metrics(persona)
        
        if not available_metrics:
            st.warning(f"No metrics available for {persona}")
            return
        
        # Group metrics into logical categories
        if persona == 'cfo':
            tab_config = {
                'Financial Overview': ['budget_vs_actual', 'total_it_spend_breakdown'],
                'Vendor Management': ['contract_expiration_alerts', 'vendor_spend_optimization'],
                'Compliance': ['grant_compliance'],
                'ROI & Performance': ['student_success_roi', 'hbcu_peer_benchmarking']
            }
        elif persona == 'cio':
            tab_config = {
                'Strategic Portfolio': ['digital_transformation_metrics', 'strategic_alignment_metrics'],
                'Business Analysis': ['business_unit_it_spend', 'app_cost_analysis_metrics'],
                'Risk & Vendor': ['risk_metrics', 'vendor_metrics']
            }
        elif persona == 'cto':
            tab_config = {
                'Infrastructure': ['infrastructure_performance_metrics', 'system_utilization_metrics'],
                'Cloud & Assets': ['cloud_cost_optimization_metrics', 'asset_lifecycle_management_metrics'],
                'Security & Tech Debt': ['security_metrics_and_response', 'technical_debt_metrics']
            }
        else:
            # Default: one tab per metric
            tab_config = {metric: [metric] for metric in available_metrics[:8]}  # Limit to 8 tabs
        
        # Create tabs
        tab_names = list(tab_config.keys())
        tabs = st.tabs(tab_names)
        
        # Display content in each tab
        for tab, tab_name in zip(tabs, tab_names):
            with tab:
                st.header(tab_name)
                
                # Display metrics for this tab
                for metric in tab_config[tab_name]:
                    if metric in available_metrics:
                        # Call appropriate display function based on metric name
                        if metric == 'budget_vs_actual' and persona == 'cfo':
                            self.display_cfo_budget_variance(st.container())
                        elif metric == 'contract_expiration_alerts' and persona == 'cfo':
                            self.display_cfo_contract_alerts(st.container())
                        elif metric == 'grant_compliance' and persona == 'cfo':
                            self.display_cfo_grant_compliance(st.container())
                        else:
                            # Generic display for other metrics
                            self.display_generic_metric(persona, metric, st.container())
    
    def display_generic_metric(self, persona, metric_name, container):
        """Generic metric display for metrics without specific handlers"""
        with container:
            st.subheader(f"📊 {metric_name.replace('_', ' ').title()}")
            
            # Try to load data
            data = self.registry.load_metric_data(persona, metric_name)
            
            if data is not None:
                # Display first few rows
                st.write(f"Sample data ({len(data)} records):")
                st.dataframe(data.head(), use_container_width=True)
                
                # Try to create a simple visualization
                numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
                if len(numeric_cols) >= 2:
                    fig = px.scatter(data, x=numeric_cols[0], y=numeric_cols[1], 
                                   title=f"{numeric_cols[0]} vs {numeric_cols[1]}")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"No data available for {metric_name}")

# Create a singleton instance
dashboard_loader = DashboardMetricLoader()
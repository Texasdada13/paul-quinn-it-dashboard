"""
CTO Metrics Display Functions
These functions read the generated CSV files and display Technology Operator metrics in the dashboard
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import numpy as np
from plotly.subplots import make_subplots
import uuid


# Get the directory where this file is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_csv_safe(filename):
    """Safely load a CSV file from the CTO metrics directory"""
    filepath = os.path.join(CURRENT_DIR, filename)
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        return None

# ============================================
# ASSET LIFECYCLE MANAGEMENT METRICS
# ============================================
def display_asset_lifecycle_management_metrics():
    """Display Asset Lifecycle Management metrics"""
    
    # Generate a unique key prefix for this function call
    key_prefix = f"asset_lifecycle_{uuid.uuid4().hex[:8]}"
     
    df = load_csv_safe('asset_lifecycle_management_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for Asset Lifecycle Management Metrics")
        return
    
    # Convert date column to datetime if it exists
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'total_assets' in df.columns:
            total_assets = df['total_assets'].iloc[-1] if not df.empty else 0
            st.metric("Total Assets", f"{total_assets:,}")
        else:
            st.metric("Total Assets", "N/A")
    
    with col2:
        if 'end_of_life_next_12_months' in df.columns:
            eol_assets = df['end_of_life_next_12_months'].iloc[-1] if not df.empty else 0
            st.metric("EOL Next 12 Months", f"{eol_assets:,}")
        else:
            st.metric("EOL Assets", "N/A")
    
    with col3:
        if 'refresh_budget_utilization' in df.columns:
            budget_util = df['refresh_budget_utilization'].iloc[-1] if not df.empty else 0
            st.metric("Budget Utilization", f"{budget_util:.1f}%")
        else:
            st.metric("Budget Utilization", "N/A")
    
    with col4:
        if 'maintenance_cost_trend' in df.columns:
            maintenance_trend = df['maintenance_cost_trend'].iloc[-1] if not df.empty else 0
            st.metric("Maintenance Cost Trend", f"${maintenance_trend:,.0f}")
        else:
            st.metric("Maintenance Cost", "N/A")
    
    # Create visualizations
    tab1, tab2, tab3 = st.tabs(["Asset Age Distribution", "Lifecycle Status", "Cost Analysis"])
    
    with tab1:
        if 'asset_age_years' in df.columns and 'asset_type' in df.columns:
            fig = px.histogram(df, x='asset_age_years', color='asset_type',
                             title="Asset Age Distribution by Type",
                             labels={'asset_age_years': 'Asset Age (Years)', 'count': 'Number of Assets'})
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_age_dist")
        else:
            st.info("Asset age data not available")
    
    with tab2:
        if 'lifecycle_stage' in df.columns:
            lifecycle_counts = df['lifecycle_stage'].value_counts()
            fig = px.pie(values=lifecycle_counts.values, names=lifecycle_counts.index,
                        title="Assets by Lifecycle Stage")
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_lifecycle")
        else:
            st.info("Lifecycle stage data not available")
    
    with tab3:
        if 'annual_maintenance_cost' in df.columns and 'asset_type' in df.columns:
            cost_by_type = df.groupby('asset_type')['annual_maintenance_cost'].sum().sort_values(ascending=True)
            fig = px.bar(x=cost_by_type.values, y=cost_by_type.index, orientation='h',
                        title="Annual Maintenance Cost by Asset Type",
                        labels={'x': 'Annual Cost ($)', 'y': 'Asset Type'})
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_cost")
        else:
            st.info("Maintenance cost data not available")

# ============================================
# CAPACITY PLANNING METRICS
# ============================================
def display_capacity_planning_metrics():
    """Display Capacity Planning metrics"""
    
    # Generate unique key prefix
    key_prefix = f"capacity_{uuid.uuid4().hex[:8]}" 
    
    df = load_csv_safe('capacity_planning_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for Capacity Planning Metrics")
        return
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'current_utilization_pct' in df.columns:
            current_util = df['current_utilization_pct'].mean()
            st.metric("Avg Utilization", f"{current_util:.1f}%")
        else:
            st.metric("Avg Utilization", "N/A")
    
    with col2:
        if 'predicted_capacity_needed' in df.columns:
            capacity_need = df['predicted_capacity_needed'].iloc[-1] if not df.empty else 0
            st.metric("Predicted Capacity Need", f"{capacity_need:.1f}")
        else:
            st.metric("Capacity Need", "N/A")
    
    with col3:
        if 'cost_optimization_opportunity' in df.columns:
            optimization = df['cost_optimization_opportunity'].sum()
            st.metric("Cost Optimization", f"${optimization:,.0f}")
        else:
            st.metric("Cost Optimization", "N/A")
    
    with col4:
        if 'time_to_capacity_limit_days' in df.columns:
            time_to_limit = df['time_to_capacity_limit_days'].min()
            st.metric("Days to Capacity Limit", f"{time_to_limit:.0f}")
        else:
            st.metric("Days to Limit", "N/A")
    
    # Visualizations
    tab1, tab2, tab3 = st.tabs(["Utilization Trends", "Capacity Forecast", "Resource Distribution"])
    
    with tab1:
        if 'date' in df.columns and 'current_utilization_pct' in df.columns:
            fig = px.line(df, x='date', y='current_utilization_pct',
                         title="Resource Utilization Over Time",
                         labels={'current_utilization_pct': 'Utilization %', 'date': 'Date'})
            fig.add_hline(y=80, line_dash="dash", line_color="orange", 
                         annotation_text="Optimal Threshold (80%)")
            fig.add_hline(y=95, line_dash="dash", line_color="red", 
                         annotation_text="Critical Threshold (95%)")
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_utilization")
        else:
            st.info("Utilization trend data not available")
    
    with tab2:
        if 'predicted_capacity_needed' in df.columns and 'current_capacity' in df.columns:
            latest = df.tail(10)  # Show last 10 data points
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=latest.index, y=latest['current_capacity'], 
                                   name='Current Capacity', mode='lines+markers'))
            fig.add_trace(go.Scatter(x=latest.index, y=latest['predicted_capacity_needed'], 
                                   name='Predicted Need', mode='lines+markers'))
            fig.update_layout(title="Capacity vs Predicted Need", 
                            xaxis_title="Time Period", yaxis_title="Capacity Units")
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_forecast")
        else:
            st.info("Capacity forecast data not available")
    
    with tab3:
        if 'resource_type' in df.columns and 'current_utilization_pct' in df.columns:
            resource_util = df.groupby('resource_type')['current_utilization_pct'].mean().sort_values(ascending=False)
            fig = px.bar(resource_util, title="Average Utilization by Resource Type",
                        labels={'value': 'Utilization %', 'index': 'Resource Type'})
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_resource_dist")
        else:
            st.info("Resource distribution data not available")

# ============================================
# CLOUD COST OPTIMIZATION METRICS
# ============================================
def display_cloud_cost_optimization_metrics():
    """Display Cloud Cost Optimization metrics"""
    
    # Generate unique key prefix
    key_prefix = f"cloud_cost_{uuid.uuid4().hex[:8]}"
    
    df = load_csv_safe('cloud_cost_optimization_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for Cloud Cost Optimization Metrics")
        return
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Cloud Cost KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'monthly_cloud_spend' in df.columns:
            monthly_spend = df['monthly_cloud_spend'].iloc[-1] if not df.empty else 0
            st.metric("Monthly Cloud Spend", f"${monthly_spend:,.0f}")
        else:
            st.metric("Monthly Spend", "N/A")
    
    with col2:
        if 'cost_optimization_savings' in df.columns:
            savings = df['cost_optimization_savings'].sum()
            st.metric("Total Savings", f"${savings:,.0f}")
        else:
            st.metric("Total Savings", "N/A")
    
    with col3:
        if 'resource_utilization_pct' in df.columns:
            avg_util = df['resource_utilization_pct'].mean()
            st.metric("Resource Utilization", f"{avg_util:.1f}%")
        else:
            st.metric("Resource Utilization", "N/A")
    
    with col4:
        if 'wasted_spend_identified' in df.columns:
            waste = df['wasted_spend_identified'].sum()
            st.metric("Waste Identified", f"${waste:,.0f}")
        else:
            st.metric("Waste Identified", "N/A")
    
    # Cloud optimization visualizations
    tab1, tab2, tab3 = st.tabs(["Spend by Service", "Optimization Opportunities", "Usage Patterns"])
    
    with tab1:
        if 'cloud_service' in df.columns and 'monthly_cloud_spend' in df.columns:
            service_spend = df.groupby('cloud_service')['monthly_cloud_spend'].sum().sort_values(ascending=True).tail(10)
            fig = px.bar(x=service_spend.values, y=service_spend.index, orientation='h',
                        title="Top 10 Cloud Services by Monthly Spend",
                        labels={'x': 'Monthly Spend ($)', 'y': 'Cloud Service'})
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_service_spend")
        else:
            st.info("Service spend data not available")
    
    with tab2:
        if 'optimization_opportunity' in df.columns and 'potential_savings' in df.columns:
            fig = px.scatter(df, x='potential_savings', y='optimization_opportunity',
                           size='monthly_cloud_spend', hover_data=['cloud_service'],
                           title="Optimization Opportunities vs Potential Savings",
                           labels={'potential_savings': 'Potential Savings ($)', 
                                  'optimization_opportunity': 'Optimization Score'})
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_opportunities")
        else:
            st.info("Optimization opportunity data not available")
    
    with tab3:
        if 'date' in df.columns and 'resource_utilization_pct' in df.columns:
            fig = px.line(df, x='date', y='resource_utilization_pct',
                         color='cloud_service' if 'cloud_service' in df.columns else None,
                         title="Resource Utilization Trends by Service")
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_usage_patterns")
        else:
            st.info("Usage pattern data not available")

# ============================================
def display_infrastructure_performance_metrics():
    """Display Infrastructure Performance metrics with comprehensive analysis"""
    
    # Generate unique key prefix
    key_prefix = f"infra_perf_{uuid.uuid4().hex[:8]}"
    
    df = load_csv_safe('infrastructure_performance_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for Infrastructure Performance Metrics")
        return
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Infrastructure performance KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'system_uptime_pct' in df.columns:
            uptime = df['system_uptime_pct'].mean()
            st.metric("System Uptime", f"{uptime:.2f}%")
        else:
            st.metric("System Uptime", "N/A")
    
    with col2:
        if 'response_time_ms' in df.columns:
            response_time = df['response_time_ms'].mean()
            st.metric("Avg Response Time", f"{response_time:.0f}ms")
        else:
            st.metric("Response Time", "N/A")
    
    with col3:
        if 'incidents_resolved' in df.columns:
            incidents = df['incidents_resolved'].sum()
            st.metric("Incidents Resolved", incidents)
        else:
            st.metric("Incidents Resolved", "N/A")
    
    with col4:
        if 'performance_score' in df.columns:
            perf_score = df['performance_score'].mean()
            st.metric("Performance Score", f"{perf_score:.1f}/10")
        else:
            st.metric("Performance Score", "N/A")
    
    # Enhanced Performance visualizations with comprehensive tabs
    tab1, tab2, tab3 = st.tabs(["System Utilization", "Performance Analysis", "Incident Analysis"])
    
    # System Utilization Tab (Enhanced)
    with tab1:
        st.subheader("Resource Utilization Analysis")
        if all(col in df.columns for col in ['cpu_utilization_pct', 'memory_utilization_pct', 'storage_utilization_pct', 'network_utilization_pct']):
            
            # Create subtabs for different utilization views
            util_tabs = st.tabs(["Trend Analysis", "Current Status", "Resource Balance", "Heat Map", "Utilization Matrix"])
            
            util_metrics = ['cpu_utilization_pct', 'memory_utilization_pct', 'storage_utilization_pct', 'network_utilization_pct']
            metric_names = ['CPU', 'Memory', 'Storage', 'Network']
            colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
            
            # Trend Analysis Tab
            with util_tabs[0]:
                if 'date' in df.columns:
                    daily_util = df.groupby('date')[util_metrics].mean().reset_index()
                    
                    fig = go.Figure()
                    
                    for i, (metric, name) in enumerate(zip(util_metrics, metric_names)):
                        fig.add_trace(go.Scatter(
                            x=daily_util['date'],
                            y=daily_util[metric],
                            mode='lines+markers',
                            name=name,
                            line=dict(color=colors[i], width=3),
                            marker=dict(size=6),
                            hovertemplate=f'<b>{name}</b><br>%{{y:.1f}}%<br>%{{x}}<extra></extra>'
                        ))
                    
                    fig.add_hline(y=80, line_dash="dash", line_color="orange", line_width=2,
                                 annotation_text="Optimal Threshold (80%)")
                    fig.add_hline(y=95, line_dash="dash", line_color="red", line_width=2,
                                 annotation_text="Critical Threshold (95%)")
                    
                    fig.update_layout(
                        title="Resource Utilization Trends Over Time",
                        xaxis_title="Date",
                        yaxis_title="Utilization %",
                        height=400,
                        hovermode='x unified'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_util_trends")
            
            # Current Status Tab
            with util_tabs[1]:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Radar chart for current utilization
                    current_util = df[util_metrics].mean()
                    
                    fig_radar = go.Figure()
                    
                    fig_radar.add_trace(go.Scatterpolar(
                        r=current_util.values,
                        theta=metric_names,
                        fill='toself',
                        fillcolor='rgba(46, 134, 171, 0.3)',
                        line_color='#2E86AB',
                        line_width=3,
                        marker_size=8,
                        name='Current Utilization'
                    ))
                    
                    fig_radar.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 100],
                                tickvals=[20, 40, 60, 80, 100]
                            )
                        ),
                        title="Current Resource Utilization",
                        height=350
                    )
                    
                    st.plotly_chart(fig_radar, use_container_width=True, key=f"{key_prefix}_radar")
                
                with col2:
                    st.write("**Utilization Status:**")
                    
                    for metric, name in zip(util_metrics, metric_names):
                        avg_util = df[metric].mean()
                        
                        if avg_util > 95:
                            status_icon = "🔴"
                            status_text = "Critical"
                        elif avg_util > 80:
                            status_icon = "🟡"
                            status_text = "Warning"
                        else:
                            status_icon = "🟢"
                            status_text = "Normal"
                        
                        st.metric(
                            label=f"{status_icon} {name}",
                            value=f"{avg_util:.1f}%",
                            delta=status_text
                        )
            
            # Resource Balance Tab
            with util_tabs[2]:
                current_util = df[util_metrics].mean()
                
                # Create a balanced scorecard
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=metric_names,
                    y=current_util.values,
                    marker_color=[colors[i] if current_util.values[i] <= 80 else '#E94B3C' for i in range(len(metric_names))],
                    text=[f'{util:.1f}%' for util in current_util.values],
                    textposition='outside'
                ))
                
                fig.add_hline(y=80, line_dash="dash", line_color="orange", 
                             annotation_text="Optimal Threshold")
                fig.add_hline(y=95, line_dash="dash", line_color="red", 
                             annotation_text="Critical Threshold")
                
                fig.update_layout(
                    title="Resource Utilization Balance",
                    xaxis_title="Resource Type",
                    yaxis_title="Current Utilization %",
                    yaxis_range=[0, 100],
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_balance")
                
                # Resource recommendations
                st.subheader("Optimization Recommendations")
                for i, (metric, name) in enumerate(zip(util_metrics, metric_names)):
                    util_val = current_util.values[i]
                    if util_val > 90:
                        st.error(f"**{name}**: Critical utilization ({util_val:.1f}%) - Immediate scaling required")
                    elif util_val > 80:
                        st.warning(f"**{name}**: High utilization ({util_val:.1f}%) - Consider scaling soon")
                    elif util_val < 30:
                        st.info(f"**{name}**: Low utilization ({util_val:.1f}%) - Potential cost optimization opportunity")
            
            # Heat Map Tab
            with util_tabs[3]:
                if 'system_name' in df.columns:
                    # Create utilization heatmap by system
                    heatmap_data = df.groupby('system_name')[util_metrics].mean()
                    
                    fig = go.Figure(data=go.Heatmap(
                        z=heatmap_data.values,
                        x=metric_names,
                        y=heatmap_data.index,
                        colorscale='RdYlGn_r',
                        zmid=50,
                        colorbar=dict(title="Utilization %"),
                        hovertemplate='<b>%{y}</b><br>%{x}: %{z:.1f}%<extra></extra>'
                    ))
                    
                    fig.update_layout(
                        title="System Resource Utilization Heat Map",
                        xaxis_title="Resource Type",
                        yaxis_title="System",
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_heatmap")
            
            # Utilization Matrix Tab
            with util_tabs[4]:
                # CPU vs Memory utilization matrix
                if 'system_name' in df.columns:
                    matrix_data = df.groupby('system_name')[['cpu_utilization_pct', 'memory_utilization_pct', 'storage_utilization_pct']].mean().reset_index()
                    
                    fig = px.scatter(
                        matrix_data,
                        x='cpu_utilization_pct',
                        y='memory_utilization_pct',
                        size='storage_utilization_pct',
                        hover_name='system_name',
                        title='CPU vs Memory Utilization (Size = Storage Utilization)',
                        labels={
                            'cpu_utilization_pct': 'CPU Utilization %',
                            'memory_utilization_pct': 'Memory Utilization %'
                        }
                    )
                    
                    # Add quadrant lines
                    fig.add_hline(y=80, line_dash="dash", line_color="gray", opacity=0.5)
                    fig.add_vline(x=80, line_dash="dash", line_color="gray", opacity=0.5)
                    
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_util_matrix")
        
        else:
            st.info("Resource utilization data not available")
    
    # Performance Analysis Tab (Enhanced)
    with tab2:
        if 'date' in df.columns and 'response_time_ms' in df.columns:
            # Create subtabs for different performance analysis views
            perf_tabs = st.tabs(["Trend Analysis", "System Breakdown", "Real-time Status", "Performance Matrix"])
            
            # Trend Analysis Tab
            with perf_tabs[0]:
                st.subheader("Response Time Trend Analysis")
                
                # Daily aggregated trends
                daily_avg = df.groupby('date')['response_time_ms'].agg(['mean', 'max', 'min']).reset_index()
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=daily_avg['date'],
                    y=daily_avg['mean'],
                    mode='lines',
                    name='Average Response Time',
                    line=dict(color='#2E86AB', width=3),
                    hovertemplate='<b>%{y:.0f}ms</b><br>%{x}<extra></extra>'
                ))
                
                fig.add_trace(go.Scatter(
                    x=daily_avg['date'],
                    y=daily_avg['max'],
                    fill=None,
                    mode='lines',
                    line_color='rgba(46, 134, 171, 0)',
                    showlegend=False
                ))
                
                fig.add_trace(go.Scatter(
                    x=daily_avg['date'],
                    y=daily_avg['min'],
                    fill='tonexty',
                    mode='lines',
                    line_color='rgba(46, 134, 171, 0)',
                    fillcolor='rgba(46, 134, 171, 0.2)',
                    name='Min-Max Range'
                ))
                
                fig.add_hline(y=500, line_dash="dash", line_color="orange", line_width=2,
                             annotation_text="Performance Threshold (500ms)")
                fig.add_hline(y=1000, line_dash="dash", line_color="red", line_width=2,
                             annotation_text="Critical Threshold (1000ms)")
                
                fig.update_layout(
                    title="Daily Response Time Trends with Performance Envelopes",
                    xaxis_title="Date",
                    yaxis_title="Response Time (ms)",
                    hovermode='x unified',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_trend_analysis")
            
            # System Breakdown Tab
            with perf_tabs[1]:
                st.subheader("System Performance Breakdown")
                
                if 'system_name' in df.columns:
                    system_performance = df.groupby('system_name')['response_time_ms'].agg(['mean', 'count', 'std']).reset_index()
                    system_performance = system_performance[system_performance['count'] >= 5]
                    system_performance = system_performance.sort_values('mean', ascending=False).head(10)
                    
                    colors = ['#E94B3C' if x > 500 else '#4A90E2' for x in system_performance['mean']]
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        x=system_performance['mean'],
                        y=system_performance['system_name'],
                        orientation='h',
                        marker_color=colors,
                        text=[f'{x:.0f}ms' for x in system_performance['mean']],
                        textposition='outside',
                        error_x=dict(type='data', array=system_performance['std'], visible=True),
                        hovertemplate='<b>%{y}</b><br>Avg: %{x:.0f}ms<br>Std Dev: %{error_x:.0f}ms<extra></extra>'
                    ))
                    
                    fig.add_vline(x=500, line_dash="dash", line_color="orange", annotation_text="Target")
                    
                    fig.update_layout(
                        title="Top 10 Systems by Response Time (with Standard Deviation)",
                        xaxis_title="Average Response Time (ms)",
                        yaxis_title="System",
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_system_breakdown")
                else:
                    st.info("System name data not available for breakdown")
            
            # Real-time Status Tab
            with perf_tabs[2]:
                st.subheader("Current Performance Status")
                
                latest_data = df[df['date'] == df['date'].max()]
                
                # Performance gauge
                current_avg = latest_data['response_time_ms'].mean()
                
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=current_avg,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Current Avg Response Time (ms)"},
                    delta={'reference': 500, 'suffix': " vs Target"},
                    gauge={
                        'axis': {'range': [None, 1500]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 500], 'color': "lightgreen"},
                            {'range': [500, 1000], 'color': "yellow"},
                            {'range': [1000, 1500], 'color': "lightcoral"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 1000
                        }
                    }
                ))
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_gauge")
                
                # System status indicators
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Systems by Performance Status:**")
                    good_systems = len(latest_data[latest_data['response_time_ms'] <= 500])
                    warning_systems = len(latest_data[(latest_data['response_time_ms'] > 500) & (latest_data['response_time_ms'] <= 1000)])
                    critical_systems = len(latest_data[latest_data['response_time_ms'] > 1000])
                    
                    st.metric("Good Performance", good_systems, delta="≤500ms")
                    st.metric("Warning", warning_systems, delta="500-1000ms", delta_color="inverse")
                    st.metric("Critical", critical_systems, delta=">1000ms", delta_color="inverse")
                
                with col2:
                    # Latest incidents
                    if 'incidents_resolved' in latest_data.columns:
                        st.write("**Recent Activity:**")
                        total_incidents = latest_data['incidents_resolved'].sum()
                        st.metric("Recent Incidents Resolved", int(total_incidents))
            
            # Performance Matrix Tab
            with perf_tabs[3]:
                st.subheader("Performance vs Utilization Matrix")
                
                if 'system_uptime_pct' in df.columns and 'system_name' in df.columns:
                    matrix_data = df.groupby('system_name').agg({
                        'response_time_ms': 'mean',
                        'system_uptime_pct': 'mean',
                        'incidents_resolved': 'sum'
                    }).reset_index()
                    
                    fig = px.scatter(
                        matrix_data,
                        x='response_time_ms',
                        y='system_uptime_pct',
                        size='incidents_resolved',
                        hover_name='system_name',
                        title='System Performance Matrix',
                        labels={
                            'response_time_ms': 'Avg Response Time (ms)',
                            'system_uptime_pct': 'Uptime %',
                            'incidents_resolved': 'Incidents Resolved'
                        }
                    )
                    
                    # Add quadrant lines
                    fig.add_hline(y=99, line_dash="dash", line_color="gray", opacity=0.5)
                    fig.add_vline(x=500, line_dash="dash", line_color="gray", opacity=0.5)
                    
                    # Add quadrant labels
                    fig.add_annotation(x=250, y=99.5, text="High Uptime<br>Fast Response ✓", 
                                     bgcolor="rgba(144,238,144,0.3)", showarrow=False)
                    fig.add_annotation(x=750, y=99.5, text="High Uptime<br>Slow Response ⚠", 
                                     bgcolor="rgba(255,255,0,0.3)", showarrow=False)
                    fig.add_annotation(x=250, y=98.5, text="Low Uptime<br>Fast Response ⚠", 
                                     bgcolor="rgba(255,255,0,0.3)", showarrow=False)
                    fig.add_annotation(x=750, y=98.5, text="Low Uptime<br>Slow Response ✗", 
                                     bgcolor="rgba(255,182,193,0.3)", showarrow=False)
                    
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_matrix")
                else:
                    st.info("Performance matrix data not available")
        else:
            st.info("Performance trend data not available")
    
    # Incident Analysis Tab (Enhanced)
    with tab3:
        if 'incident_severity' in df.columns:
            incident_counts = df['incident_severity'].value_counts()
            fig = px.pie(values=incident_counts.values, names=incident_counts.index,
                        title="Incidents by Severity Level")
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_incidents")
        else:
            st.info("Incident analysis data not available")
# ============================================
# SECURITY METRICS
# ============================================
def display_security_metrics():
    """Display Security metrics"""
    
    # Generate unique key prefix
    key_prefix = f"security_{uuid.uuid4().hex[:8]}"
    
    df = load_csv_safe('security_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for Security Metrics")
        return
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Security KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'security_incidents' in df.columns:
            incidents = df['security_incidents'].sum()
            st.metric("Security Incidents", incidents)
        else:
            st.metric("Security Incidents", "N/A")
    
    with col2:
        if 'vulnerability_score' in df.columns:
            vuln_score = df['vulnerability_score'].mean()
            st.metric("Vulnerability Score", f"{vuln_score:.1f}/10")
        else:
            st.metric("Vulnerability Score", "N/A")
    
    with col3:
        if 'compliance_score' in df.columns:
            compliance = df['compliance_score'].mean()
            st.metric("Compliance Score", f"{compliance:.1f}%")
        else:
            st.metric("Compliance Score", "N/A")
    
    with col4:
        if 'security_training_completion' in df.columns:
            training = df['security_training_completion'].mean()
            st.metric("Training Completion", f"{training:.1f}%")
        else:
            st.metric("Training Completion", "N/A")
    
    # Security visualizations
    tab1, tab2 = st.tabs(["Security Dashboard", "Compliance Trends"])
    
    with tab1:
        if 'threat_level' in df.columns:
            threat_counts = df['threat_level'].value_counts()
            fig = px.pie(values=threat_counts.values, names=threat_counts.index,
                        title="Threats by Severity Level",
                        color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'green'})
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_threats")
        else:
            st.info("Threat level data not available")
    
    with tab2:
        if 'date' in df.columns and 'compliance_score' in df.columns:
            fig = px.line(df, x='date', y='compliance_score',
                         title="Compliance Score Trends",
                         labels={'compliance_score': 'Compliance %', 'date': 'Date'})
            fig.add_hline(y=95, line_dash="dash", line_color="green", 
                         annotation_text="Target (95%)")
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_compliance")
        else:
            st.info("Compliance trend data not available")

# ============================================
# SYSTEM UTILIZATION METRICS
# ============================================
def display_system_utilization_metrics():
    """Display System Utilization metrics"""
    
    # Generate unique key prefix
    key_prefix = f"system_util_{uuid.uuid4().hex[:8]}"
    
    df = load_csv_safe('system_utilization_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for System Utilization Metrics")
        return
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # System utilization KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'cpu_utilization_pct' in df.columns:
            cpu_util = df['cpu_utilization_pct'].mean()
            st.metric("CPU Utilization", f"{cpu_util:.1f}%")
        else:
            st.metric("CPU Utilization", "N/A")
    
    with col2:
        if 'memory_utilization_pct' in df.columns:
            memory_util = df['memory_utilization_pct'].mean()
            st.metric("Memory Utilization", f"{memory_util:.1f}%")
        else:
            st.metric("Memory Utilization", "N/A")
    
    with col3:
        if 'storage_utilization_pct' in df.columns:
            storage_util = df['storage_utilization_pct'].mean()
            st.metric("Storage Utilization", f"{storage_util:.1f}%")
        else:
            st.metric("Storage Utilization", "N/A")
    
    with col4:
        if 'network_utilization_pct' in df.columns:
            network_util = df['network_utilization_pct'].mean()
            st.metric("Network Utilization", f"{network_util:.1f}%")
        else:
            st.metric("Network Utilization", "N/A")
    
    # System utilization visualizations
    tab1, tab2 = st.tabs(["Resource Utilization", "System Performance"])
    
    with tab1:
        if all(col in df.columns for col in ['cpu_utilization_pct', 'memory_utilization_pct', 'storage_utilization_pct']):
            util_metrics = ['cpu_utilization_pct', 'memory_utilization_pct', 'storage_utilization_pct']
            if 'date' in df.columns:
                fig = px.line(df, x='date', y=util_metrics,
                             title="Resource Utilization Over Time",
                             labels={'value': 'Utilization %', 'variable': 'Resource Type'})
            else:
                latest_util = df[util_metrics].mean()
                fig = px.bar(x=latest_util.index, y=latest_util.values,
                            title="Average Resource Utilization",
                            labels={'x': 'Resource Type', 'y': 'Utilization %'})
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_utilization")
        else:
            st.info("Resource utilization data not available")
    
    with tab2:
        if 'system_name' in df.columns and 'performance_score' in df.columns:
            system_perf = df.groupby('system_name')['performance_score'].mean().sort_values(ascending=False)
            fig = px.bar(system_perf, title="System Performance Scores",
                        labels={'value': 'Performance Score', 'index': 'System'})
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_performance")
        else:
            st.info("System performance data not available")

# ============================================
# TECHNICAL DEBT METRICS
# ============================================
def display_technical_debt_metrics():
    """Display Technical Debt metrics"""
    
    # Generate unique key prefix
    key_prefix = f"tech_debt_{uuid.uuid4().hex[:8]}"
    
    df = load_csv_safe('technical_debt_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for Technical Debt Metrics")
        return
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Technical debt KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'technical_debt_score' in df.columns:
            debt_score = df['technical_debt_score'].mean()
            st.metric("Technical Debt Score", f"{debt_score:.1f}/10")
        else:
            st.metric("Technical Debt Score", "N/A")
    
    with col2:
        if 'legacy_systems_count' in df.columns:
            legacy_count = df['legacy_systems_count'].iloc[-1] if not df.empty else 0
            st.metric("Legacy Systems", f"{legacy_count:,}")
        else:
            st.metric("Legacy Systems", "N/A")
    
    with col3:
        if 'maintenance_cost_annual' in df.columns:
            maintenance_cost = df['maintenance_cost_annual'].sum()
            st.metric("Annual Maintenance Cost", f"${maintenance_cost:,.0f}")
        else:
            st.metric("Maintenance Cost", "N/A")
    
    with col4:
        if 'modernization_priority' in df.columns:
            high_priority = len(df[df['modernization_priority'] == 'High'])
            st.metric("High Priority Items", high_priority)
        else:
            st.metric("High Priority Items", "N/A")
    
    # Technical debt visualizations
    tab1, tab2 = st.tabs(["Debt by System", "Modernization Pipeline"])
    
    with tab1:
        if 'system_name' in df.columns and 'technical_debt_score' in df.columns:
            debt_by_system = df.groupby('system_name')['technical_debt_score'].mean().sort_values(ascending=False).head(10)
            fig = px.bar(debt_by_system, title="Technical Debt by System (Top 10)",
                        labels={'value': 'Debt Score', 'index': 'System'},
                        color=debt_by_system.values, color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_debt_by_system")
        else:
            st.info("System debt data not available")
    
    with tab2:
        if 'modernization_priority' in df.columns:
            priority_counts = df['modernization_priority'].value_counts()
            fig = px.pie(values=priority_counts.values, names=priority_counts.index,
                        title="Modernization Pipeline by Priority",
                        color_discrete_map={'High': '#FF4444', 'Medium': '#FFA500', 'Low': '#4CAF50'})
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_modernization")
        else:
            st.info("Modernization priority data not available")

# ============================================
# MAIN REGISTRY FOR CTO METRICS
# ============================================
# This dictionary maps metric names to their display functions
CTO_METRICS = {
    'asset_lifecycle_management_metrics': display_asset_lifecycle_management_metrics,
    'capacity_planning_metrics': display_capacity_planning_metrics,
    'cloud_cost_optimization_metrics': display_cloud_cost_optimization_metrics,
    'infrastructure_performance_metrics': display_infrastructure_performance_metrics,
    'security_metrics': display_security_metrics,
    'system_utilization_metrics': display_system_utilization_metrics,
    'technical_debt_metrics': display_technical_debt_metrics,
}

def get_available_metrics():
    """Return list of available CTO metrics"""
    return list(CTO_METRICS.keys())

def display_metric(metric_name):
    """Display a specific metric by name"""
    if metric_name in CTO_METRICS:
        CTO_METRICS[metric_name]()
    else:
        st.error(f"Metric '{metric_name}' not found")
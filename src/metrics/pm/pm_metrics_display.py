"""
Project Manager Metrics Display Functions
Display comprehensive project management metrics in the dashboard
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
    """Safely load a CSV file from the PM metrics directory"""
    filepath = os.path.join(CURRENT_DIR, filename)
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        return None

# ============================================
# PROJECT CHARTER METRICS
# ============================================
def display_project_charter_metrics():
    """Display Project Charter metrics"""
    
    key_prefix = f"project_charter_{uuid.uuid4().hex[:8]}"
    
    df = load_csv_safe('project_charter_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for Project Charter Metrics")
        return
    
    # Charter overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        approved_projects = len(df[df['approval_status'] == 'Approved'])
        st.metric("Approved Projects", approved_projects)
    
    with col2:
        avg_alignment = df['strategic_alignment_score'].mean()
        st.metric("Avg Strategic Alignment", f"{avg_alignment:.1f}/10")
    
    with col3:
        total_budget = df['total_budget'].sum()
        st.metric("Total Portfolio Budget", f"${total_budget/1000000:.1f}M")
    
    with col4:
        avg_stakeholder_buyin = df['stakeholder_buy_in'].mean()
        st.metric("Stakeholder Buy-in", f"{avg_stakeholder_buyin:.1f}%")
    
    # Charter analysis tabs
    tab1, tab2, tab3 = st.tabs(["Project Overview", "Approval Status", "Strategic Alignment"])
    
    with tab1:
        # Project portfolio view
        fig = px.sunburst(df, 
                         path=['project_type', 'priority', 'project_name'],
                         values='total_budget',
                         title="Project Portfolio by Type and Priority")
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_sunburst")
    
    with tab2:
        # Approval status breakdown
        approval_counts = df['approval_status'].value_counts()
        fig = px.pie(values=approval_counts.values, names=approval_counts.index,
                    title="Project Approval Status Distribution")
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_approval")
    
    with tab3:
        # Strategic alignment analysis
        fig = px.scatter(df, x='strategic_alignment_score', y='business_justification_score',
                        size='total_budget', color='project_type', hover_name='project_name',
                        title="Strategic Alignment vs Business Justification")
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_alignment")

# ============================================
# PROJECT TIMELINE & BUDGET PERFORMANCE
# ============================================
def display_project_timeline_budget_performance():
    """Display Project Timeline & Budget Performance"""
    
    key_prefix = f"project_timeline_{uuid.uuid4().hex[:8]}"
    
    df = load_csv_safe('project_timeline_budget_performance.csv')
    
    if df is None or df.empty:
        st.info("No data available for Project Timeline & Budget Performance")
        return
    
    # Performance KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        on_time_projects = len(df[df['schedule_status'] == 'On Track'])
        st.metric("On Schedule", f"{on_time_projects}/{len(df)}")
    
    with col2:
        on_budget_projects = len(df[df['budget_status'] == 'On Track'])
        st.metric("On Budget", f"{on_budget_projects}/{len(df)}")
    
    with col3:
        avg_completion = df['timeline_completion_pct'].mean()
        st.metric("Avg Completion", f"{avg_completion:.1f}%")
    
    with col4:
        avg_health = df['health_score'].mean()
        st.metric("Avg Health Score", f"{avg_health:.1f}/10")
    
    # Performance analysis tabs
    tab1, tab2, tab3 = st.tabs(["Progress Overview", "Budget Analysis", "Health Dashboard"])
    
    with tab1:
        # Progress tracking
        fig = px.bar(df.sort_values('timeline_completion_pct', ascending=True), 
                    x='timeline_completion_pct', y='project_name', orientation='h',
                    color='schedule_status',
                    color_discrete_map={'On Track': 'green', 'Delayed': 'red', 'Completed': 'blue'},
                    title="Project Progress Overview")
        fig.add_vline(x=100, line_dash="dash", line_color="gray", annotation_text="Target")
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_progress")
    
    with tab2:
        # Budget variance analysis
        fig = px.scatter(df, x='total_budget', y='budget_variance_pct',
                        size='timeline_completion_pct', color='budget_status',
                        hover_name='project_name',
                        title="Budget Variance vs Project Size")
        fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Budget Target")
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_budget")
    
    with tab3:
        # Project health matrix
        fig = px.scatter(df, x='timeline_completion_pct', y='health_score',
                        size='total_budget', color='status',
                        hover_name='project_name',
                        title="Project Health vs Progress")
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_health")

# ============================================
# REQUIREMENTS TRACEABILITY MATRIX
# ============================================
def display_requirements_traceability_matrix():
    """Display Requirements Traceability Matrix"""
    
    key_prefix = f"requirements_{uuid.uuid4().hex[:8]}"
    
    df = load_csv_safe('requirements_traceability_matrix.csv')
    
    if df is None or df.empty:
        st.info("No data available for Requirements Traceability Matrix")
        return
    
    # Convert date columns
    if 'date_identified' in df.columns:
        df['date_identified'] = pd.to_datetime(df['date_identified'])
    if 'target_completion' in df.columns:
        df['target_completion'] = pd.to_datetime(df['target_completion'])
    
    # Requirements KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_requirements = len(df)
        st.metric("Total Requirements", total_requirements)
    
    with col2:
        completed_reqs = len(df[df['status'] == 'Completed'])
        completion_rate = (completed_reqs / total_requirements * 100) if total_requirements > 0 else 0
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    with col3:
        avg_test_coverage = df['test_coverage_pct'].mean()
        st.metric("Avg Test Coverage", f"{avg_test_coverage:.1f}%")
    
    with col4:
        high_risk_reqs = len(df[df['risk_level'] == 'High'])
        st.metric("High Risk Requirements", high_risk_reqs)
    
    # Requirements analysis
    tab1, tab2, tab3 = st.tabs(["Status Overview", "Coverage Analysis", "Risk Assessment"])
    
    with tab1:
        # Requirements by status and type
        status_type = df.groupby(['status', 'requirement_type']).size().reset_index(name='count')
        fig = px.bar(status_type, x='status', y='count', color='requirement_type',
                    title="Requirements by Status and Type")
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_status")
    
    with tab2:
        # Test coverage analysis
        fig = px.histogram(df, x='test_coverage_pct', nbins=20,
                          title="Test Coverage Distribution")
        fig.add_vline(x=80, line_dash="dash", line_color="red", annotation_text="Target (80%)")
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_coverage")
    
    with tab3:
        # Risk vs complexity analysis
        fig = px.scatter(df, x='complexity_score', y='effort_estimate_hours',
                        color='risk_level', size='completion_pct',
                        hover_name='requirement_id',
                        title="Requirement Complexity vs Effort")
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_risk")

# ============================================
# RAID LOG METRICS
# ============================================
def display_raid_log_metrics():
    """Display RAID Log (Risks, Actions, Issues, Decisions)"""
    
    key_prefix = f"raid_log_{uuid.uuid4().hex[:8]}"
    
    df = load_csv_safe('raid_log_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for RAID Log Metrics")
        return
    
    # RAID KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        open_items = len(df[df['status'].isin(['Open', 'In Progress'])])
        st.metric("Open RAID Items", open_items)
    
    with col2:
        high_severity = len(df[df['severity'].isin(['High', 'Critical'])])
        st.metric("High/Critical Items", high_severity)
    
    with col3:
        avg_days_open = df['days_open'].mean()
        st.metric("Avg Days Open", f"{avg_days_open:.1f}")
    
    with col4:
        escalated_items = len(df[df['escalated'] == True])
        st.metric("Escalated Items", escalated_items)
    
    # RAID analysis
    tab1, tab2, tab3 = st.tabs(["RAID Overview", "Risk Matrix", "Resolution Tracking"])
    
    with tab1:
        # RAID items by type and severity
        raid_summary = df.groupby(['type', 'severity']).size().reset_index(name='count')
        fig = px.bar(raid_summary, x='type', y='count', color='severity',
                    color_discrete_map={'Low': 'green', 'Medium': 'yellow', 'High': 'orange', 'Critical': 'red'},
                    title="RAID Items by Type and Severity")
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_overview")
    
    with tab2:
        # Risk matrix (for risk items only)
        risks = df[df['type'] == 'Risk'].copy()
        if not risks.empty and 'probability_score' in risks.columns:
            fig = px.scatter(risks, x='probability_score', y='impact_score',
                            size='days_open', color='status',
                            hover_name='raid_id',
                            title="Risk Probability vs Impact Matrix",
                            labels={'probability_score': 'Probability', 'impact_score': 'Impact'})
            # Add quadrant lines
            fig.add_hline(y=5, line_dash="dash", line_color="gray")
            fig.add_vline(x=5, line_dash="dash", line_color="gray")
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_risk_matrix")
    
    with tab3:
        # Resolution time analysis
        resolved_items = df[df['status'].isin(['Resolved', 'Closed'])]
        if not resolved_items.empty:
            fig = px.histogram(resolved_items, x='days_open', nbins=20,
                              title="Resolution Time Distribution")
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_resolution")

# ============================================
# RESOURCE ALLOCATION METRICS
# ============================================
def display_resource_allocation_metrics():
    """Display Resource Allocation metrics"""
    
    key_prefix = f"resource_allocation_{uuid.uuid4().hex[:8]}"
    
    df = load_csv_safe('resource_allocation_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for Resource Allocation Metrics")
        return
    
    # Resource KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_resources = len(df)
        st.metric("Total Resources", total_resources)
    
    with col2:
        avg_utilization = df['utilization_pct'].mean()
        st.metric("Avg Utilization", f"{avg_utilization:.1f}%")
    
    with col3:
        total_cost = df['cost_to_date'].sum()
        st.metric("Total Resource Cost", f"${total_cost/1000:.0f}K")
    
    with col4:
        avg_efficiency = df['efficiency_score'].mean()
        st.metric("Avg Efficiency", f"{avg_efficiency:.1f}/10")
    
    # Resource analysis
    tab1, tab2, tab3 = st.tabs(["Allocation Overview", "Utilization Analysis", "Cost Analysis"])
    
    with tab1:
        # Resource allocation by role and project
        role_project = df.groupby(['role', 'project_name']).agg({
            'allocation_pct': 'mean',
            'cost_to_date': 'sum'
        }).reset_index()
        
        fig = px.bar(role_project, x='role', y='allocation_pct', color='project_name',
                    title="Resource Allocation by Role and Project")
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_allocation")
    
    with tab2:
        # Utilization vs efficiency analysis
        fig = px.scatter(df, x='utilization_pct', y='efficiency_score',
                        size='cost_to_date', color='role',
                        hover_name='resource_name',
                        title="Resource Utilization vs Efficiency")
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_utilization")
    
    with tab3:
        # Cost analysis by role
        cost_by_role = df.groupby('role')['cost_to_date'].sum().sort_values(ascending=True)
        fig = px.bar(x=cost_by_role.values, y=cost_by_role.index, orientation='h',
                    title="Total Cost by Role")
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_cost")

# ============================================
# STAKEHOLDER COMMUNICATION METRICS
# ============================================
def display_stakeholder_communication_metrics():
    """Display Stakeholder Communication metrics"""
    
    key_prefix = f"communication_{uuid.uuid4().hex[:8]}"
    
    df = load_csv_safe('stakeholder_communication_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for Stakeholder Communication Metrics")
        return
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Communication KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_communications = len(df)
        st.metric("Total Communications", total_communications)
    
    with col2:
        avg_engagement = df['engagement_score'].mean()
        st.metric("Avg Engagement", f"{avg_engagement:.1f}/10")
    
    with col3:
        avg_satisfaction = df['satisfaction_score'].mean()
        st.metric("Avg Satisfaction", f"{avg_satisfaction:.1f}/10")
    
    with col4:
        avg_response_time = df['response_time_hours'].mean()
        st.metric("Avg Response Time", f"{avg_response_time:.1f}h")
    
    # Communication analysis
    tab1, tab2 = st.tabs(["Communication Trends", "Stakeholder Analysis"])
    
    with tab1:
        if 'date' in df.columns:
            # Communication frequency over time
            comm_trends = df.groupby(['date', 'communication_type']).size().reset_index(name='count')
            fig = px.line(comm_trends, x='date', y='count', color='communication_type',
                         title="Communication Frequency Over Time")
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_trends")
    
    with tab2:
        # Stakeholder engagement analysis
        stakeholder_metrics = df.groupby('stakeholder_type').agg({
            'engagement_score': 'mean',
            'satisfaction_score': 'mean',
            'response_time_hours': 'mean'
        }).reset_index()
        
        fig = px.bar(stakeholder_metrics, x='stakeholder_type', y='engagement_score',
                    title="Average Engagement Score by Stakeholder Type")
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_stakeholders")

# ============================================
# PROJECT PORTFOLIO DASHBOARD
# ============================================
def display_project_portfolio_dashboard_metrics():
    """Display Project Portfolio Dashboard"""
    
    key_prefix = f"portfolio_{uuid.uuid4().hex[:8]}"
    
    df = load_csv_safe('project_portfolio_dashboard_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for Project Portfolio Dashboard")
        return
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Latest portfolio metrics
    latest = df.iloc[-1] if not df.empty else df.iloc[0]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Projects", int(latest['active_projects']))
    
    with col2:
        st.metric("Portfolio Budget", f"${latest['total_portfolio_budget']/1000000:.1f}M")
    
    with col3:
        st.metric("On-Time Delivery", f"{latest['on_time_delivery_rate']:.1f}%")
    
    with col4:
        st.metric("Stakeholder Satisfaction", f"{latest['stakeholder_satisfaction_avg']:.1f}/10")
    
    # Portfolio trends
    if len(df) > 1:
        # Portfolio health over time
        fig = make_subplots(rows=2, cols=2,
                           subplot_titles=('Active Projects', 'Budget Utilization', 
                                         'Delivery Performance', 'Stakeholder Satisfaction'))
        
        fig.add_trace(go.Scatter(x=df['date'], y=df['active_projects'], 
                                name='Active Projects'), row=1, col=1)
        
        fig.add_trace(go.Scatter(x=df['date'], y=df['budget_variance_pct'], 
                                name='Budget Variance %'), row=1, col=2)
        
        fig.add_trace(go.Scatter(x=df['date'], y=df['on_time_delivery_rate'], 
                                name='On-Time %'), row=2, col=1)
        
        fig.add_trace(go.Scatter(x=df['date'], y=df['stakeholder_satisfaction_avg'], 
                                name='Satisfaction'), row=2, col=2)
        
        fig.update_layout(title="Portfolio Health Trends Over Time", height=600)
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_trends")

# ============================================
# MAIN REGISTRY FOR PM METRICS
# ============================================
PM_METRICS = {
    'project_charter_metrics': display_project_charter_metrics,
    'project_timeline_budget_performance': display_project_timeline_budget_performance,
    'requirements_traceability_matrix': display_requirements_traceability_matrix,
    'raid_log_metrics': display_raid_log_metrics,
    'resource_allocation_metrics': display_resource_allocation_metrics,
    'stakeholder_communication_metrics': display_stakeholder_communication_metrics,
    'project_portfolio_dashboard_metrics': display_project_portfolio_dashboard_metrics,
}

def get_available_metrics():
    """Return list of available PM metrics"""
    return list(PM_METRICS.keys())

def display_metric(metric_name):
    """Display a specific metric by name"""
    if metric_name in PM_METRICS:
        PM_METRICS[metric_name]()
    else:
        st.error(f"Metric '{metric_name}' not found")
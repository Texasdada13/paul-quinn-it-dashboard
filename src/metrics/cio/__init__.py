"""
CIO Metrics Display Functions
These functions read the generated CSV files and display metrics in the dashboard
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import numpy as np
from plotly.subplots import make_subplots
import uuid  # Add this import at the top of your file


# Get the directory where this file is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_csv_safe(filename):
    """Safely load a CSV file from the CIO metrics directory"""
    filepath = os.path.join(CURRENT_DIR, filename)
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        return None

# ============================================
# APP COST ANALYSIS METRICS
# ============================================
def display_app_cost_analysis_metrics():
    """Display Application Cost Analysis metrics"""
    
    # Generate a unique key prefix for this function call
    key_prefix = f"app_cost_{uuid.uuid4().hex[:8]}"
     
    df = load_csv_safe('app_cost_analysis_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for App Cost Analysis Metrics")
        return
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_monthly_cost = df.groupby('date')['monthly_cost'].sum().mean()
        st.metric("Avg Monthly Cost", f"${total_monthly_cost:,.0f}")
    
    with col2:
        avg_utilization = df['utilization_rate'].mean()
        st.metric("Avg Utilization Rate", f"{avg_utilization:.1f}%")
    
    with col3:
        high_redundancy = len(df[df['redundancy_index'] > 0.5])
        st.metric("High Redundancy Apps", high_redundancy)
    
    with col4:
        consolidation_candidates = df[df['consolidation_potential'] == 'Yes']['application'].nunique()
        st.metric("Consolidation Opportunities", consolidation_candidates)
    
    # Create visualizations
    tab1, tab2, tab3 = st.tabs(["Cost by Application", "Utilization Analysis", "Redundancy Analysis"])
    
    with tab1:
        # Cost by application
        app_costs = df.groupby('application')['monthly_cost'].mean().sort_values(ascending=True).tail(10)
        fig = px.bar(x=app_costs.values, y=app_costs.index, orientation='h',
                    title="Top 10 Applications by Monthly Cost",
                    labels={'x': 'Monthly Cost ($)', 'y': 'Application'})
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_cost_by_app")  # ADD KEY
    
    with tab2:
        # Utilization scatter plot
        latest_data = df[df['date'] == df['date'].max()]
        fig = px.scatter(latest_data, x='licenses_total', y='licenses_used',
                        size='monthly_cost', color='utilization_rate',
                        hover_data=['application'],
                        title="License Utilization Analysis",
                        labels={'licenses_total': 'Total Licenses', 'licenses_used': 'Used Licenses'})
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_utilization")  # ADD KEY
    
    with tab3:
        # Redundancy analysis
        redundancy_data = df.groupby('application')['redundancy_index'].mean().sort_values(ascending=False).head(10)
        fig = px.bar(redundancy_data, title="Applications with Highest Redundancy Index",
                    labels={'value': 'Redundancy Index', 'index': 'Application'})
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_redundancy")  # ADD KEY

# ============================================
# BUSINESS UNIT IT SPEND
# ============================================
def display_business_unit_it_spend():
    """Display Business Unit IT Spend metrics"""
    
    # Generate unique key prefix
    key_prefix = f"bu_spend_{uuid.uuid4().hex[:8]}" 
    
    df = load_csv_safe('business_unit_it_spend.csv')
    
    if df is None or df.empty:
        st.info("No data available for Business Unit IT Spend")
        return
    
    df['date'] = pd.to_datetime(df['date'])
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_budget = df['monthly_budget'].sum() / df['business_unit'].nunique()
        st.metric("Avg Monthly Budget", f"${total_budget:,.0f}")
    
    with col2:
        avg_variance = df['budget_variance_pct'].mean()
        st.metric("Avg Budget Variance", f"{avg_variance:+.1f}%")
    
    with col3:
        over_budget = len(df[df['budget_variance_pct'] > 5]) / len(df) * 100
        st.metric("% Over Budget", f"{over_budget:.1f}%")
    
    with col4:
        avg_per_fte = df['spend_per_fte'].mean()
        st.metric("Avg Spend per FTE", f"${avg_per_fte:,.0f}")
    
    # Visualizations
    tab1, tab2 = st.tabs(["Spend by Unit", "Budget Performance"])
    
    with tab1:
        unit_spend = df.groupby('business_unit')['monthly_spend'].mean().sort_values(ascending=True)
        fig = px.bar(x=unit_spend.values, y=unit_spend.index, orientation='h',
                    title="Average Monthly Spend by Business Unit",
                    labels={'x': 'Monthly Spend ($)', 'y': 'Business Unit'})
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_spend_by_unit")  # ADD KEY
    
    with tab2:
        latest = df[df['date'] == df['date'].max()]
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Budget', x=latest['business_unit'], y=latest['monthly_budget']))
        fig.add_trace(go.Bar(name='Actual', x=latest['business_unit'], y=latest['monthly_spend']))
        fig.update_layout(title="Budget vs Actual Spend (Latest Month)", barmode='group')
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_budget_vs_actual")  # ADD KEY

# ============================================
# DIGITAL TRANSFORMATION METRICS
# ============================================
def display_digital_transformation_metrics():
    """Display Digital Transformation metrics"""
    
    # Generate unique key prefix
    key_prefix = f"digital_trans_{uuid.uuid4().hex[:8]}"
    
    df = load_csv_safe('digital_transformation_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for Digital Transformation Metrics")
        return
    
    df['date'] = pd.to_datetime(df['date'])
    latest = df.iloc[-1]
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Transformation Score", f"{latest['transformation_score']:.1f}%",
                 delta=f"{latest['transformation_score'] - df.iloc[0]['transformation_score']:+.1f}%")
    
    with col2:
        st.metric("Online Adoption Rate", f"{latest['online_adoption_rate']:.1f}%",
                 delta=f"{latest['online_adoption_rate'] - df.iloc[0]['online_adoption_rate']:+.1f}%")
    
    with col3:
        st.metric("Digital Literacy (Students)", f"{latest['digital_literacy_students']:.1f}/5")
    
    with col4:
        st.metric("Satisfaction Score", f"{latest['satisfaction_score']:.1f}/5")
    
    # Trend charts
    tab1, tab2, tab3 = st.tabs(["Progress Trends", "Participation", "Milestones"])
    
    with tab1:
        metrics_to_plot = ['transformation_score', 'online_adoption_rate', 'platform_utilization_pct']
        fig = px.line(df, x='date', y=metrics_to_plot,
                     title="Digital Transformation Progress Over Time",
                     labels={'value': 'Percentage', 'variable': 'Metric'})
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_progress")  # ADD KEY
    
    with tab2:
        participation_metrics = ['student_participation_pct', 'faculty_participation_pct', 'virtual_engagement_rate']
        fig = px.line(df, x='date', y=participation_metrics,
                     title="Digital Learning Participation Trends",
                     labels={'value': 'Percentage', 'variable': 'Participant Type'})
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_participation")  # ADD KEY
    
    with tab3:
        fig = px.bar(df, x='date', y='innovation_milestones',
                    title="Innovation Milestones Achieved Over Time")
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_milestones")  # ADD KEY

# ============================================
# RISK METRICS
# ============================================
def display_risk_metrics():
    """Display Risk Management metrics"""
    
    # Generate unique key prefix
    key_prefix = f"risk_{uuid.uuid4().hex[:8]}"
    
    df = load_csv_safe('risk_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for Risk Metrics")
        return
    
    df['date'] = pd.to_datetime(df['date'])
    
    # Risk overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        high_risk = len(df[df['risk_heat_map'] == 'Critical'])
        st.metric("Critical Risks", high_risk)
    
    with col2:
        avg_exposure = df['risk_exposure_level'].mean()
        st.metric("Avg Risk Exposure", f"{avg_exposure:.1f}")
    
    with col3:
        mitigation_pct = len(df[df['mitigation_status'] == 'Resolved']) / len(df) * 100
        st.metric("Risks Mitigated", f"{mitigation_pct:.1f}%")
    
    with col4:
        avg_compliance = df['compliance_adherence_pct'].mean()
        st.metric("Compliance Rate", f"{avg_compliance:.1f}%")
    
    # Risk visualizations
    tab1, tab2 = st.tabs(["Risk Heat Map", "Risk by Category"])
    
    with tab1:
        risk_matrix = df.groupby(['risk_category', 'risk_heat_map']).size().reset_index(name='count')
        fig = px.treemap(risk_matrix, path=['risk_category', 'risk_heat_map'], values='count',
                        title="Risk Distribution Heat Map",
                        color='count', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_heatmap")  # ADD KEY
    
    with tab2:
        category_risk = df.groupby('risk_category')['risk_exposure_level'].mean().sort_values()
        fig = px.bar(x=category_risk.values, y=category_risk.index, orientation='h',
                    title="Average Risk Exposure by Category",
                    labels={'x': 'Risk Exposure Level', 'y': 'Category'})
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_by_category")  # ADD KEY



# ============================================
# STRATEGIC ALIGNMENT METRICS
# ============================================
def display_strategic_alignment_metrics():
    """Display Strategic Alignment metrics"""
    
    # Generate unique key prefix
    key_prefix = f"strategic_{uuid.uuid4().hex[:8]}"

    
    
    df = load_csv_safe('strategic_alignment_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for Strategic Alignment Metrics")
        return
    
    df['date'] = pd.to_datetime(df['date'])
    latest_date = df['date'].max()
    latest = df[df['date'] == latest_date]
    
    # Average scores across all initiatives
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_alignment = latest['alignment_score'].mean()
        st.metric("Alignment Score", f"{avg_alignment:.1f}/10")
    
    with col2:
        avg_impact = latest['student_experience_impact'].mean()
        st.metric("Student Impact", f"{avg_impact:.1f}/10")
    
    with col3:
        avg_equity = latest['equity_advancement_score'].mean()
        st.metric("Equity Score", f"{avg_equity:.1f}/10")
    
    with col4:
        avg_sustainability = latest['sustainability_factor'].mean()
        st.metric("Sustainability", f"{avg_sustainability:.1f}/10")
    
    # Visualizations
    tab1, tab2 = st.tabs(["Initiative Alignment", "Impact Analysis"])
    
    with tab1:
        # Radar chart
        fig = go.Figure()
        # ... radar chart code ...
        fig.update_layout(title="Strategic Alignment Radar - Top Initiatives",
                         polar=dict(radialaxis=dict(visible=True, range=[0, 10])))
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_radar")  # ADD KEY
    
    with tab2:
        # Impact vs Cost scatter
        fig = px.scatter(latest, x='cost_per_student_benefited', y='student_experience_impact',
                        size='alignment_score', color='initiative',
                        title="Student Impact vs Cost Efficiency",
                        labels={'cost_per_student_benefited': 'Cost per Student ($)',
                               'student_experience_impact': 'Student Impact Score'})
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_impact_cost")  # ADD KEY


# ============================================
# VENDOR METRICS
# ============================================
def display_vendor_metrics():
    """Display Vendor Performance metrics"""
    
    # Generate unique key prefix
    key_prefix = f"vendor_{uuid.uuid4().hex[:8]}"
    
    df = load_csv_safe('vendor_metrics.csv')
    
    if df is None or df.empty:
        st.info("No data available for Vendor Metrics")
        return
    
    df['date'] = pd.to_datetime(df['date'])
    
    # Vendor KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_satisfaction = df['satisfaction_score'].mean()
        st.metric("Avg Satisfaction", f"{avg_satisfaction:.1f}/5")
    
    with col2:
        avg_sla = df['sla_compliance_pct'].mean()
        st.metric("SLA Compliance", f"{avg_sla:.1f}%")
    
    with col3:
        total_spend = df['annual_spend'].sum() / df['vendor'].nunique()
        st.metric("Avg Annual Spend", f"${total_spend:,.0f}")
    
    with col4:
        avg_uptime = df['uptime_pct'].mean()
        st.metric("Avg Uptime", f"{avg_uptime:.1f}%")
    
    # Vendor analysis
    tab1, tab2 = st.tabs(["Vendor Performance", "Spend Analysis"])
    
    with tab1:
        vendor_scores = df.groupby('vendor')[['satisfaction_score', 'sla_compliance_pct', 'uptime_pct']].mean()
        vendor_scores = vendor_scores.sort_values('satisfaction_score', ascending=False).head(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Satisfaction (x20)', x=vendor_scores.index, y=vendor_scores['satisfaction_score']*20))
        fig.add_trace(go.Bar(name='SLA Compliance %', x=vendor_scores.index, y=vendor_scores['sla_compliance_pct']))
        fig.add_trace(go.Bar(name='Uptime %', x=vendor_scores.index, y=vendor_scores['uptime_pct']))
        fig.update_layout(title="Top 10 Vendor Performance Metrics", barmode='group')
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_performance")  # ADD KEY
    
    with tab2:
        # Create subtabs for different spend analysis views
        spend_tabs = st.tabs(["📊 Spend vs Budget", "📈 Spend vs Performance", "📉 Spend Trends", "🎯 Value Matrix"])
        
        # Option 1: Horizontal Bar Chart with Budget Comparison
        with spend_tabs[0]:
            vendor_spend = df.groupby('vendor')['annual_spend'].mean().sort_values(ascending=True).head(10)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=vendor_spend.index,
                x=vendor_spend.values,
                name='Annual Spend',
                orientation='h',
                marker_color='#2E86AB',
                text=[f'${x:,.0f}' for x in vendor_spend.values],
                textposition='outside'
            ))
            
            fig.update_layout(
                title="Top 10 Vendors by Annual Spend",
                xaxis_title="Annual Spend ($)",
                yaxis_title="Vendor",
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_spend_budget")
        
        # Option 3: Combo Chart - Spend vs Performance
        with spend_tabs[1]:
            vendor_summary = df.groupby('vendor').agg({
                'annual_spend': 'mean',
                'satisfaction_score': 'mean'
            }).nlargest(10, 'annual_spend')
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(name='Annual Spend', 
                    x=vendor_summary.index, 
                    y=vendor_summary['annual_spend'],
                    marker_color='#4A90E2'),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(name='Satisfaction Score', 
                        x=vendor_summary.index, 
                        y=vendor_summary['satisfaction_score'],
                        mode='lines+markers', 
                        marker=dict(size=12, color='#E94B3C'),
                        line=dict(width=3)),
                secondary_y=True,
            )
            
            fig.update_layout(title="Vendor Spend vs Satisfaction Score", height=400)
            fig.update_xaxes(title_text="Vendor", tickangle=45)
            fig.update_yaxes(title_text="Annual Spend ($)", secondary_y=False)
            fig.update_yaxes(title_text="Satisfaction Score (1-5)", secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_spend_satisfaction")
        
        # Option 4: Spend Trend Analysis
        with spend_tabs[2]:
            # Get top 5 vendors by spend
            top_vendors = df.groupby('vendor')['annual_spend'].mean().nlargest(5).index
            trend_data = df[df['vendor'].isin(top_vendors)].copy()
            
            # Group by date and vendor
            daily_trend = trend_data.groupby(['date', 'vendor'])['daily_spend'].sum().reset_index()
            
            fig = px.line(daily_trend, x='date', y='daily_spend', color='vendor',
                        title='Top 5 Vendor Daily Spend Trends',
                        labels={'daily_spend': 'Daily Spend ($)', 'date': 'Date'})
            
            fig.update_layout(height=400, hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_spend_trend")
        
        # Option 5: Spend Efficiency Matrix
        with spend_tabs[3]:
            vendor_matrix = df.groupby('vendor').agg({
                'annual_spend': 'mean',
                'satisfaction_score': 'mean',
                'sla_compliance_pct': 'mean'
            }).reset_index()
            
            fig = px.scatter(vendor_matrix, 
                            x='annual_spend', 
                            y='satisfaction_score',
                            size='sla_compliance_pct',
                            hover_name='vendor',
                            title='Vendor Value Matrix (Size = SLA Compliance)',
                            labels={'annual_spend': 'Annual Spend ($)', 
                                'satisfaction_score': 'Satisfaction Score (1-5)',
                                'sla_compliance_pct': 'SLA Compliance %'})
            
            # Add quadrant lines
            median_spend = vendor_matrix['annual_spend'].median()
            fig.add_hline(y=3.5, line_dash="dash", line_color="gray", opacity=0.3)
            fig.add_vline(x=median_spend, line_dash="dash", line_color="gray", opacity=0.3)
            
            # Add quadrant labels
            fig.add_annotation(x=0.95, y=0.95, xref="paper", yref="paper",
                            text="High Satisfaction<br>High Cost", showarrow=False, bgcolor="rgba(255,255,255,0.8)")
            fig.add_annotation(x=0.05, y=0.95, xref="paper", yref="paper",
                            text="High Satisfaction<br>Low Cost ✓", showarrow=False, bgcolor="rgba(144,238,144,0.3)")
            fig.add_annotation(x=0.95, y=0.05, xref="paper", yref="paper",
                            text="Low Satisfaction<br>High Cost ✗", showarrow=False, bgcolor="rgba(255,182,193,0.3)")
            fig.add_annotation(x=0.05, y=0.05, xref="paper", yref="paper",
                            text="Low Satisfaction<br>Low Cost", showarrow=False, bgcolor="rgba(255,255,255,0.8)")
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_value_matrix")
# ============================================
# MAIN REGISTRY FOR METRICS
# ============================================
# This dictionary maps metric names to their display functions
CIO_METRICS = {
    'app_cost_analysis_metrics': display_app_cost_analysis_metrics,
    'business_unit_it_spend': display_business_unit_it_spend,
    'digital_transformation_metrics': display_digital_transformation_metrics,
    'risk_metrics': display_risk_metrics,
    'strategic_alignment_metrics': display_strategic_alignment_metrics,
    'vendor_metrics': display_vendor_metrics,
}

def get_available_metrics():
    """Return list of available CIO metrics"""
    return list(CIO_METRICS.keys())

def display_metric(metric_name):
    """Display a specific metric by name"""
    if metric_name in CIO_METRICS:
        CIO_METRICS[metric_name]()
    else:
        st.error(f"Metric '{metric_name}' not found")
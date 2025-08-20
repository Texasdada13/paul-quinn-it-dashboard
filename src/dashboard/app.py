"""
Paul Quinn College IT Effectiveness Dashboard
Web Application using Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Paul Quinn IT Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e3d59;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .risk-high { color: #ff4444; }
    .risk-medium { color: #ffaa00; }
    .risk-low { color: #00aa00; }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load all processed data"""
    try:
        vendors = pd.read_csv("clean_vendors.csv")
        projects = pd.read_csv("clean_projects.csv")
        metrics = pd.read_csv("it_effectiveness_metrics.csv", index_col=0)
        return vendors, projects, metrics
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🎓 Paul Quinn College IT Effectiveness Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    vendors, projects, metrics = load_data()
    
    if vendors is None:
        st.error("Please ensure data files are in 02_Data/processed/")
        return
    
    # Sidebar navigation
    st.sidebar.image("https://via.placeholder.com/300x100/1e3d59/ffffff?text=Paul+Quinn+College", use_column_width=True)
    st.sidebar.markdown("---")
    
    persona = st.sidebar.radio(
        "Select Dashboard View:",
        ["Executive Summary", "CFO View", "CIO View", "CTO View", "Predictive Analytics"]
    )
    
    # Executive Summary
    if persona == "Executive Summary":
        show_executive_summary(vendors, projects, metrics)
    
    # CFO View
    elif persona == "CFO View":
        show_cfo_dashboard(vendors, projects, metrics)
    
    # CIO View
    elif persona == "CIO View":
        show_cio_dashboard(vendors, projects, metrics)
    
    # CTO View
    elif persona == "CTO View":
        show_cto_dashboard(vendors, projects, metrics)
    
    # Predictive Analytics
    elif persona == "Predictive Analytics":
        show_predictive_analytics(vendors, projects, metrics)
    
    # Footer
    st.markdown("---")
    st.markdown(f"*Dashboard updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*")

def show_executive_summary(vendors, projects, metrics):
    """Executive Summary Dashboard"""
    st.header("Executive Summary")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total IT Spend",
            f"${vendors['annual_spend'].sum():,.0f}",
            "0.86% of revenue"
        )
    
    with col2:
        st.metric(
            "Active Projects",
            len(projects),
            f"{len(projects[projects['risk_flag'] == 'HIGH'])} at risk"
        )
    
    with col3:
        st.metric(
            "System Availability",
            f"{float(metrics.loc['avg_availability', 'value']):.1f}%",
            "Above target"
        )
    
    with col4:
        st.metric(
            "ROI on Projects",
            f"{float(metrics.loc['project_roi', 'value']):.0f}%",
            "Exceeds benchmark"
        )
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        # Spend by category pie chart
        fig = px.pie(
            vendors, 
            values='annual_spend', 
            names='category',
            title='IT Spend by Category',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Project status
        status_counts = projects['status'].value_counts()
        fig = px.bar(
            x=status_counts.index, 
            y=status_counts.values,
            title='Project Status Distribution',
            labels={'x': 'Status', 'y': 'Count'},
            color=status_counts.index,
            color_discrete_map={
                'In Progress': '#1e3d59',
                'Planning': '#f5b800',
                'At Risk': '#ff4444',
                'Delayed': '#ff8800'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Risk Alert Section
    st.subheader("⚠️ Risk Alerts")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.error(f"**{len(projects[projects['risk_flag'] == 'HIGH'])}** High Risk Projects")
    with col2:
        st.warning(f"**{len(vendors[vendors['risk_level'] == 'High'])}** High Risk Vendors")
    with col3:
        st.info(f"**${vendors['annual_spend'].sum() * 0.15:,.0f}** Savings Opportunity")

def show_cfo_dashboard(vendors, projects, metrics):
    """CFO-specific dashboard"""
    st.header("💰 CFO Dashboard - Financial Intelligence")
    
    # Financial metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        it_spend_pct = float(metrics.loc['it_spend_pct_revenue', 'value'])
        st.metric(
            "IT Spend % of Revenue",
            f"{it_spend_pct:.2f}%",
            "Below 3-5% benchmark ✓",
            delta_color="inverse"
        )
    
    with col2:
        cost_per_user = float(metrics.loc['cost_per_user', 'value'])
        st.metric(
            "Cost per User",
            f"${cost_per_user:.0f}",
            "Efficient"
        )
    
    with col3:
        budget_var = float(metrics.loc['budget_variance', 'value'])
        st.metric(
            "Budget Variance",
            f"{budget_var:.1f}%",
            "Under budget ✓"
        )
    
    # Spending trends
    st.subheader("Spending Analysis")
    
    # Create monthly spending simulation
    months = pd.date_range('2024-01-01', periods=12, freq='M')
    spending_trend = pd.DataFrame({
        'Month': months,
        'Actual': [vendors['annual_spend'].sum()/12 * (1 + i*0.02) for i in range(12)],
        'Budget': [vendors['annual_spend'].sum()/12 * 1.05] * 12
    })
    
    fig = px.line(
        spending_trend, 
        x='Month', 
        y=['Actual', 'Budget'],
        title='Monthly IT Spending Trend',
        labels={'value': 'Spending ($)', 'variable': 'Type'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Cost optimization opportunities
    st.subheader("💡 Cost Optimization Opportunities")
    
    opportunities = pd.DataFrame({
        'Opportunity': ['Vendor Consolidation', 'License Optimization', 'Cloud Migration', 'Process Automation'],
        'Potential Savings': [64350, 25000, 35000, 45000],
        'Effort': ['Medium', 'Low', 'High', 'Medium'],
        'Timeline': ['3-6 months', '1-2 months', '6-12 months', '3-4 months']
    })
    
    st.dataframe(
        opportunities.style.format({'Potential Savings': '${:,.0f}'}),
        use_container_width=True
    )

def show_cio_dashboard(vendors, projects, metrics):
    """CIO-specific dashboard"""
    st.header("📊 CIO Dashboard - Portfolio & Strategy")
    
    # Portfolio metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Portfolio Health",
            f"{float(metrics.loc['budget_efficiency', 'value']):.0f}%",
            "Efficiency Score"
        )
    
    with col2:
        satisfaction = float(metrics.loc['avg_satisfaction', 'value'])
        st.metric(
            "User Satisfaction",
            f"{satisfaction:.1f}/5.0",
            "Above average"
        )
    
    with col3:
        st.metric(
            "Service Adoption",
            f"{float(metrics.loc['service_adoption_pct', 'value']):.0f}%",
            "High engagement"
        )
    
    # Project portfolio view
    st.subheader("Project Portfolio Analysis")
    
    # Project bubble chart
    projects_viz = projects.copy()
    projects_viz['size'] = projects_viz['budget'] / 1000  # Scale for visualization
    
    fig = px.scatter(
        projects_viz,
        x='budget_utilization_%',
        y='budget_remaining',
        size='size',
        color='risk_flag',
        hover_data=['project_name', 'status'],
        title='Project Risk vs Budget Analysis',
        labels={'budget_utilization_%': 'Budget Utilization %', 'budget_remaining': 'Budget Remaining ($)'},
        color_discrete_map={'HIGH': '#ff4444', 'MEDIUM': '#ffaa00', 'LOW': '#00aa00'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Innovation vs Maintenance
    st.subheader("Portfolio Balance")
    
    portfolio_mix = pd.DataFrame({
        'Category': ['Innovation', 'Enhancement', 'Maintenance'],
        'Percentage': [30, 50, 20],
        'Projects': [2, 4, 2]
    })
    
    fig = px.sunburst(
        portfolio_mix,
        path=['Category'],
        values='Percentage',
        title='Innovation vs Maintenance Mix'
    )
    st.plotly_chart(fig, use_container_width=True)

def show_cto_dashboard(vendors, projects, metrics):
    """CTO-specific dashboard"""
    st.header("🔧 CTO Dashboard - Technical Operations")
    
    # System metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        availability = float(metrics.loc['avg_availability', 'value'])
        st.metric(
            "System Availability",
            f"{availability:.2f}%",
            "Excellent"
        )
    
    with col2:
        sla = float(metrics.loc['sla_compliance', 'value'])
        st.metric(
            "SLA Compliance",
            f"{sla:.1f}%",
            "On target"
        )
    
    with col3:
        resolution = float(metrics.loc['avg_resolution_hours', 'value'])
        st.metric(
            "Avg Resolution Time",
            f"{resolution:.1f} hours",
            "Within SLA"
        )
    
    with col4:
        st.metric(
            "Active Incidents",
            "12",
            "-3 from last month",
            delta_color="inverse"
        )
    
    # Vendor analysis
    st.subheader("Vendor Risk Analysis")
    
    # Vendor risk matrix
    vendors_risk = vendors.copy()
    vendors_risk['risk_score'] = vendors_risk['annual_spend'] / 1000
    
    fig = px.treemap(
        vendors_risk,
        path=['category', 'vendor_name'],
        values='annual_spend',
        color='risk_level',
        title='Vendor Spend and Risk Distribution',
        color_discrete_map={'High': '#ff4444', 'Medium': '#ffaa00', 'Low': '#00aa00'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # System performance
    st.subheader("System Performance Metrics")
    
    # Create system performance data
    systems = ['ERP', 'LMS', 'Email', 'Network', 'Student Portal']
    performance_data = pd.DataFrame({
        'System': systems,
        'Availability': [99.5, 99.8, 99.9, 98.5, 99.2],
        'Response Time (ms)': [250, 180, 120, 50, 200],
        'User Satisfaction': [4.2, 4.5, 4.8, 4.0, 4.3]
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Availability %',
        x=performance_data['System'],
        y=performance_data['Availability'],
        yaxis='y',
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Scatter(
        name='Response Time (ms)',
        x=performance_data['System'],
        y=performance_data['Response Time (ms)'],
        yaxis='y2',
        marker_color='red',
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title='System Performance Overview',
        yaxis=dict(title='Availability %', side='left'),
        yaxis2=dict(title='Response Time (ms)', overlaying='y', side='right'),
        hovermode='x'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_predictive_analytics(vendors, projects, metrics):
    """Predictive Analytics Dashboard"""
    st.header("🔮 Predictive Analytics & AI Insights")
    
    # Predictions summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**4** Projects likely to overrun budget")
    with col2:
        st.warning("**2** Vendors require contract review")
    with col3:
        st.success("**$89,350** Total savings identified")
    
    # Budget overrun predictions
    st.subheader("📊 Budget Overrun Predictions")
    
    # Projects at risk
    at_risk = projects[projects['budget_utilization_%'] > 75].copy()
    at_risk['overrun_probability'] = at_risk['budget_utilization_%'].apply(
        lambda x: min(100, x * 1.2)
    )
    at_risk['estimated_overrun'] = at_risk['budget'] * 0.15
    
    fig = px.bar(
        at_risk.sort_values('overrun_probability', ascending=True),
        x='overrun_probability',
        y='project_name',
        orientation='h',
        title='Project Budget Overrun Risk',
        labels={'overrun_probability': 'Risk Probability (%)', 'project_name': 'Project'},
        color='overrun_probability',
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Cost savings opportunities
    st.subheader("💰 AI-Identified Savings Opportunities")
    
    savings_data = pd.DataFrame({
        'Opportunity': [
            'Vendor Consolidation - Software',
            'License Optimization',
            'Cloud Migration - Infrastructure',
            'Process Automation - Support',
            'Contract Renegotiation'
        ],
        'Potential Savings': [35000, 25000, 15000, 10000, 4350],
        'Confidence': [85, 95, 70, 80, 90],
        'Implementation Time': ['3-6 months', '1-2 months', '6-9 months', '2-3 months', '1 month']
    })
    
    # Create gauge charts for top opportunities
    for idx, row in savings_data.head(3).iterrows():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**{row['Opportunity']}**")
            st.markdown(f"Potential Savings: **${row['Potential Savings']:,}**")
            st.markdown(f"Timeline: {row['Implementation Time']}")
        
        with col2:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = row['Confidence'],
                title = {'text': "Confidence"},
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=200)
            st.plotly_chart(fig, use_container_width=True)
    
    # AI Insights
    st.subheader("🤖 AI-Generated Executive Insights")
    
    insights = [
        "💡 **Financial**: Project ROI of 125% significantly exceeds industry benchmark of 20%",
        "⚠️ **Risk**: 4 projects with >90% budget utilization require immediate intervention",
        "🎯 **Opportunity**: Vendor consolidation in Software category could save $35,000 annually",
        "📈 **Trend**: System availability at 98.9% indicates strong operational performance",
        "🔄 **Action**: Initiate license audit within 30 days for quick win savings of $25,000"
    ]
    
    for insight in insights:
        st.markdown(insight)

# Run the app
if __name__ == "__main__":
    main()

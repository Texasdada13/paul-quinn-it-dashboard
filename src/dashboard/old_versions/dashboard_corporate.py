"""
Paul Quinn College IT Dashboard - Professional Corporate Style
Features: Clean lines, muted colors, executive feel
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="PQC Executive IT Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Corporate CSS
st.markdown("""
<style>
    /* Professional Typography */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&family=Playfair+Display:wght@700&display=swap');
    
    /* Corporate Color Scheme */
    :root {
        --primary-blue: #003366;
        --secondary-gray: #4a5568;
        --accent-gold: #d4af37;
        --background: #f8f9fa;
        --card-bg: #ffffff;
    }
    
    /* Global Styles */
    .stApp {
        background-color: var(--background);
        font-family: 'Roboto', sans-serif;
    }
    
    /* Executive Header */
    h1 {
        color: var(--primary-blue);
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem !important;
        font-weight: 700;
        text-align: left;
        border-bottom: 3px solid var(--accent-gold);
        padding-bottom: 1rem;
        margin-bottom: 2rem;
    }
    
    h2, h3 {
        color: var(--primary-blue);
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    
    /* Professional Metric Cards */
    [data-testid="metric-container"] {
        background: var(--card-bg);
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--primary-blue);
        font-weight: 700;
        font-size: 2rem !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-label"] {
        color: var(--secondary-gray);
        font-weight: 300;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.8rem !important;
    }
    
    /* Sidebar - Executive Style */
    .css-1d391kg {
        background-color: var(--primary-blue);
    }
    
    .css-1d391kg .stRadio label {
        color: white !important;
    }
    
    /* Tables - Board Room Style */
    .dataframe {
        border: none !important;
        font-size: 0.9rem;
    }
    
    .dataframe th {
        background-color: var(--primary-blue) !important;
        color: white !important;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.8rem !important;
    }
    
    .dataframe td {
        border-bottom: 1px solid #e2e8f0 !important;
    }
    
    /* Executive Summary Box */
    .executive-summary {
        background: linear-gradient(135deg, var(--primary-blue) 0%, #004080 100%);
        color: white;
        padding: 2rem;
        border-radius: 4px;
        margin-bottom: 2rem;
    }
    
    /* Professional Alerts */
    .stAlert {
        border-left: 4px solid var(--accent-gold);
        background-color: var(--card-bg);
        border-radius: 0;
    }
</style>
""", unsafe_allow_html=True)

# Data loading function
@st.cache_data
def load_data():
    try:
        vendors = pd.read_csv("clean_vendors.csv")
        projects = pd.read_csv("clean_projects.csv")
        metrics = pd.read_csv("it_effectiveness_metrics.csv", index_col=0)
        return vendors, projects, metrics
    except:
        try:
            vendors = pd.read_csv("02_Data/processed/clean_vendors.csv")
            projects = pd.read_csv("02_Data/processed/clean_projects.csv")
            metrics = pd.read_csv("02_Data/processed/it_effectiveness_metrics.csv", index_col=0)
            return vendors, projects, metrics
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None, None, None

def main():
    # Professional Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("# Executive IT Dashboard")
        st.markdown("**Paul Quinn College** | Information Technology Division")
    with col2:
        st.markdown(f"<div style='text-align: right; color: #4a5568; padding-top: 2rem;'>{datetime.now().strftime('%B %Y')}</div>", unsafe_allow_html=True)
    
    # Load data
    vendors, projects, metrics = load_data()
    if vendors is None:
        return
    
    # Executive Summary Section
    st.markdown("""
    <div class="executive-summary">
        <h2 style="color: white; margin-top: 0;">Executive Summary</h2>
        <p style="font-size: 1.1rem; line-height: 1.8;">
        The IT portfolio demonstrates strong fiscal discipline with spending at 0.86% of revenue, 
        significantly below the 3-5% industry benchmark. Project ROI of 125% exceeds targets, 
        while system availability maintains 98.9% uptime.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Performance Indicators
    st.markdown("### Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("TOTAL SPEND", f"${vendors['annual_spend'].sum():,.0f}")
    
    with col2:
        st.metric("ROI", f"{float(metrics.loc['project_roi', 'value']):.0f}%")
    
    with col3:
        st.metric("EFFICIENCY", f"{float(metrics.loc['budget_efficiency', 'value']):.0f}%")
    
    with col4:
        st.metric("AVAILABILITY", f"{float(metrics.loc['avg_availability', 'value']):.1f}%")
    
    with col5:
        high_risk = len(projects[projects['risk_flag'] == 'HIGH'])
        st.metric("AT RISK", f"{high_risk}")
    
    # Professional Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Corporate Pie Chart
        fig = px.pie(
            vendors,
            values='annual_spend',
            names='category',
            title='Budget Allocation by Category',
            color_discrete_sequence=['#003366', '#004080', '#0059b3', '#007acc', '#4da6ff']
        )
        
        fig.update_layout(
            font=dict(family="Roboto", size=12),
            title_font_size=16,
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Executive Bar Chart
        dept_spend = projects.groupby('department')['budget'].sum().sort_values(ascending=True)
        
        fig = go.Figure(data=[
            go.Bar(
                x=dept_spend.values,
                y=dept_spend.index,
                orientation='h',
                marker_color='#003366'
            )
        ])
        
        fig.update_layout(
            title='Departmental IT Investment',
            xaxis_title='Budget ($)',
            font=dict(family="Roboto", size=12),
            title_font_size=16,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Board-Ready Tables
    st.markdown("### Portfolio Details")
    
    tab1, tab2, tab3 = st.tabs(["Project Status", "Vendor Analysis", "Risk Assessment"])
    
    with tab1:
        project_summary = projects[['project_name', 'department', 'budget', 'spent_to_date', 'status', 'risk_flag']]
        st.dataframe(
            project_summary.style.format({
                'budget': '${:,.0f}',
                'spent_to_date': '${:,.0f}'
            }),
            use_container_width=True
        )
    
    with tab2:
        vendor_summary = vendors[['vendor_name', 'category', 'annual_spend', 'risk_level']]
        st.dataframe(
            vendor_summary.style.format({
                'annual_spend': '${:,.0f}'
            }),
            use_container_width=True
        )
    
    with tab3:
        risk_items = pd.concat([
            projects[projects['risk_flag'] == 'HIGH'][['project_name', 'risk_flag']].rename(columns={'project_name': 'Item'}),
            vendors[vendors['risk_level'] == 'High'][['vendor_name', 'risk_level']].rename(columns={'vendor_name': 'Item', 'risk_level': 'risk_flag'})
        ])
        st.dataframe(risk_items, use_container_width=True)

if __name__ == "__main__":
    main()

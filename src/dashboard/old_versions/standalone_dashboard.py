"""
Paul Quinn College IT Analytics Suite - Standalone Modern Dashboard
No external dependencies required - perfect for demo
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="PQC Analytics Suite | Premium",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern color palette
COLORS = {
    'primary': '#2563eb',
    'primary_dark': '#1e40af',
    'secondary': '#7c3aed',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'dark': '#0f172a',
    'light': '#f8fafc',
    'gray': '#64748b'
}

# Modern CSS styling
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }}
    
    /* Main container */
    .main {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }}
    
    /* Header */
    .main-header {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInDown 0.8s ease;
    }}
    
    .sub-header {{
        color: {COLORS['dark']};
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1.5rem 0;
        position: relative;
        padding-left: 1rem;
    }}
    
    .sub-header:before {{
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 24px;
        background: linear-gradient(180deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        border-radius: 2px;
    }}
    
    /* Metric Cards */
    div[data-testid="metric-container"] {{
        background: linear-gradient(145deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.15),
            inset 0 0 0 1px rgba(255,255,255,0.5);
        transition: all 0.3s ease;
    }}
    
    div[data-testid="metric-container"]:hover {{
        transform: translateY(-4px);
        box-shadow: 
            0 12px 48px rgba(31, 38, 135, 0.25),
            inset 0 0 0 1px rgba(255,255,255,0.7);
    }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['dark']} 0%, #1e293b 100%);
    }}
    
    section[data-testid="stSidebar"] h3 {{
        color: white !important;
    }}
    
    section[data-testid="stSidebar"] p {{
        color: rgba(255, 255, 255, 0.8) !important;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 0.25rem;
        gap: 0.5rem;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: white !important;
        color: {COLORS['primary']} !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
    }}
    
    /* Animations */
    @keyframes fadeInDown {{
        from {{
            opacity: 0;
            transform: translateY(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
    }}
    
    .status-active {{
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: {COLORS['success']};
        margin-right: 0.5rem;
    }}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_persona' not in st.session_state:
    st.session_state.current_persona = 'CFO'

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h2 style='color: white; margin: 0;'>🎓</h2>
            <h3 style='color: white; margin: 0; font-weight: 700;'>Paul Quinn College</h3>
            <p style='color: rgba(255,255,255,0.8); margin: 0.5rem 0;'>IT Analytics Suite</p>
            <span class='badge'>PREMIUM EDITION</span>
        </div>
        <hr style='border: 1px solid rgba(255,255,255,0.2); margin: 2rem 0;'>
    """, unsafe_allow_html=True)
    
    # Persona selection
    persona = st.selectbox(
        "📌 Select Dashboard View",
        ["CFO - Financial Steward", "CIO - Strategic Partner", "CTO - Technology Operator", 
         "Project Manager View", "HBCU Institutional View"]
    )
    
    # Quick stats
    st.markdown("### 📊 System Status")
    st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;'>
            <span class='status-active'></span>
            <span style='color: white; font-weight: 500;'>All Systems Operational</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("📊 Report", use_container_width=True):
            st.success("Generating...")
    
    # HBCU Stats
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    st.markdown("### 🏛️ HBCU Metrics")
    
    metrics_data = [
        ("Students", "5,800", "↑ 3.2%"),
        ("Cost/Student", "$8,224", "↓ $426"),
        ("Compliance", "94%", "↑ 2%"),
        ("Tech Grad", "78%", "↑ 5%")
    ]
    
    for label, value, delta in metrics_data:
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); padding: 0.75rem; margin: 0.5rem 0; border-radius: 8px;'>
                <div style='color: rgba(255,255,255,0.7); font-size: 0.75rem;'>{label}</div>
                <div style='color: white; font-size: 1.25rem; font-weight: 600;'>{value}</div>
                <div style='color: #10b981; font-size: 0.875rem;'>{delta}</div>
            </div>
        """, unsafe_allow_html=True)

# Main content
st.markdown("<h1 class='main-header'>🎓 Paul Quinn College Analytics Suite</h1>", unsafe_allow_html=True)

# CFO Dashboard
if persona == "CFO - Financial Steward":
    st.markdown("<h2 class='sub-header'>Financial Overview & Optimization</h2>", unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total IT Budget", "$5.0M", "+2.9%", help="Year-over-year change")
    with col2:
        st.metric("YTD Spend", "$1.9M", "-3%", help="38% of budget")
    with col3:
        st.metric("Cost Savings", "$340K", "+12%", help="Through optimization")
    with col4:
        st.metric("Contracts at Risk", "13", delta_color="inverse", help="Expiring < 90 days")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Budget Analysis", "📃 Contracts", "🏛️ Compliance", "📈 Benchmarking"])
    
    with tab1:
        st.markdown("<h3 class='sub-header'>Budget vs Actual Analysis</h3>", unsafe_allow_html=True)
        
        # Budget data
        categories = ['IT Portfolio', 'Operations', 'Academic Tech', 'Cloud Services', 
                     'Cybersecurity', 'Student Services', 'Infrastructure']
        budget = [850000, 620000, 780000, 450000, 320000, 550000, 930000]
        actual = [920000, 580000, 810000, 490000, 290000, 530000, 880000]
        
        # Create chart
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Budget', x=categories, y=budget, marker_color=COLORS['primary']))
        fig.add_trace(go.Bar(name='Actual', x=categories, y=actual, marker_color=COLORS['secondary']))
        
        # Variance line
        variance = [(a-b)/b*100 for a, b in zip(actual, budget)]
        fig.add_trace(go.Scatter(
            name='Variance %', x=categories, y=variance,
            mode='lines+markers', marker=dict(size=10),
            line=dict(color=COLORS['warning'], width=2),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Budget Variance by Category",
            yaxis=dict(title="Amount ($)"),
            yaxis2=dict(title="Variance (%)", overlaying="y", side="right"),
            hovermode='x unified',
            plot_bgcolor='white',
            height=400,
            showlegend=True,
            legend=dict(orientation="h", y=1.1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Total Budget:** ${sum(budget):,}")
        with col2:
            st.success(f"**Total Actual:** ${sum(actual):,}")
        with col3:
            total_var = (sum(actual) - sum(budget))/sum(budget)*100
            st.warning(f"**Variance:** {total_var:+.1f}%")
    
    with tab2:
        st.markdown("<h3 class='sub-header'>Contract Management</h3>", unsafe_allow_html=True)
        
        # Contract data
        contracts = pd.DataFrame({
            'Vendor': ['Microsoft', 'Oracle', 'AWS', 'Salesforce', 'Adobe', 'Zoom'],
            'Value': [450000, 320000, 680000, 290000, 180000, 95000],
            'Days Until Expiry': [45, 92, 180, 30, 267, 15],
            'Risk': ['High', 'Medium', 'Low', 'High', 'Low', 'Critical']
        })
        
        # Risk gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = len(contracts[contracts['Days Until Expiry'] < 90]),
            title = {'text': "Contracts at Risk"},
            gauge = {
                'axis': {'range': [None, 10]},
                'bar': {'color': COLORS['warning']},
                'steps': [
                    {'range': [0, 3], 'color': '#e8f5e9'},
                    {'range': [3, 6], 'color': '#fff3e0'},
                    {'range': [6, 10], 'color': '#ffebee'}
                ],
            }
        ))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(contracts, use_container_width=True)
    
    with tab3:
        st.markdown("<h3 class='sub-header'>Grant Compliance</h3>", unsafe_allow_html=True)
        
        # Compliance scores
        grants = ['Title III', 'Title IV', 'HBCU Excellence', 'NSF Grant', 'State Funding']
        scores = [96, 94, 98, 91, 89]
        
        fig = go.Figure()
        for grant, score in zip(grants, scores):
            color = COLORS['success'] if score >= 95 else COLORS['warning'] if score >= 90 else COLORS['danger']
            fig.add_trace(go.Bar(
                x=[score], y=[grant], orientation='h',
                marker=dict(color=color), showlegend=False
            ))
        
        fig.update_layout(
            title="Compliance Scores by Grant",
            xaxis=dict(range=[0, 100], title="Score %"),
            yaxis=dict(title=""),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("<h3 class='sub-header'>HBCU Benchmarking</h3>", unsafe_allow_html=True)
        
        # Radar chart
        categories = ['IT Spend/Student', 'Cloud Adoption', 'Digital Maturity', 'Cost Efficiency', 'Innovation']
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[8.5, 7.8, 7.2, 8.5, 6.9],
            theta=categories,
            fill='toself',
            name='Paul Quinn',
            marker_color=COLORS['primary']
        ))
        fig.add_trace(go.Scatterpolar(
            r=[7.2, 6.5, 6.8, 7.9, 6.2],
            theta=categories,
            fill='toself',
            name='HBCU Average',
            marker_color=COLORS['gray']
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# CIO Dashboard
elif persona == "CIO - Strategic Partner":
    st.markdown("<h2 class='sub-header'>Strategic IT Portfolio Management</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Digital Transformation", "65%", "+15%")
    with col2:
        st.metric("Project Success", "87%", "+5%")
    with col3:
        st.metric("Innovation Index", "7.8/10", "+0.6")
    with col4:
        st.metric("Business Alignment", "92%", "+3%")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Portfolio", "💡 Innovation", "📊 Performance"])
    
    with tab1:
        # Sunburst chart
        fig = go.Figure(go.Sunburst(
            labels=['Portfolio', 'Run', 'Grow', 'Transform',
                   'Operations', 'Maintenance', 'Enhancements', 'Innovation'],
            parents=['', 'Portfolio', 'Portfolio', 'Portfolio',
                    'Run', 'Run', 'Grow', 'Transform'],
            values=[0, 45, 35, 20, 25, 20, 35, 20],
            branchvalues="total",
            marker=dict(colors=[COLORS['primary'], COLORS['gray'], 
                              COLORS['warning'], COLORS['success']])
        ))
        fig.update_layout(height=400, margin=dict(t=50, b=0))
        st.plotly_chart(fig, use_container_width=True)

# CTO Dashboard
elif persona == "CTO - Technology Operator":
    st.markdown("<h2 class='sub-header'>Technical Operations & Infrastructure</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("System Uptime", "99.8%", "+0.2%")
    with col2:
        st.metric("Incident Resolution", "2.4 hrs", "-0.6 hrs")
    with col3:
        st.metric("Cloud Utilization", "78%", "+5%")
    with col4:
        st.metric("Security Score", "A-", "↑")
    
    tab1, tab2, tab3 = st.tabs(["🖥️ Infrastructure", "☁️ Cloud", "🔒 Security"])
    
    with tab1:
        # Performance metrics
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        cpu = np.random.normal(65, 10, 30).clip(0, 100)
        memory = np.random.normal(72, 8, 30).clip(0, 100)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=cpu, name='CPU', line=dict(color=COLORS['primary'])))
        fig.add_trace(go.Scatter(x=dates, y=memory, name='Memory', line=dict(color=COLORS['secondary'])))
        
        fig.update_layout(
            title="System Performance (30 days)",
            xaxis_title="Date",
            yaxis_title="Usage %",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# PM Dashboard
elif persona == "Project Manager View":
    st.markdown("<h2 class='sub-header'>Project Management Dashboard</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Projects", "8", "")
    with col2:
        st.metric("On Schedule", "87%", "+5%")
    with col3:
        st.metric("Resource Utilization", "92%", "+3%")
    with col4:
        st.metric("Portfolio Health", "8.1/10", "+0.3")
    
    # Project timeline
    projects = pd.DataFrame({
        'Project': ['Student Portal', 'Cloud Migration', 'Security Update', 'LMS Upgrade'],
        'Progress': [75, 45, 90, 30],
        'Status': ['On Track', 'At Risk', 'On Track', 'Planning']
    })
    
    fig = go.Figure()
    colors = {'On Track': COLORS['success'], 'At Risk': COLORS['warning'], 'Planning': COLORS['gray']}
    
    for _, row in projects.iterrows():
        fig.add_trace(go.Bar(
            x=[row['Progress']],
            y=[row['Project']],
            orientation='h',
            marker_color=colors[row['Status']],
            name=row['Status'],
            showlegend=False
        ))
    
    fig.update_layout(
        title="Project Progress",
        xaxis=dict(range=[0, 100], title="Completion %"),
        yaxis=dict(title=""),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

# HBCU View
else:
    st.markdown("<h2 class='sub-header'>HBCU Institutional Analytics</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Mission Alignment", "94%", "+3%")
    with col2:
        st.metric("Student Success", "78%", "+5%")
    with col3:
        st.metric("Grant Performance", "91%", "+2%")
    with col4:
        st.metric("Tech Equity", "86%", "+7%")
    
    st.info("Complete HBCU institutional metrics and benchmarking analysis would be displayed here.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #64748b; padding: 2rem 0;'>
        <p style='font-weight: 600;'>Paul Quinn College IT Analytics Suite - Premium Edition</p>
        <p style='font-size: 0.875rem;'>© 2024 | Built for Excellence in HBCU Education</p>
    </div>
""", unsafe_allow_html=True)
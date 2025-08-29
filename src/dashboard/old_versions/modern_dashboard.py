"""
Paul Quinn College IT Analytics Suite - Modern Premium Dashboard
Enhanced with professional design, animations, and advanced visualizations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
import os
import sys

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modules with error handling
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

# Page configuration
st.set_page_config(
    page_title="PQC Analytics Suite | Premium",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern color palette
COLORS = {
    'primary': '#2563eb',      # Royal blue
    'primary_dark': '#1e40af',
    'secondary': '#7c3aed',    # Purple
    'success': '#10b981',      # Emerald
    'warning': '#f59e0b',      # Amber
    'danger': '#ef4444',       # Red
    'dark': '#0f172a',         # Slate 900
    'light': '#f8fafc',        # Slate 50
    'gray': '#64748b',         # Slate 500
    'gradient_start': '#667eea',
    'gradient_end': '#764ba2'
}

# Enhanced Custom CSS with modern design
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }}
    
    /* Main container background */
    .main {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }}
    
    /* Header Styles */
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
    
    /* Metric Cards - Glassmorphism */
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
    
    /* Metric values styling */
    div[data-testid="metric-container"] > div {{
        gap: 0.5rem;
    }}
    
    div[data-testid="metric-container"] label {{
        color: {COLORS['gray']} !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {{
        font-weight: 700 !important;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['dark']} 0%, #1e293b 100%);
        backdrop-filter: blur(10px);
    }}
    
    section[data-testid="stSidebar"] .block-container {{
        padding-top: 2rem;
    }}
    
    section[data-testid="stSidebar"] h3 {{
        color: white !important;
        font-weight: 600;
    }}
    
    section[data-testid="stSidebar"] p {{
        color: rgba(255, 255, 255, 0.8) !important;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox label {{
        color: rgba(255, 255, 255, 0.9) !important;
    }}
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 0.25rem;
        gap: 0.5rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        color: {COLORS['gray']};
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: rgba(255, 255, 255, 0.8);
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
    
    /* Expander Styling */
    .streamlit-expanderHeader {{
        background: linear-gradient(145deg, #f8fafc, #f1f5f9);
        border-radius: 8px;
        font-weight: 500;
    }}
    
    /* Badge Styling */
    .badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }}
    
    .badge-premium {{
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
        animation: pulse 2s ease infinite;
    }}
    
    .badge-success {{
        background: linear-gradient(135deg, {COLORS['success']} 0%, #059669 100%);
        color: white;
    }}
    
    .badge-info {{
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
    }}
    
    /* Status Indicators */
    .status-indicator {{
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 0.5rem;
        animation: pulse 2s ease infinite;
    }}
    
    .status-active {{
        background: {COLORS['success']};
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
    }}
    
    .status-warning {{
        background: {COLORS['warning']};
        box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.7);
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
    
    @keyframes pulse {{
        0% {{
            box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.7);
        }}
        70% {{
            box-shadow: 0 0 0 10px rgba(37, 99, 235, 0);
        }}
        100% {{
            box-shadow: 0 0 0 0 rgba(37, 99, 235, 0);
        }}
    }}
    
    @keyframes slideIn {{
        from {{
            transform: translateX(-100%);
            opacity: 0;
        }}
        to {{
            transform: translateX(0);
            opacity: 1;
        }}
    }}
    
    /* Chart container styling */
    .plot-container {{
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }}
    
    /* Info boxes */
    .stAlert {{
        background: linear-gradient(145deg, #eff6ff, #dbeafe);
        border-left: 4px solid {COLORS['primary']};
        border-radius: 8px;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        color: {COLORS['gray']};
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 1px solid #e5e7eb;
    }}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_persona' not in st.session_state:
    st.session_state.current_persona = 'CFO'

if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Initialize HBCU integrator
if HBCU_INTEGRATION_AVAILABLE:
    hbcu_integrator = HBCUMetricsIntegrator()
else:
    hbcu_integrator = None

# Sidebar with modern styling
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h2 style='color: white; margin: 0;'>🎓</h2>
            <h3 style='color: white; margin: 0; font-weight: 700;'>Paul Quinn College</h3>
            <p style='color: rgba(255,255,255,0.8); margin: 0.5rem 0;'>IT Analytics Suite</p>
            <span class='badge badge-premium'>PREMIUM EDITION</span>
        </div>
        <hr style='border: 1px solid rgba(255,255,255,0.2); margin: 2rem 0;'>
    """, unsafe_allow_html=True)
    
    # Persona selection with icon
    persona_options = {
        "CFO - Financial Steward": "💰",
        "CIO - Strategic Partner": "🎯", 
        "CTO - Technology Operator": "⚙️",
        "Project Manager View": "📊",
        "HBCU Institutional View": "🏛️"
    }
    
    selected_persona = st.selectbox(
        "📌 Select Dashboard View",
        list(persona_options.keys()),
        help="Choose your role-specific dashboard"
    )
    
    persona_icon = persona_options[selected_persona]
    persona_key = selected_persona.split(' - ')[0].lower()
    
    # Metrics Status with animation
    st.markdown("### 📊 System Status")
    
    if METRICS_AVAILABLE:
        available_metrics = metric_registry.get_available_metrics(persona_key) if persona_key != 'project' else []
        status_color = COLORS['success'] if len(available_metrics) > 0 else COLORS['warning']
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;'>
                <span class='status-indicator status-active'></span>
                <span style='color: white; font-weight: 500;'>{len(available_metrics)} Metrics Active</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;'>
                <span class='status-indicator status-warning'></span>
                <span style='color: #fbbf24; font-weight: 500;'>System Loading...</span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    
    # Quick Actions with modern buttons
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("📊 Report", use_container_width=True):
            st.success("Generating...")
    
    # HBCU Quick Stats with cards
    if HBCU_INTEGRATION_AVAILABLE and hbcu_integrator:
        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
        st.markdown("### 🏛️ HBCU Metrics")
        
        metrics_data = [
            ("Students", "5,800", "↑ 3.2%", COLORS['success']),
            ("Cost/Student", "$8,224", "↓ $426", COLORS['success']),
            ("Compliance", "94%", "↑ 2%", COLORS['warning']),
            ("Tech Grad", "78%", "↑ 5%", COLORS['success'])
        ]
        
        for label, value, delta, color in metrics_data:
            st.markdown(f"""
                <div style='background: rgba(255,255,255,0.1); padding: 0.75rem; margin: 0.5rem 0; border-radius: 8px; border-left: 3px solid {color};'>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.75rem; text-transform: uppercase;'>{label}</div>
                    <div style='color: white; font-size: 1.25rem; font-weight: 600;'>{value}</div>
                    <div style='color: {color}; font-size: 0.875rem;'>{delta}</div>
                </div>
            """, unsafe_allow_html=True)

# Main content area
st.markdown(f"""
    <h1 class='main-header'>
        {persona_icon} Paul Quinn College Analytics Suite
    </h1>
""", unsafe_allow_html=True)

# Function to create modern metric cards
def create_metric_card(title, value, delta, delta_color, icon="📊"):
    return f"""
        <div style='background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);'>
            <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                <span style='font-size: 1.5rem; margin-right: 0.5rem;'>{icon}</span>
                <span style='color: {COLORS['gray']}; font-size: 0.875rem; font-weight: 500;'>{title}</span>
            </div>
            <div style='font-size: 2rem; font-weight: 700; color: {COLORS['dark']};'>{value}</div>
            <div style='color: {delta_color}; font-size: 0.875rem; font-weight: 500; margin-top: 0.25rem;'>{delta}</div>
        </div>
    """

# Display content based on persona
if selected_persona == "CFO - Financial Steward":
    st.markdown("<h2 class='sub-header'>Financial Overview & Optimization</h2>", unsafe_allow_html=True)
    
    # Modern KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    # Generate sample data for visualization
    if METRICS_AVAILABLE and persona_key == 'cfo':
        try:
            budget_data, _ = cfo_metrics.get_budget_variance_data()
            contract_data, _ = cfo_metrics.get_contract_alerts()
            
            if budget_data is not None:
                total_budget = budget_data['Initial Budget'].sum()
                total_actual = budget_data['Actual Spend'].sum()
                variance_pct = ((total_actual - total_budget) / total_budget * 100) if total_budget > 0 else 0
            else:
                total_budget = 5000000
                total_actual = 4759640
                variance_pct = -4.8
            
            contracts_at_risk = len(contract_data[contract_data['Days Until Expiry'] < 90]) if contract_data is not None else 13
        except:
            total_budget = 5000000
            total_actual = 4759640
            variance_pct = -4.8
            contracts_at_risk = 13
    else:
        total_budget = 5000000
        total_actual = 4759640
        variance_pct = -4.8
        contracts_at_risk = 13
    
    with col1:
        st.metric("Total IT Budget", f"${total_budget/1000000:.1f}M", f"{variance_pct:+.1f}%")
    with col2:
        st.metric("YTD Spend", f"${total_actual/1000000:.1f}M", "-3%")
    with col3:
        st.metric("Cost Savings", "$340K", "+12%")
    with col4:
        st.metric("Contracts at Risk", contracts_at_risk, delta_color="inverse")
    
    # Create modern tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Budget Analysis", "📃 Contracts", "🏛️ Compliance", "📈 Benchmarking"])
    
    with tab1:
        st.markdown("<h3 class='sub-header'>Budget vs Actual Analysis with Variance Alerts</h3>", unsafe_allow_html=True)
        
        # Create sample budget data
        categories = ['IT Project Portfolio', 'Operations', 'Academic Tech', 'Cloud Services', 
                     'Cybersecurity', 'Student Services', 'Infrastructure']
        budget_values = [850000, 620000, 780000, 450000, 320000, 550000, 930000]
        actual_values = [920000, 580000, 810000, 490000, 290000, 530000, 880000]
        
        # Create modern bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Budget',
            x=categories,
            y=budget_values,
            marker_color=COLORS['primary'],
            marker_line_color='white',
            marker_line_width=2,
            opacity=0.9
        ))
        
        fig.add_trace(go.Bar(
            name='Actual',
            x=categories,
            y=actual_values,
            marker_color=COLORS['secondary'],
            marker_line_color='white',
            marker_line_width=2,
            opacity=0.9
        ))
        
        # Calculate variance for color coding
        variances = [(a-b)/b*100 for a, b in zip(actual_values, budget_values)]
        colors = [COLORS['danger'] if v > 5 else COLORS['warning'] if v > 0 else COLORS['success'] for v in variances]
        
        fig.add_trace(go.Scatter(
            name='Variance %',
            x=categories,
            y=variances,
            mode='lines+markers',
            marker=dict(size=10, color=colors),
            line=dict(color=COLORS['gray'], width=2, dash='dash'),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Budget Variance by Category",
            xaxis_tickangle=-45,
            yaxis=dict(title="Amount ($)", side="left"),
            yaxis2=dict(title="Variance (%)", overlaying="y", side="right"),
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter"),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=80, b=80),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Variance Summary Cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Total Budget:** ${sum(budget_values):,}")
        with col2:
            st.success(f"**Total Actual:** ${sum(actual_values):,}")
        with col3:
            total_var = (sum(actual_values) - sum(budget_values))/sum(budget_values)*100
            if total_var > 0:
                st.warning(f"**Overall Variance:** {total_var:+.1f}%")
            else:
                st.success(f"**Overall Variance:** {total_var:+.1f}%")
    
    with tab2:
        st.markdown("<h3 class='sub-header'>Contract Management Dashboard</h3>", unsafe_allow_html=True)
        
        # Sample contract data
        contracts_df = pd.DataFrame({
            'Vendor': ['Microsoft', 'Oracle', 'AWS', 'Salesforce', 'Adobe', 'Zoom'],
            'Contract Value': [450000, 320000, 680000, 290000, 180000, 95000],
            'Days Until Expiry': [45, 92, 180, 30, 267, 15],
            'Risk Level': ['High', 'Medium', 'Low', 'High', 'Low', 'Critical']
        })
        
        # Create gauge chart for contract risk
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = contracts_df[contracts_df['Days Until Expiry'] < 90].shape[0],
            title = {'text': "Contracts Requiring Attention"},
            delta = {'reference': 5},
            gauge = {
                'axis': {'range': [None, 10]},
                'bar': {'color': COLORS['warning']},
                'steps': [
                    {'range': [0, 3], 'color': COLORS['success']},
                    {'range': [3, 6], 'color': COLORS['warning']},
                    {'range': [6, 10], 'color': COLORS['danger']}
                ],
                'threshold': {
                    'line': {'color': COLORS['danger'], 'width': 4},
                    'thickness': 0.75,
                    'value': 8
                }
            }
        ))
        
        fig_gauge.update_layout(height=250, margin=dict(t=50, b=0))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Contract details table
        st.dataframe(
            contracts_df.style.apply(lambda x: ['background-color: #fee2e2' if v < 60 else '' for v in contracts_df['Days Until Expiry']], axis=0),
            use_container_width=True
        )
    
    with tab3:
        st.markdown("<h3 class='sub-header'>Grant Compliance Tracking</h3>", unsafe_allow_html=True)
        
        # Compliance metrics
        compliance_data = {
            'Title III': 96,
            'Title IV': 94,
            'HBCU Excellence': 98,
            'NSF Grant': 91,
            'State Funding': 89
        }
        
        fig_compliance = go.Figure()
        
        for grant, score in compliance_data.items():
            color = COLORS['success'] if score >= 95 else COLORS['warning'] if score >= 90 else COLORS['danger']
            fig_compliance.add_trace(go.Bar(
                x=[score],
                y=[grant],
                orientation='h',
                marker=dict(color=color, line=dict(color='white', width=2)),
                name=grant,
                showlegend=False
            ))
        
        fig_compliance.update_layout(
            title="Grant Compliance Scores",
            xaxis=dict(range=[0, 100], title="Compliance %"),
            yaxis=dict(title=""),
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_compliance, use_container_width=True)
        
        # Compliance summary
        avg_compliance = np.mean(list(compliance_data.values()))
        st.success(f"**Average Compliance Score:** {avg_compliance:.1f}% - Excellent")
    
    with tab4:
        st.markdown("<h3 class='sub-header'>HBCU Peer Benchmarking</h3>", unsafe_allow_html=True)
        
        # Benchmark data
        benchmark_data = pd.DataFrame({
            'Metric': ['IT Spend per Student', 'Cloud Adoption %', 'Digital Maturity', 'Cost Efficiency'],
            'Paul Quinn': [1420, 78, 7.2, 8.5],
            'HBCU Average': [1650, 65, 6.8, 7.9],
            'Top Quartile': [1350, 85, 8.1, 9.2]
        })
        
        fig_radar = go.Figure()
        
        categories = benchmark_data['Metric'].tolist()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=benchmark_data['Paul Quinn'],
            theta=categories,
            fill='toself',
            name='Paul Quinn',
            marker_color=COLORS['primary']
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=benchmark_data['HBCU Average'],
            theta=categories,
            fill='toself',
            name='HBCU Average',
            marker_color=COLORS['gray']
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=benchmark_data['Top Quartile'],
            theta=categories,
            fill='toself',
            name='Top Quartile',
            marker_color=COLORS['success']
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 10])
            ),
            showlegend=True,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)

elif selected_persona == "CIO - Strategic Partner":
    st.markdown("<h2 class='sub-header'>Strategic IT Portfolio Management</h2>", unsafe_allow_html=True)
    
    # CIO Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Digital Transformation", "65%", "+15%")
    with col2:
        st.metric("Project Success Rate", "87%", "+5%")
    with col3:
        st.metric("Innovation Index", "7.8/10", "+0.6")
    with col4:
        st.metric("Business Alignment", "92%", "+3%")
    
    # Strategic tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Strategic Portfolio", "💡 Innovation", "📊 Performance"])
    
    with tab1:
        st.markdown("<h3 class='sub-header'>IT Portfolio Distribution</h3>", unsafe_allow_html=True)
        
        # Portfolio sunburst chart
        fig = go.Figure(go.Sunburst(
            labels=['IT Portfolio', 'Run', 'Grow', 'Transform',
                   'Operations', 'Maintenance', 'Infrastructure',
                   'Enhancements', 'New Features', 'Integrations',
                   'Digital Innovation', 'AI/ML Projects', 'Student Experience'],
            parents=['', 'IT Portfolio', 'IT Portfolio', 'IT Portfolio',
                    'Run', 'Run', 'Run',
                    'Grow', 'Grow', 'Grow',
                    'Transform', 'Transform', 'Transform'],
            values=[0, 45, 35, 20,
                   20, 15, 10,
                   15, 12, 8,
                   8, 7, 5],
            branchvalues="total",
            marker=dict(colors=[COLORS['primary'], COLORS['gray'], COLORS['warning'], COLORS['success']]),
        ))
        
        fig.update_layout(
            height=400,
            margin=dict(t=50, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig, use_container_width=True)

elif selected_persona == "CTO - Technology Operator":
    st.markdown("<h2 class='sub-header'>Technical Operations & Infrastructure</h2>", unsafe_allow_html=True)
    
    # CTO Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("System Uptime", "99.8%", "+0.2%")
    with col2:
        st.metric("Incident Resolution", "2.4 hrs", "-0.6 hrs")
    with col3:
        st.metric("Cloud Utilization", "78%", "+5%")
    with col4:
        st.metric("Security Score", "A-", "↑")
    
    # Technical tabs
    tab1, tab2, tab3 = st.tabs(["🖥️ Infrastructure", "☁️ Cloud Services", "🔒 Security"])
    
    with tab1:
        st.markdown("<h3 class='sub-header'>Infrastructure Performance</h3>", unsafe_allow_html=True)
        
        # Generate time series data
        dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
        performance_data = pd.DataFrame({
            'Date': dates,
            'CPU Usage': np.random.normal(65, 10, 90).clip(0, 100),
            'Memory Usage': np.random.normal(72, 8, 90).clip(0, 100),
            'Network Latency': np.random.normal(25, 5, 90).clip(0, 100)
        })
        
        fig = go.Figure()
        
        for metric in ['CPU Usage', 'Memory Usage', 'Network Latency']:
            fig.add_trace(go.Scatter(
                x=performance_data['Date'],
                y=performance_data[metric],
                mode='lines',
                name=metric,
                line=dict(width=2)
            ))
        
        fig.update_layout(
            title="System Performance Metrics",
            xaxis_title="Date",
            yaxis_title="Usage %",
            hovermode='x unified',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig, use_container_width=True)

elif selected_persona == "Project Manager View":
    st.markdown("<h2 class='sub-header'>Project Management Dashboard</h2>", unsafe_allow_html=True)
    
    # PM Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Projects", "8", "")
    with col2:
        st.metric("On Schedule", "87%", "+5%")
    with col3:
        st.metric("Resource Utilization", "92%", "+3%")
    with col4:
        st.metric("Portfolio Health", "8.1/10", "+0.3")
    
    # Project tabs
    st.info("Project Management metrics visualization would display here when PM modules are connected.")

elif selected_persona == "HBCU Institutional View":
    st.markdown("<h2 class='sub-header'>HBCU Institutional Analytics</h2>", unsafe_allow_html=True)
    
    if HBCU_INTEGRATION_AVAILABLE and hbcu_integrator:
        hbcu_integrator.render_institutional_hbcu_view()
    else:
        st.info("HBCU institutional metrics would display here when integration module is available.")

# Footer
st.markdown("---")
st.markdown("""
    <div class='footer'>
        <p style='font-weight: 600; color: #1e293b;'>Paul Quinn College IT Analytics Suite - Premium Edition</p>
        <p style='font-size: 0.875rem;'>Powered by Advanced Analytics | Real-time Metrics | © 2024</p>
    </div>
""", unsafe_allow_html=True)
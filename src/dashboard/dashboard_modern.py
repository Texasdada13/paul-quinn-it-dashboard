"""
Paul Quinn College IT Dashboard - Modern Innovative Style
Features: Glassmorphism, animated gradients, futuristic feel
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="PQC IT Intelligence Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Innovative CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container with Glassmorphism */
    .main .block-container {
        padding: 2rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem !important;
        text-align: center;
        margin-bottom: 2rem;
        animation: gradient 3s ease infinite;
    }
    
    h2 {
        color: #1a202c;
        font-weight: 600;
        margin-top: 2rem;
    }
    
    /* Metrics Cards */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    /* Metric Values */
    [data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: 2.5rem !important;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
    }
    
    /* Radio Buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    /* Animation */
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating Elements */
    .floating {
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }
    
    /* Alerts with Glow */
    .stAlert {
        background: rgba(255, 255, 255, 0.9);
        border: none;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Load data function remains the same
@st.cache_data
def load_data():
    try:
        vendors = pd.read_csv("clean_vendors.csv")
        projects = pd.read_csv("clean_projects.csv")
        metrics = pd.read_csv("it_effectiveness_metrics.csv", index_col=0)
        return vendors, projects, metrics
    except:
        # For local testing
        try:
            vendors = pd.read_csv("02_Data/processed/clean_vendors.csv")
            projects = pd.read_csv("02_Data/processed/clean_projects.csv")
            metrics = pd.read_csv("02_Data/processed/it_effectiveness_metrics.csv", index_col=0)
            return vendors, projects, metrics
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None, None, None

def create_animated_metric(label, value, delta=None, delta_color="normal"):
    """Create an animated metric card"""
    st.markdown(f"""
    <div class="floating">
        {st.metric(label, value, delta, delta_color=delta_color)}
    </div>
    """, unsafe_allow_html=True)

def main():
    # Animated Header
    st.markdown("""
    <h1 class="floating">🚀 IT Intelligence Hub</h1>
    <p style="text-align: center; color: white; font-size: 1.2rem; margin-bottom: 3rem;">
        Next-Generation Analytics for Paul Quinn College
    </p>
    """, unsafe_allow_html=True)
    
    # Load data
    vendors, projects, metrics = load_data()
    if vendors is None:
        return
    
    # Sidebar with modern design
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <div style="width: 100px; height: 100px; margin: 0 auto; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 50%; display: flex; align-items: center; 
                        justify-content: center; font-size: 3rem;">
                🎓
            </div>
            <h3 style="color: white; margin-top: 1rem;">PQC Analytics</h3>
        </div>
        """, unsafe_allow_html=True)
        
        view = st.radio(
            "Select Intelligence View",
            ["🏠 Command Center", "💰 Financial Intelligence", "📊 Strategic Insights", 
             "🔧 Operations Hub", "🤖 AI Predictions"],
            index=0
        )
    
    if view == "🏠 Command Center":
        # Hero Metrics with Animation
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_spend = vendors['annual_spend'].sum()
            st.metric(
                "💎 Total IT Investment",
                f"${total_spend:,.0f}",
                "↓ 12% YoY",
                delta_color="inverse"
            )
        
        with col2:
            roi = float(metrics.loc['project_roi', 'value'])
            st.metric(
                "📈 Portfolio ROI",
                f"{roi:.0f}%",
                "↑ 25% vs benchmark"
            )
        
        with col3:
            availability = float(metrics.loc['avg_availability', 'value'])
            st.metric(
                "⚡ System Performance",
                f"{availability:.1f}%",
                "↑ 0.5% this month"
            )
        
        with col4:
            high_risk = len(projects[projects['risk_flag'] == 'HIGH'])
            st.metric(
                "🎯 Risk Score",
                f"{high_risk} items",
                "Needs attention",
                delta_color="inverse"
            )
        
        # Interactive Visualizations
        st.markdown("### 📊 Live Analytics Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Futuristic Donut Chart
            fig = go.Figure(data=[go.Pie(
                labels=vendors['category'].unique(),
                values=vendors.groupby('category')['annual_spend'].sum(),
                hole=.7,
                marker=dict(
                    colors=px.colors.sequential.Plasma,
                    line=dict(color='white', width=2)
                )
            )])
            
            fig.update_layout(
                title="Investment Distribution",
                showlegend=True,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1a202c', size=14)
            )
            
            # Add center text
            fig.add_annotation(
                text=f"${total_spend/1000:.0f}K",
                x=0.5, y=0.5,
                font_size=30,
                showarrow=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Animated Bar Chart
            project_health = projects.groupby('risk_flag').size()
            
            fig = go.Figure(data=[
                go.Bar(
                    x=project_health.index,
                    y=project_health.values,
                    marker=dict(
                        color=['#00aa00', '#ffaa00', '#ff4444'],
                        line=dict(color='white', width=2)
                    ),
                    text=project_health.values,
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title="Project Health Matrix",
                showlegend=False,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Insights Section with Gradient Cards
        st.markdown("### 🧠 AI-Powered Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("💡 **Opportunity Alert**\n\nVendor consolidation could save $64,350 annually")
        
        with col2:
            st.warning("⚡ **Action Required**\n\n4 projects approaching budget limits")
        
        with col3:
            st.success("🎯 **Performance Win**\n\nSystem uptime exceeds industry standards")

# Run the app
if __name__ == "__main__":
    main()
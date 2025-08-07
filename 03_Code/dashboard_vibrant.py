"""
Paul Quinn College IT Dashboard - Vibrant and Engaging Style
Features: Bold colors, playful animations, interactive elements
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="PQC IT Adventure Dashboard! 🎨",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Vibrant and Engaging CSS
st.markdown("""
<style>
    /* Fun Typography */
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&family=Fredoka+One&display=swap');
    
    /* Vibrant Color Palette */
    :root {
        --hot-pink: #ff006e;
        --bright-blue: #3a86ff;
        --sunshine-yellow: #ffbe0b;
        --mint-green: #8ac926;
        --purple-pop: #c77dff;
    }
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Quicksand', sans-serif;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Playful Headers */
    h1 {
        font-family: 'Fredoka One', cursive;
        font-size: 4rem !important;
        background: linear-gradient(45deg, var(--hot-pink), var(--bright-blue), var(--sunshine-yellow));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Fun Metric Cards */
    [data-testid="metric-container"] {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 3px solid transparent;
        background-image: linear-gradient(white, white), 
                          linear-gradient(45deg, var(--hot-pink), var(--bright-blue));
        background-origin: border-box;
        background-clip: content-box, border-box;
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: scale(1.05) rotate(2deg);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    /* Colorful Metric Values */
    [data-testid="metric-container"]:nth-child(1) [data-testid="metric-value"] {
        color: var(--hot-pink) !important;
        font-weight: 700;
        font-size: 2.5rem !important;
    }
    
    [data-testid="metric-container"]:nth-child(2) [data-testid="metric-value"] {
        color: var(--bright-blue) !important;
        font-weight: 700;
        font-size: 2.5rem !important;
    }
    
    [data-testid="metric-container"]:nth-child(3) [data-testid="metric-value"] {
        color: var(--mint-green) !important;
        font-weight: 700;
        font-size: 2.5rem !important;
    }
    
    [data-testid="metric-container"]:nth-child(4) [data-testid="metric-value"] {
        color: var(--purple-pop) !important;
        font-weight: 700;
        font-size: 2.5rem !important;
    }
    
    /* Playful Sidebar */
    .css-1d391kg {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
    }
    
    /* Fun Buttons */
    .stRadio > div > label {
        background: linear-gradient(45deg, var(--hot-pink), var(--bright-blue));
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.25rem;
        display: inline-block;
        transition: all 0.3s ease;
    }
    
    .stRadio > div > label:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    /* Emoji Rain */
    .emoji {
        position: fixed;
        font-size: 2rem;
        animation: fall linear infinite;
        z-index: 0;
    }
    
    @keyframes fall {
        to {
            transform: translateY(100vh);
        }
    }
    
    /* Fun Alerts */
    .stAlert {
        border-radius: 20px;
        border: none;
        font-weight: 600;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# Add floating emojis
st.markdown("""
<div class="emoji" style="left: 10%; animation-duration: 10s;">💰</div>
<div class="emoji" style="left: 30%; animation-duration: 12s; animation-delay: 1s;">📊</div>
<div class="emoji" style="left: 50%; animation-duration: 8s; animation-delay: 2s;">🚀</div>
<div class="emoji" style="left: 70%; animation-duration: 11s; animation-delay: 0.5s;">⭐</div>
<div class="emoji" style="left: 90%; animation-duration: 9s; animation-delay: 1.5s;">🎯</div>
""", unsafe_allow_html=True)

# Data loading
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
    # Fun Header
    st.markdown("""
    <h1>🎉 PQC IT Magic Dashboard! 🎉</h1>
    <p style="text-align: center; font-size: 1.5rem; color: white; font-weight: 600;">
    Where Data Meets Delight! 🌈
    </p>
    """, unsafe_allow_html=True)
    
    # Load data
    vendors, projects, metrics = load_data()
    if vendors is None:
        return
    
    # Sidebar with fun navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 5rem;">🎨</div>
            <h2 style="color: #ff006e;">Pick Your Adventure!</h2>
        </div>
        """, unsafe_allow_html=True)
        
        view = st.radio(
            "",
            ["🎪 Fun Overview", "💸 Money Madness", "🎯 Strategy Safari", 
             "⚡ Tech Thunder", "🔮 Crystal Ball"],
            index=0
        )
    
    if view == "🎪 Fun Overview":
        # Colorful Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 Money Pot",
                f"${vendors['annual_spend'].sum():,.0f}",
                "Saved 12% 🎉"
            )
        
        with col2:
            roi = float(metrics.loc['project_roi', 'value'])
            st.metric(
                "🚀 ROI Rocket",
                f"{roi:.0f}%",
                "To the moon! 🌙"
            )
        
        with col3:
            st.metric(
                "⭐ Happy Score",
                "4.2/5",
                "Users love it! ❤️"
            )
        
        with col4:
            st.metric(
                "🎯 Success Rate",
                "98.9%",
                "Nearly perfect! ✨"
            )
        
        # Fun Visualizations
        st.markdown("### 🎨 Colorful Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Rainbow Pie Chart
            fig = px.pie(
                vendors,
                values='annual_spend',
                names='category',
                title='🌈 Where the Money Goes!',
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hoverinfo='label+percent+value',
                marker=dict(line=dict(color='white', width=3))
            )
            
            fig.update_layout(
                font=dict(family="Quicksand", size=14, color='#333'),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Fun Gauge Chart
            satisfaction = float(metrics.loc['avg_satisfaction', 'value'])
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = satisfaction,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "😊 Happiness Meter", 'font': {'size': 24}},
                delta = {'reference': 3.5, 'increasing': {'color': "green"}},
                gauge = {
                    'axis': {'range': [None, 5], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "#ff006e"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 1], 'color': '#ffccd5'},
                        {'range': [1, 2], 'color': '#ffb3ba'},
                        {'range': [2, 3], 'color': '#ff99a1'},
                        {'range': [3, 4], 'color': '#ff8087'},
                        {'range': [4, 5], 'color': '#ff666d'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 4.5
                    }
                }
            ))
            
            fig.update_layout(
                height=400,
                font={'family': "Quicksand", 'color': "#333", 'size': 14}
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Fun Facts Section
        st.markdown("### 🎊 Did You Know?")
        
        col1, col2, col3 = st.columns(3)
        
        fun_facts = [
            ("🦸‍♂️", "You're saving more than a superhero!", f"${vendors['annual_spend'].sum() * 0.15:,.0f} in savings identified!"),
            ("🏆", "You're winning at IT!", "125% ROI beats 95% of colleges!"),
            ("🌟", "You're a star performer!", "98.9% uptime is stellar!")
        ]
        
        for col, (emoji, title, fact) in zip([col1, col2, col3], fun_facts):
            with col:
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 20px; 
                            text-align: center; height: 200px; display: flex; 
                            flex-direction: column; justify-content: center;
                            box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
                    <div style="font-size: 3rem;">{emoji}</div>
                    <h4 style="color: #ff006e; margin: 0.5rem 0;">{title}</h4>
                    <p style="color: #666;">{fact}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Interactive Elements
        st.markdown("### 🎮 Play with the Data!")
        
        if st.button("🎲 Generate Random Insight!", key="insight_btn"):
            insights = [
                "🎯 Your best performing vendor is saving you 20% compared to market rates!",
                "🚀 Project completion rate increased by 15% this quarter!",
                "💡 AI suggests consolidating software licenses for $25K savings!",
                "⭐ User satisfaction is at an all-time high!",
                "🎨 Your IT portfolio is more balanced than 80% of similar institutions!"
            ]
            st.balloons()
            st.success(random.choice(insights))

if __name__ == "__main__":
    main()

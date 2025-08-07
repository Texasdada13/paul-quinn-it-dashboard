"""
Paul Quinn College IT Analytics Suite - Multi-Page App
Combines all dashboards into one application
"""

import streamlit as st

st.set_page_config(
    page_title="PQC IT Analytics Suite",
    page_icon="🎓",
    layout="wide"
)

# Create navigation
page = st.sidebar.selectbox(
    "Choose a Dashboard",
    ["Home", "Executive Overview", "Modern Style", "Corporate Style", "Vibrant Style", "Usage & ROI Analytics"]
)

if page == "Home":
    st.title("🎓 Paul Quinn College IT Analytics Suite")
    st.markdown("### Select a dashboard from the sidebar to begin")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **Available Dashboards:**
        - **Executive Overview**: Original comprehensive dashboard
        - **Modern Style**: Glassmorphism with animations
        - **Corporate Style**: Professional board-ready view
        - **Vibrant Style**: Colorful and engaging
        - **Usage & ROI**: Deep dive into utilization and returns
        """)
    with col2:
        st.success("""
        **Key Metrics Available:**
        - IT Spend Analysis
        - Vendor Management
        - Project Tracking
        - Usage Analytics
        - ROI Calculations
        - Predictive Insights
        """)

elif page == "Executive Overview":
    exec(open('03_Code/it_dashboard_app.py').read())
    
elif page == "Modern Style":
    exec(open('03_Code/dashboard_modern.py').read())
    
elif page == "Corporate Style":
    exec(open('03_Code/dashboard_corporate.py').read())
    
elif page == "Vibrant Style":
    exec(open('03_Code/dashboard_vibrant.py').read())
    
elif page == "Usage & ROI Analytics":
    exec(open('03_Code/usage_roi_dashboard_fixed.py').read())

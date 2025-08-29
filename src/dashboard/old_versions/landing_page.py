import streamlit as st

st.set_page_config(
    page_title="PQC IT Analytics Suite",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Paul Quinn College IT Analytics Suite")
st.markdown("### Welcome to Your IT Intelligence Platform")

st.info("""
**Available Dashboards:**

Deploy each dashboard separately for now:
- [Executive Dashboard](https://your-app.streamlit.app) - Deploy using `it_dashboard_app.py`
- [Modern Style](https://your-app2.streamlit.app) - Deploy using `03_Code/dashboard_modern.py`
- [Usage & ROI](https://your-app3.streamlit.app) - Deploy using `03_Code/usage_roi_dashboard_fixed.py`
""")

st.success("For now, please deploy each dashboard as a separate app!")

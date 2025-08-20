import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PQC IT Dashboard", page_icon="🎓", layout="wide")

st.title("🎓 Paul Quinn College IT Analytics Suite")
st.markdown("### IT Spend Management Dashboard")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📊 Overview", "💰 Budget", "📈 Projects"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total IT Budget", "$2.8M", "+5.2%")
    with col2:
        st.metric("YTD Spend", "$1.9M", "-3%")
    with col3:
        st.metric("Cost Savings", "$340K", "+12%")
    with col4:
        st.metric("Active Projects", "5", "+2")
    
    st.success("Dashboard is working! 🎉")

with tab2:
    st.header("Budget Analysis")
    
    # Sample data
    budget_data = pd.DataFrame({
        'Category': ['Cloud Services', 'Software', 'Hardware', 'Security', 'Services'],
        'Budget': [850000, 620000, 480000, 500000, 350000],
        'Actual': [780000, 590000, 510000, 485000, 320000]
    })
    
    fig = px.bar(budget_data, x='Category', y=['Budget', 'Actual'], barmode='group',
                 title="Budget vs Actual Spend")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Project Status")
    
    projects = pd.DataFrame({
        'Project': ['Cloud Migration', 'Student Portal', 'Security Update', 'LMS Upgrade'],
        'Status': ['In Progress', 'Completed', 'In Progress', 'Planning'],
        'Completion': [75, 100, 40, 10]
    })
    
    st.dataframe(projects, use_container_width=True)

st.markdown("---")
st.markdown("✅ Minimal version working! Ready for full deployment.")
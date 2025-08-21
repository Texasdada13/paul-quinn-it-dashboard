"""
Paul Quinn College IT Analytics Suite
Enterprise IT Spend & Project Management Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import json

# Page configuration
st.set_page_config(
    page_title="PQC IT Analytics Suite",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for consistent styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1e3d59;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: 600;
    }
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_persona' not in st.session_state:
    st.session_state.current_persona = 'CFO'

# Helper functions
def generate_sample_data():
    """Generate sample data for demonstrations"""
    return {
        'projects': pd.DataFrame({
            'Project Name': ['Student Portal Upgrade', 'Cloud Migration Phase 1', 'Cybersecurity Enhancement', 
                           'LMS Modernization', 'Network Infrastructure'],
            'Status': ['In Progress', 'Completed', 'In Progress', 'Planning', 'In Progress'],
            'Budget': [250000, 180000, 300000, 150000, 200000],
            'Spent': [175000, 178000, 125000, 20000, 150000],
            'Completion': [70, 100, 40, 10, 75],
            'Risk Level': ['Medium', 'Low', 'High', 'Low', 'Medium'],
            'End Date': pd.to_datetime(['2024-06-30', '2024-03-15', '2024-09-30', '2024-12-31', '2024-07-31'])
        }),
        'vendors': pd.DataFrame({
            'Vendor': ['Microsoft', 'Adobe', 'AWS', 'Blackboard', 'Cisco', 'Zoom', 'Others'],
            'Annual Spend': [450000, 280000, 520000, 180000, 220000, 85000, 265000],
            'Contract End': pd.to_datetime(['2025-06-30', '2024-12-31', '2025-03-31', '2024-09-30', 
                                          '2025-12-31', '2024-06-30', '2025-01-31']),
            'Satisfaction': [4.2, 3.8, 4.5, 3.2, 4.0, 4.6, 3.5]
        }),
        'usage': pd.DataFrame({
            'System': ['Email (Office 365)', 'LMS (Blackboard)', 'Video Conferencing', 'Cloud Storage', 
                      'Student Portal', 'Library Systems'],
            'Active Users': [850, 750, 680, 720, 820, 450],
            'Total Licenses': [900, 900, 700, 900, 900, 500],
            'Utilization %': [94, 83, 97, 80, 91, 90]
        })
    }

# Sidebar navigation
st.sidebar.markdown("### 🎓 Paul Quinn College")
st.sidebar.markdown("**IT Analytics Suite**")
st.sidebar.markdown("---")

persona = st.sidebar.selectbox(
    "Select Persona View",
    ["CFO - Financial Steward", "CIO - Strategic Partner", "CTO - Technology Operator", "Project Manager View"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Actions")
if st.sidebar.button("📊 Generate Report"):
    st.sidebar.success("Report generated!")
if st.sidebar.button("📧 Email Dashboard"):
    st.sidebar.success("Dashboard emailed!")
if st.sidebar.button("🔄 Refresh Data"):
    st.sidebar.success("Data refreshed!")

# Load sample data
data = generate_sample_data()

# Main content based on persona
st.markdown("<h1 class='main-header'>🎓 Paul Quinn College IT Analytics Suite</h1>", unsafe_allow_html=True)

if persona == "CFO - Financial Steward":
    st.markdown("### CFO Dashboard - Financial Overview & Optimization")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total IT Budget", "$2.8M", "+5.2%", help="Year-over-year change")
    with col2:
        st.metric("YTD Spend", "$1.9M", "-3%", help="68% of annual budget")
    with col3:
        st.metric("Cost Savings", "$340K", "+12%", help="Through optimization initiatives")
    with col4:
        st.metric("ROI", "2.4x", "+0.3", help="Return on IT investments")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Budget Analysis", "💰 Cost Optimization", "📈 Benchmarking", "📑 Reports"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Budget breakdown chart
            budget_data = pd.DataFrame({
                'Category': ['Cloud Services', 'Software Licenses', 'Hardware', 'Professional Services', 'Security'],
                'Budget': [850000, 620000, 480000, 350000, 500000],
                'Actual': [780000, 590000, 510000, 320000, 485000]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Budget', x=budget_data['Category'], y=budget_data['Budget'], 
                               marker_color='lightblue'))
            fig.add_trace(go.Bar(name='Actual', x=budget_data['Category'], y=budget_data['Actual'], 
                               marker_color='darkblue'))
            fig.update_layout(
                title="Budget vs Actual Spend by Category",
                barmode='group',
                height=400,
                xaxis_title="Category",
                yaxis_title="Amount ($)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Spend distribution pie chart
            fig_pie = px.pie(
                values=[780000, 590000, 510000, 320000, 485000],
                names=['Cloud', 'Software', 'Hardware', 'Services', 'Security'],
                title="Spend Distribution"
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Trend analysis
        st.subheader("3-Year Spending Trend")
        years = [2022, 2023, 2024]
        trend_data = pd.DataFrame({
            'Year': years * 3,
            'Category': ['Run'] * 3 + ['Grow'] * 3 + ['Transform'] * 3,
            'Amount': [1.8, 1.9, 2.0, 0.5, 0.6, 0.7, 0.2, 0.3, 0.4]
        })
        
        fig_trend = px.line(trend_data, x='Year', y='Amount', color='Category', 
                           title="Strategic IT Investment Trend (in $M)", markers=True)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with tab2:
        st.warning("🔔 **3 Cost Optimization Opportunities Identified** - Potential Annual Savings: $125K")
        
        # Optimization opportunities table
        opt_df = pd.DataFrame({
            'Opportunity': ['Consolidate LMS Platforms', 'Unused Software Licenses', 'Cloud Right-sizing'],
            'Annual Savings': ['$45,000', '$38,000', '$42,000'],
            'Effort': ['Medium', 'Low', 'Low'],
            'Impact': ['High', 'Low', 'Medium'],
            'Status': ['🟡 In Review', '🟢 Approved', '🟡 Pending']
        })
        
        st.dataframe(opt_df, use_container_width=True, hide_index=True)
        
        # Vendor analysis
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top Vendor Spend")
            vendor_chart = px.bar(data['vendors'].head(5), x='Vendor', y='Annual Spend', 
                                 title="Top 5 Vendors by Annual Spend")
            st.plotly_chart(vendor_chart, use_container_width=True)
        
        with col2:
            st.subheader("License Utilization")
            usage_chart = px.bar(data['usage'], x='System', y='Utilization %', 
                                title="System Utilization Rates", color='Utilization %',
                                color_continuous_scale='RdYlGn')
            st.plotly_chart(usage_chart, use_container_width=True)
    
    with tab3:
        st.subheader("Peer Institution Benchmarking")
        
        # Benchmark comparison
        benchmark_data = pd.DataFrame({
            'Metric': ['IT Spend per Student', 'IT % of Budget', 'Cloud Adoption %', 'Security Spend %'],
            'Paul Quinn': [2800, 4.2, 65, 12],
            'Peer Average': [3200, 5.1, 58, 10],
            'Top Quartile': [2500, 3.8, 75, 15]
        })
        
        fig_bench = go.Figure()
        fig_bench.add_trace(go.Bar(name='Paul Quinn', x=benchmark_data['Metric'], y=benchmark_data['Paul Quinn']))
        fig_bench.add_trace(go.Bar(name='Peer Average', x=benchmark_data['Metric'], y=benchmark_data['Peer Average']))
        fig_bench.add_trace(go.Bar(name='Top Quartile', x=benchmark_data['Metric'], y=benchmark_data['Top Quartile']))
        fig_bench.update_layout(barmode='group', title="Benchmark Comparison with Peer Institutions")
        st.plotly_chart(fig_bench, use_container_width=True)
        
        # Performance indicators
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("**Cost Efficiency**: Better than 72% of peers")
        with col2:
            st.success("**Cloud Adoption**: Leading peer group")
        with col3:
            st.warning("**Security Investment**: Room for improvement")
    
    with tab4:
        st.subheader("Financial Reports & Compliance")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Available Reports")
            if st.button("📄 Annual IT Budget Report"):
                st.success("Generating report...")
            if st.button("📊 Cost Optimization Analysis"):
                st.success("Generating report...")
            if st.button("📈 ROI Assessment"):
                st.success("Generating report...")
            if st.button("✅ Compliance Audit Trail"):
                st.success("Generating report...")
        
        with col2:
            st.markdown("### Compliance Status")
            compliance_df = pd.DataFrame({
                'Standard': ['FERPA', 'Title IV', 'PCI DSS', 'NIST'],
                'Status': ['✅ Compliant', '✅ Compliant', '⚠️ Review Needed', '✅ Compliant'],
                'Last Audit': ['Jan 2024', 'Mar 2024', 'Due', 'Feb 2024']
            })
            st.dataframe(compliance_df, use_container_width=True, hide_index=True)

elif persona == "CIO - Strategic Partner":
    st.markdown("### CIO Dashboard - Strategic IT Portfolio Management")
    
    # Strategic metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Digital Transformation", "65%", "+15%", help="Progress on digital initiatives")
    with col2:
        st.metric("Project Success Rate", "87%", "+5%", help="Projects completed on time/budget")
    with col3:
        st.metric("Innovation Index", "7.8/10", "+0.6", help="Innovation maturity score")
    with col4:
        st.metric("Business Alignment", "92%", "+3%", help="IT-Business alignment score")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Strategic Portfolio", "📊 Project Performance", "🚀 Innovation Pipeline", "⚠️ Risk Management"])
    
    with tab1:
        st.subheader("IT Investment by Strategic Category")
        
        # Strategic allocation
        strategy_data = pd.DataFrame({
            'Category': ['Run', 'Grow', 'Transform'],
            'Current': [70, 20, 10],
            'Target': [60, 25, 15],
            'Best Practice': [50, 30, 20]
        })
        
        fig_strategy = go.Figure()
        fig_strategy.add_trace(go.Bar(name='Current', x=strategy_data['Category'], y=strategy_data['Current']))
        fig_strategy.add_trace(go.Bar(name='Target', x=strategy_data['Category'], y=strategy_data['Target']))
        fig_strategy.add_trace(go.Bar(name='Best Practice', x=strategy_data['Category'], y=strategy_data['Best Practice']))
        fig_strategy.update_layout(
            barmode='group',
            title="Strategic IT Investment Distribution (%)",
            yaxis_title="Percentage of IT Budget"
        )
        st.plotly_chart(fig_strategy, use_container_width=True)
        
        # Initiative alignment
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Initiative Alignment with College Mission")
            alignment_data = pd.DataFrame({
                'Initiative': ['Online Learning Platform', 'Student Success Analytics', 'Digital Campus', 'Cybersecurity'],
                'Alignment Score': [95, 92, 88, 85],
                'Impact': ['High', 'High', 'Medium', 'High']
            })
            fig_align = px.bar(alignment_data, x='Alignment Score', y='Initiative', orientation='h',
                             color='Impact', title="Mission Alignment Scores")
            st.plotly_chart(fig_align, use_container_width=True)
        
        with col2:
            st.subheader("Digital Maturity Assessment")
            maturity_data = pd.DataFrame({
                'Area': ['Infrastructure', 'Applications', 'Data & Analytics', 'Security', 'Innovation'],
                'Score': [7.5, 6.8, 5.5, 8.2, 6.0]
            })
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=maturity_data['Score'],
                theta=maturity_data['Area'],
                fill='toself',
                name='Current State'
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                showlegend=False,
                title="Digital Maturity Scores"
            )
            st.plotly_chart(fig_radar, use_container_width=True)
    
    with tab2:
        st.subheader("Active Project Portfolio")
        
        # Project dashboard
        projects_display = data['projects'].copy()
        projects_display['Progress'] = projects_display['Completion'].apply(lambda x: f"{x}%")
        projects_display['Budget Utilization'] = (projects_display['Spent'] / projects_display['Budget'] * 100).round(1).astype(str) + '%'
        
        st.dataframe(
            projects_display[['Project Name', 'Status', 'Progress', 'Budget', 'Spent', 'Budget Utilization', 'Risk Level', 'End Date']],
            use_container_width=True,
            hide_index=True
        )
        
        # Project timeline
        st.subheader("Project Timeline (Gantt View)")
        gantt_data = []
        for _, project in data['projects'].iterrows():
            gantt_data.append(dict(
                Task=project['Project Name'],
                Start=datetime.now() - timedelta(days=90),
                Finish=project['End Date'],
                Complete=project['Completion']
            ))
        
        fig_gantt = px.timeline(
            pd.DataFrame(gantt_data),
            x_start="Start",
            x_end="Finish",
            y="Task",
            title="Project Timeline"
        )
        fig_gantt.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_gantt, use_container_width=True)
    
    with tab3:
        st.subheader("Innovation Pipeline & Emerging Technologies")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Technologies Under Evaluation")
            tech_eval = pd.DataFrame({
                'Technology': ['AI-Powered Student Advising', 'Blockchain Credentials', 'IoT Campus Safety', 'VR Learning Labs'],
                'Potential Impact': ['High', 'Medium', 'High', 'Medium'],
                'Readiness': ['Pilot', 'Research', 'Planning', 'Research'],
                'Investment': ['$75K', '$25K', '$100K', '$50K']
            })
            st.dataframe(tech_eval, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("### Innovation Metrics")
            st.metric("Ideas Submitted", "47", "+12 this quarter")
            st.metric("Pilots Active", "3", "")
            st.metric("Time to Production", "4.2 months", "-0.8 months")
            st.metric("Innovation ROI", "3.2x", "+0.5x")
    
    with tab4:
        st.subheader("IT Risk Dashboard")
        
        # Risk matrix
        risk_data = pd.DataFrame({
            'Risk': ['Legacy System Failure', 'Cyber Attack', 'Vendor Lock-in', 'Budget Overrun', 'Skills Gap'],
            'Probability': [3, 2, 4, 2, 3],
            'Impact': [4, 5, 3, 3, 3],
            'Score': [12, 10, 12, 6, 9],
            'Mitigation': ['Modernization plan in progress', 'Security tools deployed', 'Multi-vendor strategy', 
                         'Monthly reviews', 'Training program launched']
        })
        
        fig_risk = px.scatter(risk_data, x='Probability', y='Impact', size='Score', 
                            hover_data=['Risk', 'Mitigation'], text='Risk',
                            title="Risk Heat Map", color='Score',
                            color_continuous_scale='Reds')
        fig_risk.update_layout(xaxis_title="Probability", yaxis_title="Impact")
        st.plotly_chart(fig_risk, use_container_width=True)
        
        # Risk details
        st.dataframe(risk_data[['Risk', 'Score', 'Mitigation']], use_container_width=True, hide_index=True)

elif persona == "CTO - Technology Operator":
    st.markdown("### CTO Dashboard - Technical Operations & Infrastructure")
    
    # Technical metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("System Uptime", "99.8%", "+0.2%", help="Last 30 days")
    with col2:
        st.metric("Incident Resolution", "2.4 hrs", "-0.6 hrs", help="Average resolution time")
    with col3:
        st.metric("Cloud Utilization", "78%", "+5%", help="Resource utilization")
    with col4:
        st.metric("Security Score", "A-", "↑", help="Security posture rating")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🖥️ Infrastructure", "📊 Performance", "🔒 Security", "👥 Support"])
    
    with tab1:
        st.subheader("Infrastructure Overview")
        
        col1, col2 = st.columns(2)
        with col1:
            # Server utilization
            server_data = pd.DataFrame({
                'Server': ['Web Server 1', 'Web Server 2', 'DB Server', 'App Server', 'File Server'],
                'CPU %': [45, 62, 78, 55, 38],
                'Memory %': [52, 70, 85, 48, 42],
                'Storage %': [60, 55, 92, 45, 88]
            })
            
            fig_server = go.Figure()
            fig_server.add_trace(go.Bar(name='CPU', x=server_data['Server'], y=server_data['CPU %']))
            fig_server.add_trace(go.Bar(name='Memory', x=server_data['Server'], y=server_data['Memory %']))
            fig_server.add_trace(go.Bar(name='Storage', x=server_data['Server'], y=server_data['Storage %']))
            fig_server.update_layout(barmode='group', title="Server Resource Utilization")
            st.plotly_chart(fig_server, use_container_width=True)
        
        with col2:
            # Cloud vs on-premise
            cloud_data = pd.DataFrame({
                'Type': ['Cloud', 'On-Premise'],
                'Workloads': [65, 35]
            })
            fig_cloud = px.pie(cloud_data, values='Workloads', names='Type', 
                             title="Workload Distribution", hole=0.4)
            st.plotly_chart(fig_cloud, use_container_width=True)
        
        # Network performance
        st.subheader("Network Performance (Last 24 Hours)")
        hours = list(range(24))
        bandwidth_data = pd.DataFrame({
            'Hour': hours,
            'Bandwidth (Mbps)': [200 + np.random.randint(-50, 100) for _ in hours],
            'Latency (ms)': [10 + np.random.randint(-5, 10) for _ in hours]
        })
        
        fig_network = go.Figure()
        fig_network.add_trace(go.Scatter(x=bandwidth_data['Hour'], y=bandwidth_data['Bandwidth (Mbps)'],
                                       mode='lines', name='Bandwidth', yaxis='y'))
        fig_network.add_trace(go.Scatter(x=bandwidth_data['Hour'], y=bandwidth_data['Latency (ms)'],
                                       mode='lines', name='Latency', yaxis='y2'))
        fig_network.update_layout(
            title="Network Performance Metrics",
            xaxis_title="Hour",
            yaxis=dict(title="Bandwidth (Mbps)", side='left'),
            yaxis2=dict(title="Latency (ms)", overlaying='y', side='right')
        )
        st.plotly_chart(fig_network, use_container_width=True)
    
    with tab2:
        st.subheader("Application Performance Monitoring")
        
        # Application health
        app_data = pd.DataFrame({
            'Application': ['Student Portal', 'LMS', 'Email System', 'Library System', 'Finance System'],
            'Response Time (ms)': [245, 380, 120, 290, 410],
            'Availability %': [99.9, 99.5, 99.99, 99.7, 99.8],
            'Error Rate %': [0.1, 0.5, 0.01, 0.3, 0.2],
            'Users': [820, 750, 850, 450, 125]
        })
        
        st.dataframe(app_data, use_container_width=True, hide_index=True)
        
        # Performance trends
        col1, col2 = st.columns(2)
        with col1:
            fig_response = px.bar(app_data, x='Application', y='Response Time (ms)', 
                                title="Application Response Times",
                                color='Response Time (ms)', color_continuous_scale='RdYlGn_r')
            st.plotly_chart(fig_response, use_container_width=True)
        
        with col2:
            fig_availability = px.bar(app_data, x='Application', y='Availability %', 
                                    title="Application Availability",
                                    color='Availability %', color_continuous_scale='RdYlGn')
            st.plotly_chart(fig_availability, use_container_width=True)
    
    with tab3:
        st.subheader("Security Operations Center")
        
        # Security metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Threats Blocked", "1,247", "+15%", help="Last 7 days")
        with col2:
            st.metric("Vulnerabilities", "12", "-3", help="Open vulnerabilities")
        with col3:
            st.metric("Patch Compliance", "94%", "+2%", help="Systems patched")
        with col4:
            st.metric("Security Training", "87%", "+5%", help="Staff completed")
        
        # Threat analysis
        threat_data = pd.DataFrame({
            'Date': pd.date_range(start='2024-01-01', periods=7, freq='D'),
            'Malware': [12, 15, 8, 22, 18, 14, 16],
            'Phishing': [45, 52, 38, 41, 55, 48, 42],
            'DDoS': [2, 0, 1, 3, 0, 1, 2],
            'Other': [8, 12, 6, 9, 11, 7, 10]
        })
        
        fig_threats = go.Figure()
        for threat in ['Malware', 'Phishing', 'DDoS', 'Other']:
            fig_threats.add_trace(go.Scatter(x=threat_data['Date'], y=threat_data[threat],
                                           mode='lines+markers', name=threat, stackgroup='one'))
        fig_threats.update_layout(title="Security Threat Trends (Last 7 Days)")
        st.plotly_chart(fig_threats, use_container_width=True)
        
        # Vulnerability status
        st.subheader("Vulnerability Management")
        vuln_data = pd.DataFrame({
            'Severity': ['Critical', 'High', 'Medium', 'Low'],
            'Open': [0, 2, 5, 5],
            'In Progress': [1, 3, 8, 12],
            'Resolved (30d)': [5, 18, 42, 68]
        })
        
        fig_vuln = go.Figure()
        fig_vuln.add_trace(go.Bar(name='Open', x=vuln_data['Severity'], y=vuln_data['Open']))
        fig_vuln.add_trace(go.Bar(name='In Progress', x=vuln_data['Severity'], y=vuln_data['In Progress']))
        fig_vuln.add_trace(go.Bar(name='Resolved', x=vuln_data['Severity'], y=vuln_data['Resolved (30d)']))
        fig_vuln.update_layout(barmode='stack', title="Vulnerability Status by Severity")
        st.plotly_chart(fig_vuln, use_container_width=True)
    
    with tab4:
        st.subheader("IT Support Operations")
        
        # Ticket metrics
        col1, col2 = st.columns(2)
        with col1:
            ticket_data = pd.DataFrame({
                'Category': ['Hardware', 'Software', 'Network', 'Account', 'Other'],
                'Open': [12, 28, 8, 15, 10],
                'Resolved (Week)': [45, 112, 32, 68, 38]
            })
            
            fig_tickets = go.Figure()
            fig_tickets.add_trace(go.Bar(name='Open', x=ticket_data['Category'], y=ticket_data['Open']))
            fig_tickets.add_trace(go.Bar(name='Resolved', x=ticket_data['Category'], y=ticket_data['Resolved (Week)']))
            fig_tickets.update_layout(barmode='group', title="Support Tickets by Category")
            st.plotly_chart(fig_tickets, use_container_width=True)
        
        with col2:
            # SLA compliance
            sla_data = pd.DataFrame({
                'Priority': ['Critical', 'High', 'Medium', 'Low'],
                'SLA Met %': [98, 95, 92, 88],
                'Target %': [99, 95, 90, 85]
            })
            
            fig_sla = go.Figure()
            fig_sla.add_trace(go.Bar(name='Actual', x=sla_data['Priority'], y=sla_data['SLA Met %']))
            fig_sla.add_trace(go.Bar(name='Target', x=sla_data['Priority'], y=sla_data['Target %']))
            fig_sla.update_layout(barmode='group', title="SLA Compliance by Priority")
            st.plotly_chart(fig_sla, use_container_width=True)

elif persona == "Project Manager View":
    st.markdown("### Project Management Dashboard")
    
    # Project metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Projects", "5", "", help="Currently in progress")
    with col2:
        st.metric("On Schedule", "80%", "+10%", help="Projects on track")
    with col3:
        st.metric("Resource Utilization", "85%", "+5%", help="Team capacity")
    with col4:
        st.metric("Budget Variance", "-2.3%", "", help="Under budget")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Project Overview", "📊 RAID Log", "👥 Resources", "📈 Reports"])
    
    with tab1:
        st.subheader("Active Projects Status")
        
        # Enhanced project view
        projects_pm = data['projects'].copy()
        projects_pm['Health'] = projects_pm['Risk Level'].map({'Low': '🟢', 'Medium': '🟡', 'High': '🔴'})
        projects_pm['Budget Status'] = projects_pm.apply(
            lambda x: '✅' if x['Spent'] <= x['Budget'] else '⚠️', axis=1
        )
        
        display_cols = ['Health', 'Project Name', 'Status', 'Completion', 'Budget', 'Spent', 'Budget Status', 'End Date']
        st.dataframe(projects_pm[display_cols], use_container_width=True, hide_index=True)
        
        # Project health dashboard
        col1, col2 = st.columns(2)
        with col1:
            health_counts = projects_pm['Risk Level'].value_counts()
            fig_health = px.pie(values=health_counts.values, names=health_counts.index, 
                              title="Project Health Distribution",
                              color_discrete_map={'Low': 'green', 'Medium': 'yellow', 'High': 'red'})
            st.plotly_chart(fig_health, use_container_width=True)
        
        with col2:
            # Budget burn rate
            burn_data = pd.DataFrame({
                'Project': projects_pm['Project Name'],
                'Burn Rate': (projects_pm['Spent'] / projects_pm['Budget'] * 100).round(1)
            })
            fig_burn = px.bar(burn_data, x='Project', y='Burn Rate', title="Budget Burn Rate (%)",
                            color='Burn Rate', color_continuous_scale='RdYlGn_r')
            st.plotly_chart(fig_burn, use_container_width=True)
    
    with tab2:
        st.subheader("RAID Log (Risks, Actions, Issues, Decisions)")
        
        # RAID items
        raid_data = pd.DataFrame({
            'ID': ['R001', 'A001', 'I001', 'D001', 'R002', 'I002'],
            'Type': ['Risk', 'Action', 'Issue', 'Decision', 'Risk', 'Issue'],
            'Project': ['Cloud Migration', 'Student Portal', 'LMS Modernization', 'Cybersecurity', 'Network Infrastructure', 'Student Portal'],
            'Description': [
                'Potential data migration delays',
                'Complete user acceptance testing',
                'Integration API not working',
                'Selected AWS as cloud provider',
                'Vendor contract expiring',
                'Performance degradation reported'
            ],
            'Priority': ['High', 'High', 'Critical', 'Medium', 'Medium', 'High'],
            'Owner': ['John Smith', 'Sarah Johnson', 'Mike Davis', 'Lisa Brown', 'John Smith', 'Sarah Johnson'],
            'Due Date': pd.to_datetime(['2024-02-15', '2024-02-10', '2024-02-05', '2024-01-30', '2024-03-01', '2024-02-08']),
            'Status': ['Open', 'In Progress', 'Open', 'Closed', 'Open', 'In Progress']
        })
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            type_filter = st.multiselect("Filter by Type", options=raid_data['Type'].unique(), 
                                       default=raid_data['Type'].unique())
        with col2:
            priority_filter = st.multiselect("Filter by Priority", options=raid_data['Priority'].unique(),
                                           default=raid_data['Priority'].unique())
        with col3:
            status_filter = st.multiselect("Filter by Status", options=raid_data['Status'].unique(),
                                         default=raid_data['Status'].unique())
        
        # Apply filters
        filtered_raid = raid_data[
            (raid_data['Type'].isin(type_filter)) &
            (raid_data['Priority'].isin(priority_filter)) &
            (raid_data['Status'].isin(status_filter))
        ]
        
        st.dataframe(filtered_raid, use_container_width=True, hide_index=True)
        
        # RAID summary
        col1, col2 = st.columns(2)
        with col1:
            raid_summary = filtered_raid['Type'].value_counts()
            fig_raid = px.bar(x=raid_summary.index, y=raid_summary.values, 
                            title="RAID Items by Type", labels={'x': 'Type', 'y': 'Count'})
            st.plotly_chart(fig_raid, use_container_width=True)
        
        with col2:
            priority_summary = filtered_raid['Priority'].value_counts()
            fig_priority = px.pie(values=priority_summary.values, names=priority_summary.index,
                                title="Items by Priority")
            st.plotly_chart(fig_priority, use_container_width=True)
    
    with tab3:
        st.subheader("Resource Management")
        
        # Team allocation
        team_data = pd.DataFrame({
            'Team Member': ['John Smith', 'Sarah Johnson', 'Mike Davis', 'Lisa Brown', 'Tom Wilson'],
            'Role': ['Project Manager', 'Developer', 'Developer', 'Business Analyst', 'QA Engineer'],
            'Current Project': ['Cloud Migration', 'Student Portal', 'Student Portal', 'LMS Modernization', 'Cybersecurity'],
            'Allocation %': [100, 80, 80, 60, 75],
            'Available Hours': [0, 8, 8, 16, 10]
        })
        
        st.dataframe(team_data, use_container_width=True, hide_index=True)
        
        # Resource utilization chart
        fig_resource = px.bar(team_data, x='Team Member', y='Allocation %', 
                            title="Team Resource Allocation",
                            color='Allocation %', color_continuous_scale='RdYlGn_r')
        fig_resource.add_hline(y=100, line_dash="dash", line_color="red", 
                             annotation_text="Max Capacity")
        st.plotly_chart(fig_resource, use_container_width=True)
        
        # Skills matrix
        st.subheader("Team Skills Matrix")
        skills_data = pd.DataFrame({
            'Team Member': ['John Smith', 'Sarah Johnson', 'Mike Davis', 'Lisa Brown', 'Tom Wilson'],
            'Project Management': [5, 2, 2, 3, 2],
            'Development': [2, 5, 5, 2, 3],
            'Cloud/AWS': [4, 4, 5, 3, 3],
            'Security': [3, 3, 4, 2, 5],
            'Business Analysis': [4, 2, 2, 5, 3]
        })
        
        fig_skills = go.Figure(data=go.Heatmap(
            z=skills_data.iloc[:, 1:].values,
            x=skills_data.columns[1:],
            y=skills_data['Team Member'],
            colorscale='Viridis',
            text=skills_data.iloc[:, 1:].values,
            texttemplate="%{text}",
            textfont={"size": 12}
        ))
        fig_skills.update_layout(title="Team Skills Matrix (1-5 scale)")
        st.plotly_chart(fig_skills, use_container_width=True)
    
    with tab4:
        st.subheader("Project Reports & Analytics")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Generate Reports")
            report_type = st.selectbox("Select Report Type", [
                "Project Status Report",
                "Resource Utilization Report",
                "Budget Analysis Report",
                "Risk Assessment Report",
                "Milestone Tracking Report"
            ])
            
            date_range = st.date_input("Date Range", value=(datetime.now() - timedelta(days=30), datetime.now()))
            
            if st.button("Generate Report", type="primary"):
                st.success(f"Generating {report_type}...")
                st.download_button(
                    label="Download Report",
                    data=f"Sample {report_type} content",
                    file_name=f"{report_type.lower().replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
        
        with col2:
            st.markdown("### Quick Stats")
            st.info("**Milestones This Month**: 8")
            st.success("**Completed Tasks**: 145")
            st.warning("**Overdue Items**: 3")
            st.error("**Critical Issues**: 1")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Paul Quinn College IT Analytics Suite | Built with Streamlit | © 2024</p>
    </div>
    """,
    unsafe_allow_html=True
)
"""
Executive Usage & ROI Dashboard - Fixed Version
Shows the complete picture of IT value
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="IT Usage & ROI Dashboard", layout="wide")

# Custom CSS for executive style
st.markdown("""
<style>
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
        color: #1e3d59;
    }
    .medium-font {
        font-size: 18px !important;
        color: #2e4d69;
    }
    .insight-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_usage_data():
    """Load all usage and ROI data"""
    try:
        usage = pd.read_excel('PQC_Usage_Efficiency_ROI_Data.xlsx', sheet_name='Software_Usage')
        efficiency = pd.read_excel('PQC_Usage_Efficiency_ROI_Data.xlsx', sheet_name='Efficiency_Gains')
        roi = pd.read_excel('PQC_Usage_Efficiency_ROI_Data.xlsx', sheet_name='ROI_Analysis')
        satisfaction = pd.read_excel('PQC_Usage_Efficiency_ROI_Data.xlsx', sheet_name='User_Satisfaction')
        comparison = pd.read_excel('PQC_Usage_Efficiency_ROI_Data.xlsx', sheet_name='Usage_Comparison')
        return usage, efficiency, roi, satisfaction, comparison
    except:
        st.error("Please run generate_usage_roi_data.py first!")
        return None, None, None, None, None

def main():
    st.title(" IT Usage, Efficiency & ROI Dashboard")
    st.markdown("**Executive View**: Complete Picture of IT Value Delivery")
    
    # Load data
    usage, efficiency, roi, satisfaction, comparison = load_usage_data()
    if usage is None:
        return
    
    # Top-line metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_utilization = usage['utilization_rate'].mean()
        st.metric(
            "License Utilization",
            f"{avg_utilization:.0f}%",
            f"${(100-avg_utilization)/100 * 2322572:.0f} wasted",
            delta_color="inverse"
        )
    
    with col2:
        total_roi = roi['net_benefit'].sum()
        st.metric(
            "Total ROI Value",
            f"${total_roi:,.0f}",
            f"{(total_roi/roi['annual_cost'].sum()*100):.0f}% return"
        )
    
    with col3:
        hours_saved = roi['labor_hours_saved'].sum()
        st.metric(
            "Hours Saved/Year",
            f"{hours_saved:,.0f}",
            f"={hours_saved/2080:.0f} FTEs"
        )
    
    with col4:
        avg_satisfaction = satisfaction['satisfaction_score'].mean()
        st.metric(
            "User Satisfaction",
            f"{avg_satisfaction:.1f}/5.0",
            "Above target" if avg_satisfaction > 4 else "Below target"
        )
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([" Usage & Waste", " ROI Analysis", " Efficiency Gains", " User Satisfaction"])
    
    with tab1:
        st.subheader("Software Usage Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Utilization by category
            usage_by_vendor = usage.groupby('vendor_name').agg({
                'utilization_rate': 'mean',
                'cost_per_active_user': 'mean'
            }).sort_values('utilization_rate')
            
            fig = px.bar(
                usage_by_vendor.tail(10),
                x='utilization_rate',
                orientation='h',
                title='Bottom 10: Lowest Utilization Software',
                labels={'utilization_rate': 'Utilization %', 'index': 'Software'},
                color='utilization_rate',
                color_continuous_scale='Reds_r'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Cost per active user
            fig = px.scatter(
                comparison,
                x='avg_utilization',
                y='actual_cost_per_active_user',
                size='annual_spend',
                color='utilization_category',
                title='Utilization vs. Cost per Active User',
                labels={'avg_utilization': 'Utilization %', 'actual_cost_per_active_user': 'Cost per Active User ($)'},
                hover_data=['vendor_name']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Waste analysis
        st.markdown('<p class="medium-font"> License Waste Analysis</p>', unsafe_allow_html=True)
        waste_df = comparison[comparison['optimization_opportunity'] == 'Yes'][
            ['vendor_name', 'annual_spend', 'avg_utilization', 'licenses']
        ].copy()
        waste_df['wasted_spend'] = waste_df['annual_spend'] * (1 - waste_df['avg_utilization']/100)
        waste_df['wasted_licenses'] = (waste_df['licenses'] * (1 - waste_df['avg_utilization']/100)).astype(int)
        
        st.dataframe(
            waste_df.style.format({
                'annual_spend': '${:,.0f}',
                'wasted_spend': '${:,.0f}',
                'avg_utilization': '{:.0f}%'
            }),
            use_container_width=True
        )
    
    with tab2:
        st.subheader("Return on Investment Analysis")
        
        # ROI waterfall chart using graph_objects
        fig = go.Figure(go.Waterfall(
            name="ROI",
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "total"],
            x=["Annual Cost", "Labor Savings", "Error Reduction", "Productivity Gains", "Net ROI"],
            textposition="outside",
            text=[f"${abs(x):,.0f}" for x in [
                -roi['annual_cost'].sum(),
                roi['labor_cost_savings'].sum(),
                roi['error_reduction_savings'].sum(),
                roi['productivity_gains'].sum(),
                roi['net_benefit'].sum()
            ]],
            y=[
                -roi['annual_cost'].sum(),
                roi['labor_cost_savings'].sum(),
                roi['error_reduction_savings'].sum(),
                roi['productivity_gains'].sum(),
                roi['net_benefit'].sum()
            ],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        
        fig.update_layout(
            title="IT Investment ROI Breakdown",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top ROI systems
        col1, col2 = st.columns(2)
        
        with col1:
            top_roi = roi.nlargest(5, 'roi_percentage')[['vendor_name', 'roi_percentage', 'payback_period_months']]
            fig = px.bar(
                top_roi,
                x='vendor_name',
                y='roi_percentage',
                title='Top 5 Systems by ROI %',
                labels={'roi_percentage': 'ROI %', 'vendor_name': 'System'},
                text='roi_percentage'
            )
            fig.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Payback period
            fig = px.scatter(
                roi,
                x='payback_period_months',
                y='roi_percentage',
                size='annual_cost',
                title='Payback Period vs ROI',
                labels={'payback_period_months': 'Payback (Months)', 'roi_percentage': 'ROI %'},
                hover_data=['vendor_name']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Efficiency & Productivity Gains")
        
        # Process improvements
        fig = px.bar(
            efficiency.sort_values('hours_saved_per_user_monthly', ascending=True),
            y='system_name',
            x='hours_saved_per_user_monthly',
            orientation='h',
            title='Monthly Hours Saved per User by System',
            color='impact_level',
            color_discrete_map={'Critical': '#ff4444', 'High': '#ffaa00', 'Medium': '#00aa00'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Efficiency metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("** Key Efficiency Gains:**")
            for _, row in efficiency.iterrows():
                st.markdown(f" **{row['system_name']}**: {row['process_improved']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Adoption vs satisfaction
            fig = px.scatter(
                efficiency,
                x='adoption_rate',
                y='user_satisfaction_score',
                size='hours_saved_per_user_monthly',
                title='Adoption Rate vs User Satisfaction',
                labels={'adoption_rate': 'Adoption %', 'user_satisfaction_score': 'Satisfaction Score'},
                hover_data=['system_name']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("User Satisfaction Analysis")
        
        # Department satisfaction
        dept_satisfaction = satisfaction.groupby('department')['satisfaction_score'].mean().sort_values()
        
        fig = px.bar(
            x=dept_satisfaction.values,
            y=dept_satisfaction.index,
            orientation='h',
            title='Average Satisfaction by Department',
            labels={'x': 'Satisfaction Score', 'y': 'Department'},
            color=dept_satisfaction.values,
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Satisfaction components
        satisfaction_metrics = satisfaction.groupby('vendor_name').agg({
            'satisfaction_score': 'mean',
            'would_recommend': 'mean',
            'ease_of_use': 'mean',
            'meets_needs': 'mean'
        }).round(2)
        
        # Bottom performers
        bottom_satisfaction = satisfaction_metrics.nsmallest(5, 'satisfaction_score')
        st.markdown("** Systems Requiring Attention (Lowest Satisfaction):**")
        st.dataframe(
            bottom_satisfaction.style.format({
                'satisfaction_score': '{:.1f}',
                'would_recommend': '{:.0f}%',
                'ease_of_use': '{:.1f}',
                'meets_needs': '{:.0f}%'
            }),
            use_container_width=True
        )
    
    # Executive Insights
    st.markdown("---")
    st.markdown('<p class="big-font"> Executive Action Items</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("** Immediate Actions:**")
        st.markdown(f" Eliminate {int(comparison['licenses'].sum() * 0.3)} unused licenses")
        st.markdown(f" Save ${comparison[comparison['avg_utilization'] < 50]['annual_spend'].sum():,.0f}")
        st.markdown(" Focus on bottom 5 utilization systems")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("** Success Stories:**")
        st.markdown(f" {roi['roi_percentage'].max():.0f}% ROI on top system")
        st.markdown(f" {roi['labor_hours_saved'].sum()/2080:.0f} FTEs worth of time saved")
        st.markdown(f" {efficiency['process_error_reduction'].mean():.0f}% error reduction")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("** Optimization Targets:**")
        st.markdown(" Increase utilization to 75%+")
        st.markdown(" Improve satisfaction to 4.5/5")
        st.markdown(" Reduce payback to <12 months")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

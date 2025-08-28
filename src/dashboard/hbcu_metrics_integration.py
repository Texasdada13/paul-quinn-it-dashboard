# hbcu_metrics_integration.py
"""
HBCU Metrics Integration Module for Paul Quinn College IT Analytics Suite
Integrates institutional HBCU metrics across existing CFO, CIO, CTO personas
"""

import pandas as pd
import streamlit as st
from typing import Dict, List, Any
import plotly.express as px
import plotly.graph_objects as go

class HBCUMetricsIntegrator:
    """
    Integrates HBCU-specific institutional metrics with existing persona-based dashboards
    """
    
    def __init__(self):
        self.hbcu_metrics = self._load_hbcu_metrics()
        self.persona_mappings = self._define_persona_mappings()
    
    def _load_hbcu_metrics(self) -> Dict[str, pd.DataFrame]:
        """Load all HBCU CSV files into organized DataFrames"""
        import os
        base_path = os.path.join(os.path.dirname(__file__), '..', 'metrics', 'hbcu')
        try:
            return {
                'cost_efficiency': pd.read_csv(os.path.join(base_path, 'hbcu_cost_per_student_served_examples.csv')),
                'grant_compliance': pd.read_csv(os.path.join(base_path, 'hbcu_grant_compliance_tracking_examples.csv')),
                'resource_maximization': pd.read_csv(os.path.join(base_path, 'hbcu_resource_maximization_examples.csv')),
                'student_success_roi': pd.read_csv(os.path.join(base_path, 'hbcu_student_success_roi_examples.csv'))
            }
        except FileNotFoundError as e:
            st.warning(f"HBCU metrics file not found: {e}")
            return {}
    
    def _define_persona_mappings(self) -> Dict[str, Dict[str, List[str]]]:
        """Define which HBCU metrics map to each persona"""
        return {
            'cfo': {
                'cost_efficiency': [
                    'Cost Per Student Served',
                    'Cost Per Pell Student Served',
                    'Benchmark Comparison Per Student Cost',
                    'Year-over-Year Per Student Cost Trend'
                ],
                'grant_compliance': [
                    'Compliance Rate by Grant Type',
                    'Audit Exception Rate',
                    'Unspent Grant Funds',
                    'Grant Risk Score'
                ],
                'resource_maximization': [
                    'Instructional Spending Ratio',
                    'Federal/State Funding Ratio',
                    'Academic vs. Admin Spend Ratio',
                    'Cost Per Degree Awarded'
                ]
            },
            'cio': {
                'student_success_roi': [
                    'Technology-Linked Graduation Rate',
                    'Technology-Linked Retention Rate',
                    'Faculty Adoption Rate',
                    'Student Engagement Index'
                ],
                'resource_maximization': [
                    'Mission Alignment Index',
                    'Peer Benchmark (Instructional %)',
                    'Instructional Spend Trend (5y)'
                ]
            },
            'cto': {
                'student_success_roi': [
                    'Tech Intervention Cost per Graduate',
                    'Digital Literacy Test Improvement',
                    'Program Completion Rate',
                    'Minority/URM Student Tech Support Utilization'
                ],
                'cost_efficiency': [
                    'IT Services Cost Per Student',
                    'Efficiency Ratio (IT)',
                    'Student Satisfaction With Services'
                ]
            }
        }
    
    def get_persona_hbcu_metrics(self, persona: str) -> Dict[str, pd.DataFrame]:
        """Get HBCU metrics filtered for specific persona"""
        if persona not in self.persona_mappings:
            return {}
        
        persona_metrics = {}
        for category, metric_names in self.persona_mappings[persona].items():
            if category in self.hbcu_metrics:
                df = self.hbcu_metrics[category]
                filtered_df = df[df['Metric'].isin(metric_names)]
                if not filtered_df.empty:
                    persona_metrics[category] = filtered_df
        
        return persona_metrics
    
    def render_hbcu_dashboard_section(self, persona: str):
        """Render HBCU metrics section for persona dashboard"""
        st.markdown("### 🎓 HBCU Institutional Metrics")
        
        hbcu_metrics = self.get_persona_hbcu_metrics(persona)
        
        if not hbcu_metrics:
            st.info("No HBCU metrics configured for this persona.")
            return
        
        # Create tabs for different HBCU metric categories
        if len(hbcu_metrics) > 1:
            tabs = st.tabs([self._format_category_name(cat) for cat in hbcu_metrics.keys()])
            for tab, (category, df) in zip(tabs, hbcu_metrics.items()):
                with tab:
                    self._render_metric_category(category, df, persona)
        else:
            category, df = list(hbcu_metrics.items())[0]
            self._render_metric_category(category, df, persona)
    
    def _render_metric_category(self, category: str, df: pd.DataFrame, persona: str):
        """Render individual HBCU metric category"""
        st.markdown(f"#### {self._format_category_name(category)}")
        
        # Key metrics cards
        cols = st.columns(min(3, len(df)))
        for idx, (_, row) in enumerate(df.head(3).iterrows()):
            with cols[idx % 3]:
                self._render_metric_card(row['Metric'], row['Example'], category)
        
        # Detailed metrics table
        if len(df) > 3:
            with st.expander("View All Metrics"):
                st.dataframe(
                    df[['Metric', 'Description', 'Example']],
                    use_container_width=True,
                    hide_index=True
                )
        
        # Category-specific visualizations
        self._render_category_visualization(category, df, persona)
    
    def _render_metric_card(self, metric_name: str, value: str, category: str):
        """Render individual metric card with HBCU styling"""
        # Color coding by category
        colors = {
            'cost_efficiency': '#1f77b4',
            'grant_compliance': '#ff7f0e', 
            'resource_maximization': '#2ca02c',
            'student_success_roi': '#d62728'
        }
        
        color = colors.get(category, '#333333')
        
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, {color}15, {color}05);
                border-left: 4px solid {color};
                padding: 1rem;
                margin: 0.5rem 0;
                border-radius: 0.5rem;
            ">
                <h4 style="margin: 0; color: {color}; font-size: 0.9rem;">{metric_name}</h4>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; font-weight: bold;">{value}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    def _render_category_visualization(self, category: str, df: pd.DataFrame, persona: str):
        """Render visualizations specific to HBCU metric categories"""
        
        if category == 'cost_efficiency' and persona == 'cfo':
            self._render_cost_efficiency_chart(df)
        elif category == 'student_success_roi' and persona == 'cio':
            self._render_student_success_chart(df)
        elif category == 'grant_compliance' and persona == 'cfo':
            self._render_compliance_gauge(df)
    
    def _render_cost_efficiency_chart(self, df: pd.DataFrame):
        """Render cost efficiency comparison chart"""
        # Extract benchmark comparison data
        benchmark_row = df[df['Metric'] == 'Benchmark Comparison Per Student Cost']
        if not benchmark_row.empty:
            # Parse "HBCU: $8,224, Peer: $13,650" format
            import re
            value = benchmark_row.iloc[0]['Example']
            matches = re.findall(r'(\w+): \$([0-9,]+)', value)
            
            if len(matches) >= 2:
                data = {
                    'Institution Type': [match[0] for match in matches],
                    'Cost per Student': [int(match[1].replace(',', '')) for match in matches]
                }
                
                fig = px.bar(
                    data, 
                    x='Institution Type', 
                    y='Cost per Student',
                    title='Cost per Student: HBCU vs Peer Comparison',
                    color='Institution Type',
                    color_discrete_map={'HBCU': '#2ca02c', 'Peer': '#ff7f0e'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_student_success_chart(self, df: pd.DataFrame):
        """Render student success metrics radar chart"""
        success_metrics = df[df['Metric'].str.contains('Rate|Index')]['Metric'].tolist()
        
        if len(success_metrics) >= 3:
            # Create sample data for radar chart
            metrics = success_metrics[:5]  # Limit to 5 for readability
            values = [85, 78, 92, 88, 76]  # Sample values
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=metrics,
                fill='toself',
                name='Paul Quinn College',
                line_color='#2ca02c'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100])
                ),
                title="Student Success Metrics Overview",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_compliance_gauge(self, df: pd.DataFrame):
        """Render grant compliance gauge chart"""
        compliance_row = df[df['Metric'] == 'Compliance Rate by Grant Type']
        if not compliance_row.empty:
            # Extract average compliance rate (simplified)
            value = compliance_row.iloc[0]['Example']
            # Parse "Federal: 96%, Foundation: 92%" to get average
            import re
            percentages = re.findall(r'(\d+)%', value)
            if percentages:
                avg_compliance = sum(int(p) for p in percentages) / len(percentages)
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = avg_compliance,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Grant Compliance Rate"},
                    delta = {'reference': 90},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#2ca02c"},
                        'steps': [
                            {'range': [0, 70], 'color': "#ffcccc"},
                            {'range': [70, 90], 'color': "#fff3cd"},
                            {'range': [90, 100], 'color': "#d4edda"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 95
                        }
                    }
                ))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    def _format_category_name(self, category: str) -> str:
        """Format category names for display"""
        return category.replace('_', ' ').title()
    
    def render_institutional_hbcu_view(self):
        """Render comprehensive HBCU institutional dashboard"""
        st.markdown("# 🎓 HBCU Institutional Performance Dashboard")
        st.markdown("*Paul Quinn College Mission-Aligned Metrics*")
        
        # Executive summary cards
        st.markdown("## Executive Summary")
        cols = st.columns(4)
        
        with cols[0]:
            st.metric(
                "Students Served", 
                "5,800", 
                "↑ 3.2%",
                help="Total undergraduate enrollment"
            )
        
        with cols[1]:
            st.metric(
                "Cost per Student", 
                "$8,224", 
                "↓ $426",
                help="40% below peer average"
            )
        
        with cols[2]:
            st.metric(
                "Grant Compliance", 
                "94%", 
                "↑ 2%",
                help="Federal and foundation grants"
            )
        
        with cols[3]:
            st.metric(
                "Tech-Enabled Graduation", 
                "78%", 
                "↑ 5%",
                help="Technology intervention impact"
            )
        
        # Full metrics by category
        st.markdown("## Detailed Institutional Metrics")
        
        for category, df in self.hbcu_metrics.items():
            with st.expander(f"📊 {self._format_category_name(category)} ({len(df)} metrics)"):
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Add download button for each category
                csv = df.to_csv(index=False)
                st.download_button(
                    f"Download {self._format_category_name(category)} CSV",
                    csv,
                    f"pqc_{category}_metrics.csv",
                    "text/csv"
                )

# Integration helper functions
def integrate_hbcu_metrics_into_persona(persona_dashboard_func):
    """Decorator to integrate HBCU metrics into existing persona dashboards"""
    def wrapper(*args, **kwargs):
        # Render original persona dashboard
        result = persona_dashboard_func(*args, **kwargs)
        
        # Add HBCU metrics section
        integrator = HBCUMetricsIntegrator()
        persona_name = kwargs.get('persona', 'unknown')
        integrator.render_hbcu_dashboard_section(persona_name)
        
        return result
    return wrapper

def add_hbcu_institutional_nav():
    """Add HBCU institutional view to navigation"""
    if st.sidebar.button("🎓 HBCU Institutional View"):
        st.session_state.current_view = 'hbcu_institutional'

# Example usage in existing dashboard
if __name__ == "__main__":
    # Initialize integrator
    integrator = HBCUMetricsIntegrator()
    
    # Demo: Render CFO view with HBCU metrics
    st.title("CFO Dashboard with HBCU Integration")
    integrator.render_hbcu_dashboard_section('cfo')
    
    st.markdown("---")
    
    # Demo: Full institutional view
    integrator.render_institutional_hbcu_view()
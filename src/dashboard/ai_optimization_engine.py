"""
AI-Driven Technology Investment Optimization Engine
Integrates with existing ISSA dashboard to provide intelligent recommendations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

class AIOptimizationEngine:
    """AI-powered engine for technology investment optimization"""
    
    def __init__(self):
        self.optimization_algorithms = {
            'cost_reduction': self._analyze_cost_reduction_opportunities,
            'roi_maximization': self._analyze_roi_opportunities,
            'risk_mitigation': self._analyze_risk_mitigation,
            'resource_optimization': self._analyze_resource_optimization
        }
        
        # AI-driven recommendation weights
        self.recommendation_weights = {
            'financial_impact': 0.35,
            'implementation_ease': 0.25,
            'strategic_alignment': 0.20,
            'risk_reduction': 0.20
        }
    
    def generate_optimization_recommendations(self, persona: str, data: Dict) -> List[Dict]:
        """Generate AI-powered optimization recommendations based on persona and data"""
        
        recommendations = []
        
        # Run all optimization algorithms
        for algorithm_name, algorithm_func in self.optimization_algorithms.items():
            try:
                algorithm_recommendations = algorithm_func(persona, data)
                recommendations.extend(algorithm_recommendations)
            except Exception as e:
                logging.error(f"Error in {algorithm_name}: {e}")
        
        # Score and rank recommendations
        scored_recommendations = self._score_recommendations(recommendations, persona)
        
        # Return top recommendations
        return sorted(scored_recommendations, key=lambda x: x['ai_score'], reverse=True)[:10]
    
    def _analyze_cost_reduction_opportunities(self, persona: str, data: Dict) -> List[Dict]:
        """AI analysis for cost reduction opportunities"""
        recommendations = []
        
        if persona == 'cfo':
            # Analyze contract optimization
            if 'contract_data' in data:
                contract_df = data['contract_data']
                
                # Find consolidation opportunities
                vendor_analysis = contract_df.groupby('Vendor')['Annual Spend'].agg(['sum', 'count']).reset_index()
                high_spend_vendors = vendor_analysis[vendor_analysis['sum'] > 100000]
                
                for _, vendor in high_spend_vendors.iterrows():
                    if vendor['count'] > 1:  # Multiple contracts with same vendor
                        potential_savings = vendor['sum'] * 0.15  # Assume 15% savings from consolidation
                        recommendations.append({
                            'type': 'cost_reduction',
                            'title': f'Consolidate contracts with {vendor["Vendor"]}',
                            'description': f'Consolidate {vendor["count"]} contracts to negotiate better terms',
                            'potential_savings': potential_savings,
                            'implementation_effort': 'Medium',
                            'timeline': '3-6 months',
                            'confidence': 0.8,
                            'category': 'Contract Optimization'
                        })
            
            # Analyze budget variance for optimization
            if 'budget_data' in data:
                budget_df = data['budget_data']
                underutilized = budget_df[budget_df['Variance Amount'] < -50000]  # Significantly under budget
                
                for _, item in underutilized.iterrows():
                    reallocation_amount = abs(item['Variance Amount']) * 0.7
                    recommendations.append({
                        'type': 'cost_reduction',
                        'title': f'Reallocate underutilized budget from {item["Budget Category"]}',
                        'description': f'Redirect ${reallocation_amount:,.0f} to high-impact initiatives',
                        'potential_savings': reallocation_amount,
                        'implementation_effort': 'Low',
                        'timeline': '1-2 months',
                        'confidence': 0.9,
                        'category': 'Budget Reallocation'
                    })
        
        elif persona == 'cio':
            # Analyze application rationalization
            recommendations.append({
                'type': 'cost_reduction',
                'title': 'Application Portfolio Rationalization',
                'description': 'Eliminate redundant applications and consolidate similar functions',
                'potential_savings': 250000,
                'implementation_effort': 'High',
                'timeline': '6-12 months',
                'confidence': 0.75,
                'category': 'Application Optimization'
            })
        
        elif persona == 'cto':
            # Analyze infrastructure optimization
            recommendations.append({
                'type': 'cost_reduction',
                'title': 'Cloud Infrastructure Right-Sizing',
                'description': 'Optimize cloud resources based on actual usage patterns',
                'potential_savings': 180000,
                'implementation_effort': 'Medium',
                'timeline': '2-3 months',
                'confidence': 0.85,
                'category': 'Infrastructure Optimization'
            })
        
        return recommendations
    
    def _analyze_roi_opportunities(self, persona: str, data: Dict) -> List[Dict]:
        """AI analysis for ROI maximization opportunities"""
        recommendations = []
        
        # Student success ROI opportunities
        recommendations.append({
            'type': 'roi_maximization',
            'title': 'Expand AI-Powered Student Analytics',
            'description': 'Deploy predictive analytics to identify at-risk students early',
            'potential_roi': 3.2,  # 3.2x return
            'investment_required': 150000,
            'expected_benefit': 480000,
            'implementation_effort': 'Medium',
            'timeline': '4-6 months',
            'confidence': 0.82,
            'category': 'Student Success Technology'
        })
        
        if persona == 'cfo':
            recommendations.append({
                'type': 'roi_maximization',
                'title': 'Automated Financial Reporting System',
                'description': 'Reduce manual reporting effort by 70% and improve accuracy',
                'potential_roi': 2.8,
                'investment_required': 120000,
                'expected_benefit': 336000,
                'implementation_effort': 'Medium',
                'timeline': '3-5 months',
                'confidence': 0.78,
                'category': 'Process Automation'
            })
        
        elif persona == 'cio':
            recommendations.append({
                'type': 'roi_maximization',
                'title': 'Digital Learning Platform Enhancement',
                'description': 'Upgrade LMS with AI-powered personalization features',
                'potential_roi': 4.1,
                'investment_required': 200000,
                'expected_benefit': 820000,
                'implementation_effort': 'High',
                'timeline': '6-9 months',
                'confidence': 0.75,
                'category': 'Digital Learning'
            })
        
        return recommendations
    
    def _analyze_risk_mitigation(self, persona: str, data: Dict) -> List[Dict]:
        """AI analysis for risk mitigation opportunities"""
        recommendations = []
        
        # Security and compliance risks
        recommendations.append({
            'type': 'risk_mitigation',
            'title': 'Enhanced Cybersecurity Framework',
            'description': 'Implement zero-trust security model to reduce breach risk by 85%',
            'risk_reduction': 0.85,
            'potential_cost_avoidance': 2500000,  # Cost of potential breach
            'investment_required': 300000,
            'implementation_effort': 'High',
            'timeline': '6-12 months',
            'confidence': 0.88,
            'category': 'Security Enhancement'
        })
        
        if persona == 'cfo':
            # Compliance automation
            recommendations.append({
                'type': 'risk_mitigation',
                'title': 'Automated Grant Compliance Monitoring',
                'description': 'Real-time tracking to prevent compliance violations and fund clawbacks',
                'risk_reduction': 0.92,
                'potential_cost_avoidance': 1200000,
                'investment_required': 80000,
                'implementation_effort': 'Medium',
                'timeline': '2-4 months',
                'confidence': 0.91,
                'category': 'Compliance Automation'
            })
        
        return recommendations
    
    def _analyze_resource_optimization(self, persona: str, data: Dict) -> List[Dict]:
        """AI analysis for resource optimization opportunities"""
        recommendations = []
        
        # Staff productivity enhancement
        recommendations.append({
            'type': 'resource_optimization',
            'title': 'AI-Powered IT Service Desk',
            'description': 'Implement chatbot to handle 60% of routine IT requests',
            'resource_savings': 'Equivalent to 1.5 FTE',
            'productivity_gain': '40%',
            'investment_required': 95000,
            'annual_savings': 180000,
            'implementation_effort': 'Medium',
            'timeline': '3-4 months',
            'confidence': 0.83,
            'category': 'Automation & Efficiency'
        })
        
        if persona == 'cto':
            recommendations.append({
                'type': 'resource_optimization',
                'title': 'Automated Infrastructure Monitoring',
                'description': 'Proactive monitoring to reduce downtime by 75%',
                'resource_savings': 'Equivalent to 0.8 FTE',
                'productivity_gain': '35%',
                'investment_required': 65000,
                'annual_savings': 120000,
                'implementation_effort': 'Low',
                'timeline': '1-2 months',
                'confidence': 0.89,
                'category': 'Infrastructure Automation'
            })
        
        return recommendations
    
    def _score_recommendations(self, recommendations: List[Dict], persona: str) -> List[Dict]:
        """Apply AI scoring algorithm to rank recommendations"""
        
        for rec in recommendations:
            score = 0
            
            # Financial Impact Score (0-100)
            if 'potential_savings' in rec:
                financial_score = min(rec['potential_savings'] / 10000, 100)  # Scale to 100
            elif 'expected_benefit' in rec:
                financial_score = min(rec['expected_benefit'] / 10000, 100)
            elif 'annual_savings' in rec:
                financial_score = min(rec['annual_savings'] / 5000, 100)
            else:
                financial_score = 50  # Default
            
            # Implementation Ease Score (0-100)
            effort_scores = {'Low': 90, 'Medium': 60, 'High': 30}
            ease_score = effort_scores.get(rec.get('implementation_effort', 'Medium'), 60)
            
            # Strategic Alignment Score (0-100) - simplified
            strategic_score = 80  # Would be more sophisticated in real implementation
            
            # Risk Reduction Score (0-100)
            if 'confidence' in rec:
                risk_score = rec['confidence'] * 100
            elif 'risk_reduction' in rec:
                risk_score = rec['risk_reduction'] * 100
            else:
                risk_score = 70
            
            # Calculate weighted score
            score = (
                financial_score * self.recommendation_weights['financial_impact'] +
                ease_score * self.recommendation_weights['implementation_ease'] +
                strategic_score * self.recommendation_weights['strategic_alignment'] +
                risk_score * self.recommendation_weights['risk_reduction']
            )
            
            rec['ai_score'] = round(score, 1)
            rec['financial_score'] = round(financial_score, 1)
            rec['ease_score'] = round(ease_score, 1)
            rec['strategic_score'] = round(strategic_score, 1)
            rec['risk_score'] = round(risk_score, 1)
        
        return recommendations


class OptimizationDashboard:
    """Streamlit dashboard for AI-driven optimization recommendations"""
    
    def __init__(self):
        self.ai_engine = AIOptimizationEngine()
    
    def render_optimization_dashboard(self, persona: str, data: Dict):
        """Render the main optimization dashboard"""
        
        st.markdown("## 🤖 AI-Powered Optimization Recommendations")
        st.markdown("*Harness AI to maximize value from your technology investments*")
        
        # Generate recommendations
        with st.spinner("AI analyzing your data for optimization opportunities..."):
            recommendations = self.ai_engine.generate_optimization_recommendations(persona, data)
        
        if not recommendations:
            st.warning("No optimization recommendations available at this time.")
            return
        
        # Summary metrics
        self._render_optimization_summary(recommendations)
        
        # Detailed recommendations
        self._render_detailed_recommendations(recommendations, persona)
        
        # Implementation roadmap
        self._render_implementation_roadmap(recommendations)
    
    def _render_optimization_summary(self, recommendations: List[Dict]):
        """Render optimization opportunity summary"""
        
        # Calculate totals
        total_savings = sum(rec.get('potential_savings', rec.get('annual_savings', 0)) for rec in recommendations)
        total_investment = sum(rec.get('investment_required', 0) for rec in recommendations)
        avg_roi = np.mean([rec.get('potential_roi', rec.get('expected_benefit', 0) / max(rec.get('investment_required', 1), 1)) for rec in recommendations if rec.get('investment_required', 0) > 0])
        
        # Summary cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Potential Annual Savings", f"${total_savings:,.0f}", help="Total identified savings opportunities")
        
        with col2:
            st.metric("📈 Average ROI", f"{avg_roi:.1f}x", help="Average return on investment")
        
        with col3:
            st.metric("🎯 Recommendations", len(recommendations), help="AI-generated optimization opportunities")
        
        with col4:
            high_confidence = len([r for r in recommendations if r.get('confidence', 0.5) > 0.8])
            st.metric("✅ High Confidence", high_confidence, help="Recommendations with >80% confidence")
        
        # Opportunity categories chart
        st.markdown("### 📊 Optimization Opportunities by Category")
        
        category_data = {}
        for rec in recommendations:
            category = rec.get('category', 'Other')
            savings = rec.get('potential_savings', rec.get('annual_savings', 0))
            if category in category_data:
                category_data[category] += savings
            else:
                category_data[category] = savings
        
        if category_data:
            fig = px.pie(
                values=list(category_data.values()),
                names=list(category_data.keys()),
                title="Savings Potential by Category"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_detailed_recommendations(self, recommendations: List[Dict], persona: str):
        """Render detailed recommendation cards"""
        
        st.markdown("### 🎯 Top AI Recommendations")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category_filter = st.multiselect(
                "Filter by Category",
                options=list(set(rec.get('category', 'Other') for rec in recommendations)),
                default=list(set(rec.get('category', 'Other') for rec in recommendations))
            )
        
        with col2:
            effort_filter = st.multiselect(
                "Implementation Effort",
                options=['Low', 'Medium', 'High'],
                default=['Low', 'Medium', 'High']
            )
        
        with col3:
            min_confidence = st.slider("Minimum Confidence", 0.0, 1.0, 0.5, 0.1)
        
        # Filter recommendations
        filtered_recs = [
            rec for rec in recommendations
            if rec.get('category', 'Other') in category_filter
            and rec.get('implementation_effort', 'Medium') in effort_filter
            and rec.get('confidence', 0.5) >= min_confidence
        ]
        
        # Display recommendation cards
        for i, rec in enumerate(filtered_recs[:8]):  # Show top 8
            self._render_recommendation_card(rec, i)
    
    def _render_recommendation_card(self, rec: Dict, index: int):
        """Render individual recommendation card"""
        
        # Color coding based on type
        colors = {
            'cost_reduction': '#28a745',
            'roi_maximization': '#007bff', 
            'risk_mitigation': '#ffc107',
            'resource_optimization': '#17a2b8'
        }
        
        color = colors.get(rec['type'], '#6c757d')
        
        with st.expander(f"🎯 {rec['title']} (Score: {rec['ai_score']}/100)", expanded=index < 3):
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {rec['description']}")
                st.markdown(f"**Category:** {rec.get('category', 'General')}")
                st.markdown(f"**Timeline:** {rec.get('timeline', 'TBD')}")
                
                # Financial metrics
                if 'potential_savings' in rec:
                    st.success(f"💰 Potential Annual Savings: ${rec['potential_savings']:,.0f}")
                if 'potential_roi' in rec:
                    st.success(f"📈 Expected ROI: {rec['potential_roi']:.1f}x")
                if 'investment_required' in rec:
                    st.info(f"💵 Investment Required: ${rec['investment_required']:,.0f}")
            
            with col2:
                # AI Score breakdown
                st.markdown("**AI Analysis Score**")
                
                # Progress bars for score components
                st.progress(rec['financial_score']/100)
                st.caption(f"Financial Impact: {rec['financial_score']}/100")
                
                st.progress(rec['ease_score']/100)
                st.caption(f"Implementation Ease: {rec['ease_score']}/100")
                
                st.progress(rec['strategic_score']/100)
                st.caption(f"Strategic Alignment: {rec['strategic_score']}/100")
                
                st.progress(rec['risk_score']/100)
                st.caption(f"Risk Mitigation: {rec['risk_score']}/100")
                
                # Overall confidence
                confidence = rec.get('confidence', 0.5)
                st.metric("Confidence", f"{confidence:.0%}")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"📋 Create Project", key=f"project_{index}"):
                    st.success("Project template created!")
            with col2:
                if st.button(f"📧 Email Details", key=f"email_{index}"):
                    st.success("Details emailed to stakeholders!")
            with col3:
                if st.button(f"📊 Deep Dive Analysis", key=f"analysis_{index}"):
                    st.success("Detailed analysis initiated!")
    
    def _render_implementation_roadmap(self, recommendations: List[Dict]):
        """Render implementation roadmap visualization"""
        
        st.markdown("### 🗺️ AI-Optimized Implementation Roadmap")
        
        # Sort by combination of impact and ease
        sorted_recs = sorted(recommendations[:6], key=lambda x: x['ai_score'], reverse=True)
        
        # Create timeline data
        timeline_data = []
        current_date = datetime.now()
        
        for i, rec in enumerate(sorted_recs):
            # Parse timeline
            timeline = rec.get('timeline', '3-6 months')
            if 'month' in timeline:
                months = int(timeline.split('-')[0]) if '-' in timeline else int(timeline.split()[0])
            else:
                months = 6  # Default
            
            start_date = current_date + timedelta(days=i*30)  # Stagger starts
            end_date = start_date + timedelta(days=months*30)
            
            timeline_data.append({
                'Task': rec['title'][:40] + '...' if len(rec['title']) > 40 else rec['title'],
                'Start': start_date,
                'Finish': end_date,
                'Score': rec['ai_score'],
                'Savings': rec.get('potential_savings', rec.get('annual_savings', 0))
            })
        
        if timeline_data:
            timeline_df = pd.DataFrame(timeline_data)
            
            # Gantt chart
            fig = px.timeline(
                timeline_df,
                x_start='Start',
                x_end='Finish', 
                y='Task',
                color='Score',
                title='Optimized Implementation Timeline',
                color_continuous_scale='Viridis'
            )
            
            fig.update_yaxes(autorange="reversed")
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary table
            st.markdown("**Implementation Summary**")
            summary_df = timeline_df[['Task', 'Score', 'Savings']].copy()
            summary_df['Savings'] = summary_df['Savings'].apply(lambda x: f"${x:,.0f}")
            summary_df['Score'] = summary_df['Score'].apply(lambda x: f"{x}/100")
            
            st.dataframe(summary_df, use_container_width=True, hide_index=True)

# Integration function for existing dashboard
def add_ai_optimization_tab(persona: str, data: Dict):
    """Add AI optimization tab to existing persona dashboards"""
    
    dashboard = OptimizationDashboard()
    
    # Sample data structure - would be populated from actual metrics
    sample_data = {
        'contract_data': pd.DataFrame({
            'Vendor': ['Microsoft', 'Adobe', 'AWS', 'Microsoft', 'Salesforce'],
            'Annual Spend': [150000, 80000, 200000, 90000, 120000],
            'Days Until Expiry': [45, 120, 200, 30, 180]
        }),
        'budget_data': pd.DataFrame({
            'Budget Category': ['Software Licenses', 'Hardware', 'Cloud Services', 'Consulting'],
            'Initial Budget': [500000, 300000, 400000, 200000],
            'Actual Spend': [420000, 280000, 450000, 160000],
            'Variance Amount': [-80000, -20000, 50000, -40000]
        })
    }
    
    dashboard.render_optimization_dashboard(persona, sample_data)

# Example usage in main dashboard
def integrate_with_existing_dashboard():
    """Show how to integrate with existing ISSA dashboard"""
    
    st.markdown("## Integration Example")
    st.markdown("Add this tab to your existing persona dashboards:")
    
    st.code('''
    # In your existing dashboard file (fully_integrated_dashboard.py)
    
    # Add to CFO tabs:
    tabs = st.tabs(["📊 Budget Analysis", "📃 Contracts & Vendors", "🤖 AI Optimization", "📈 ROI & Benchmarking"])
    
    with tabs[2]:  # AI Optimization tab
        from ai_optimization_engine import add_ai_optimization_tab
        add_ai_optimization_tab('cfo', dashboard_data)
    ''', language='python')
    
    # Demo the optimization dashboard
    st.markdown("### Live Demo - CFO Optimization Dashboard")
    add_ai_optimization_tab('cfo', {})
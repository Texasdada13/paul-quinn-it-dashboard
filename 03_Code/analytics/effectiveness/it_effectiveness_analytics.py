"""
IT Effectiveness Analytics Framework
Based on JITM research themes and measures
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class ITEffectivenessAnalytics:
    """Comprehensive IT effectiveness measurement system"""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.load_data()
        
    def load_data(self):
        """Load all relevant data"""
        self.vendors = pd.read_csv(os.path.join(self.data_path, "clean_vendors.csv"))
        self.projects = pd.read_csv(os.path.join(self.data_path, "clean_projects.csv"))
        # Simulate additional data we'd collect in real implementation
        self.create_simulated_data()
    
    def create_simulated_data(self):
        """Create additional data for comprehensive analysis"""
        # Customer satisfaction scores
        self.satisfaction_data = pd.DataFrame({
            'department': ['IT', 'Finance', 'Academic Affairs', 'Student Services', 'Administration'],
            'satisfaction_score': np.random.uniform(3.5, 4.8, 5),
            'response_rate': np.random.uniform(0.6, 0.9, 5),
            'tickets_resolved': np.random.randint(50, 200, 5),
            'avg_resolution_time': np.random.uniform(2, 8, 5)
        })
        
        # System performance metrics
        self.system_metrics = pd.DataFrame({
            'system': ['ERP', 'LMS', 'Email', 'Network', 'Student Portal'],
            'availability_pct': np.random.uniform(98.5, 99.9, 5),
            'response_time_ms': np.random.uniform(100, 500, 5),
            'user_count': np.random.randint(100, 1000, 5),
            'incidents_monthly': np.random.randint(0, 10, 5)
        })
        
        # Employee engagement
        self.employee_data = pd.DataFrame({
            'team': ['Infrastructure', 'Applications', 'Support', 'Security', 'PMO'],
            'engagement_score': np.random.uniform(3.0, 4.5, 5),
            'training_hours': np.random.randint(10, 40, 5),
            'certifications': np.random.randint(0, 5, 5),
            'turnover_rate': np.random.uniform(0.05, 0.20, 5)
        })
    
    # THEME 1: Finance/ROI/Investments/Revenue
    def calculate_financial_effectiveness(self):
        """Calculate financial and ROI metrics"""
        metrics = {}
        
        # IT spend as % of revenue (benchmark: 3-5% for higher ed)
        total_revenue = 50000000  # $50M assumed for small college
        it_spend = self.vendors['annual_spend'].sum()
        metrics['it_spend_pct_revenue'] = (it_spend / total_revenue) * 100
        
        # Cost per student/employee
        total_users = 1500  # Assumed
        metrics['cost_per_user'] = it_spend / total_users
        
        # Project ROI
        project_benefits = self.projects['budget'].sum() * 1.5  # Assumed 1.5x return
        project_costs = self.projects['spent_to_date'].sum()
        metrics['project_roi'] = ((project_benefits - project_costs) / project_costs) * 100
        
        # Budget variance
        metrics['budget_variance'] = (
            (self.projects['budget'].sum() - self.projects['spent_to_date'].sum()) / 
            self.projects['budget'].sum() * 100
        )
        
        return pd.DataFrame([metrics])
    
    # THEME 2: Customers
    def calculate_customer_effectiveness(self):
        """Calculate customer-focused metrics"""
        metrics = {}
        
        # Overall satisfaction
        metrics['avg_satisfaction'] = self.satisfaction_data['satisfaction_score'].mean()
        
        # Net Promoter Score (simulated)
        metrics['nps_score'] = np.random.randint(20, 60)
        
        # Service adoption rate
        metrics['service_adoption_pct'] = (
            self.system_metrics['user_count'].sum() / 1500 * 100
        )
        
        # First-call resolution rate
        metrics['first_call_resolution'] = np.random.uniform(0.7, 0.85) * 100
        
        return pd.DataFrame([metrics])
    
    # THEME 3: Costs/Budgets
    def calculate_cost_effectiveness(self):
        """Calculate cost and budget efficiency metrics"""
        metrics = {}
        
        # Cost reduction YoY
        metrics['cost_reduction_pct'] = np.random.uniform(-5, 10)
        
        # Vendor consolidation opportunity
        unique_categories = self.vendors['category'].nunique()
        total_vendors = len(self.vendors)
        metrics['vendor_concentration'] = unique_categories / total_vendors
        
        # Budget utilization efficiency
        metrics['budget_efficiency'] = (
            self.projects[self.projects['risk_flag'] != 'HIGH']['budget_utilization_%'].mean()
        )
        
        # Cost avoidance through optimization
        metrics['cost_avoidance'] = self.vendors['annual_spend'].sum() * 0.1  # 10% potential
        
        return pd.DataFrame([metrics])
    
    # THEME 4: Satisfaction
    def calculate_satisfaction_effectiveness(self):
        """Calculate satisfaction metrics across stakeholders"""
        metrics = {}
        
        # Department satisfaction variance
        metrics['satisfaction_variance'] = self.satisfaction_data['satisfaction_score'].std()
        
        # Response rate
        metrics['avg_response_rate'] = self.satisfaction_data['response_rate'].mean() * 100
        
        # Satisfaction trend (simulated)
        metrics['satisfaction_trend'] = np.random.choice(['Improving', 'Stable', 'Declining'])
        
        # Employee satisfaction
        metrics['employee_satisfaction'] = self.employee_data['engagement_score'].mean()
        
        return pd.DataFrame([metrics])
    
    # THEME 5: Service
    def calculate_service_effectiveness(self):
        """Calculate service delivery metrics"""
        metrics = {}
        
        # System availability
        metrics['avg_availability'] = self.system_metrics['availability_pct'].mean()
        
        # SLA compliance
        metrics['sla_compliance'] = np.random.uniform(0.9, 0.98) * 100
        
        # Average resolution time
        metrics['avg_resolution_hours'] = self.satisfaction_data['avg_resolution_time'].mean()
        
        # Service catalog completeness
        metrics['service_catalog_items'] = np.random.randint(20, 40)
        
        # Incident reduction rate
        metrics['incident_reduction_pct'] = np.random.uniform(-10, 20)
        
        return pd.DataFrame([metrics])
    
    def generate_balanced_scorecard(self):
        """Generate a comprehensive balanced scorecard"""
        scorecard = {
            'Financial': self.calculate_financial_effectiveness(),
            'Customer': self.calculate_customer_effectiveness(),
            'Internal Process': self.calculate_cost_effectiveness(),
            'Learning & Growth': self.calculate_satisfaction_effectiveness(),
            'Service Delivery': self.calculate_service_effectiveness()
        }
        
        return scorecard
    
    def generate_executive_insights(self):
        """Generate AI-like insights for leadership"""
        insights = []
        
        # Financial insight
        roi = self.calculate_financial_effectiveness()['project_roi'].values[0]
        if roi > 20:
            insights.append(f"STRONG: Project ROI of {roi:.1f}% exceeds industry benchmark of 20%")
        else:
            insights.append(f"ATTENTION: Project ROI of {roi:.1f}% below industry benchmark")
        
        # Risk insight
        high_risk_count = len(self.projects[self.projects['risk_flag'] == 'HIGH'])
        if high_risk_count > 2:
            insights.append(f"RISK ALERT: {high_risk_count} projects at high risk require intervention")
        
        # Optimization insight
        vendor_savings = self.vendors['annual_spend'].sum() * 0.15
        insights.append(f"OPPORTUNITY: Vendor consolidation could save ${vendor_savings:,.0f} annually")
        
        # Service insight
        availability = self.system_metrics['availability_pct'].mean()
        if availability > 99.5:
            insights.append(f"EXCELLENT: System availability at {availability:.1f}% exceeds target")
        
        return insights

# Main execution
if __name__ == "__main__":
    print("IT Effectiveness Analytics Engine\n" + "="*50)
    
    # Initialize analytics
    analytics = ITEffectivenessAnalytics("02_Data/processed")
    
    # Generate all metrics
    print("\n1. FINANCIAL EFFECTIVENESS")
    financial = analytics.calculate_financial_effectiveness()
    print(financial.T)
    
    print("\n2. CUSTOMER EFFECTIVENESS")
    customer = analytics.calculate_customer_effectiveness()
    print(customer.T)
    
    print("\n3. COST EFFECTIVENESS")
    cost = analytics.calculate_cost_effectiveness()
    print(cost.T)
    
    print("\n4. SATISFACTION EFFECTIVENESS")
    satisfaction = analytics.calculate_satisfaction_effectiveness()
    print(satisfaction.T)
    
    print("\n5. SERVICE EFFECTIVENESS")
    service = analytics.calculate_service_effectiveness()
    print(service.T)
    
    print("\n" + "="*50)
    print("EXECUTIVE INSIGHTS (AI-Generated)")
    print("="*50)
    for insight in analytics.generate_executive_insights():
        print(f"• {insight}")
    
    # Save comprehensive results
    results = pd.concat([
        financial.T.rename(columns={0: 'value'}),
        customer.T.rename(columns={0: 'value'}),
        cost.T.rename(columns={0: 'value'}),
        satisfaction.T.rename(columns={0: 'value'}),
        service.T.rename(columns={0: 'value'})
    ])
    results.to_csv("02_Data/processed/it_effectiveness_metrics.csv")
    print(f"\nMetrics saved to: 02_Data/processed/it_effectiveness_metrics.csv")

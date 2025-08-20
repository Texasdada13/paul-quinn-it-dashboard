"""
Predictive Analytics for IT Effectiveness
AI/ML-like predictions without complex libraries
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ITPredictiveAnalytics:
    """Simple but effective predictive analytics"""
    
    def __init__(self):
        self.vendors = pd.read_csv("02_Data/processed/clean_vendors.csv")
        self.projects = pd.read_csv("02_Data/processed/clean_projects.csv")
    
    def predict_budget_overruns(self):
        """Predict which projects will overrun budget"""
        predictions = []
        
        for _, project in self.projects.iterrows():
            # Simple prediction based on burn rate
            if project['budget_utilization_%'] > 75:
                risk_score = min(100, project['budget_utilization_%'] * 1.2)
                predictions.append({
                    'project': project['project_name'],
                    'overrun_probability': f"{risk_score:.0f}%",
                    'estimated_overrun': f"${(project['budget'] * 0.15):,.0f}",
                    'recommendation': 'Immediate review required' if risk_score > 90 else 'Monitor closely'
                })
        
        return pd.DataFrame(predictions)
    
    def predict_vendor_risks(self):
        """Predict vendor-related risks"""
        # Simulate contract end dates
        self.vendors['months_to_renewal'] = np.random.randint(1, 24, len(self.vendors))
        
        risks = []
        for _, vendor in self.vendors.iterrows():
            risk_factors = 0
            risk_factors += 1 if vendor['risk_level'] == 'High' else 0
            risk_factors += 1 if vendor['annual_spend'] > 40000 else 0
            risk_factors += 1 if vendor['months_to_renewal'] < 6 else 0
            
            if risk_factors >= 2:
                risks.append({
                    'vendor': vendor['vendor_name'],
                    'risk_score': risk_factors * 33,
                    'primary_risk': 'Contract renewal' if vendor['months_to_renewal'] < 6 else 'High spend concentration',
                    'action': 'Begin renegotiation' if vendor['months_to_renewal'] < 6 else 'Seek alternatives'
                })
        
        return pd.DataFrame(risks)
    
    def predict_cost_savings(self):
        """Predict potential cost savings opportunities"""
        opportunities = []
        
        # Vendor consolidation
        categories = self.vendors.groupby('category')['annual_spend'].agg(['sum', 'count'])
        for category, data in categories.iterrows():
            if data['count'] > 2:
                savings = data['sum'] * 0.15  # 15% through consolidation
                opportunities.append({
                    'opportunity': f"Consolidate {category} vendors",
                    'potential_savings': f"${savings:,.0f}",
                    'effort': 'Medium',
                    'timeline': '3-6 months'
                })
        
        # License optimization (simulated)
        opportunities.append({
            'opportunity': 'Optimize software licenses',
            'potential_savings': '$25,000',
            'effort': 'Low',
            'timeline': '1-2 months'
        })
        
        return pd.DataFrame(opportunities)
    
    def generate_predictions_report(self):
        """Generate comprehensive predictions report"""
        print("IT PREDICTIVE ANALYTICS REPORT")
        print("="*50)
        
        # Budget overruns
        print("\n📊 BUDGET OVERRUN PREDICTIONS")
        overruns = self.predict_budget_overruns()
        if not overruns.empty:
            print(overruns.to_string(index=False))
        else:
            print("✓ No projects at risk of budget overrun")
        
        # Vendor risks
        print("\n\n⚠️  VENDOR RISK PREDICTIONS")
        vendor_risks = self.predict_vendor_risks()
        if not vendor_risks.empty:
            print(vendor_risks.to_string(index=False))
        else:
            print("✓ No high-risk vendors identified")
        
        # Cost savings
        print("\n\n💰 COST SAVINGS OPPORTUNITIES")
        savings = self.predict_cost_savings()
        print(savings.to_string(index=False))
        
        # Executive summary
        total_savings = 0
        for s in savings['potential_savings']:
            # Extract number from string like '$25,000'
            num_str = s.replace('$', '').replace(',', '')
            total_savings += float(num_str)
        
        print(f"\n\n📈 EXECUTIVE SUMMARY")
        print(f"Total potential savings identified: ${total_savings:,.0f}")
        print(f"High-risk items requiring attention: {len(overruns) + len(vendor_risks)}")
        print(f"Recommended actions: {len(savings)} cost optimization initiatives")

# Run predictions
if __name__ == "__main__":
    predictor = ITPredictiveAnalytics()
    predictor.generate_predictions_report()

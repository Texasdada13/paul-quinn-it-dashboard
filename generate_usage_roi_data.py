"""
Enhanced IT Effectiveness Analytics - Usage, Efficiency & ROI Tracking
This adds the critical missing pieces for true IT value measurement
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_usage_and_impact_data():
    """Generate comprehensive usage and efficiency data"""
    
    print("📊 Generating Usage, Efficiency & ROI Impact Data...")
    print("="*60)
    
    # Load existing vendor data to enhance
    vendors = pd.read_excel('PQC_Robust_Mock_Data.xlsx', sheet_name='Vendors')
    systems = pd.read_excel('PQC_Robust_Mock_Data.xlsx', sheet_name='Systems')
    
    # 1. SOFTWARE USAGE ANALYTICS
    print("\n1. Creating Software Usage Analytics...")
    
    usage_data = []
    for _, vendor in vendors.iterrows():
        # Generate monthly usage data
        for month in pd.date_range('2024-01-01', '2024-06-30', freq='ME'):
            # Different usage patterns based on software type
            if vendor['category'] == 'Enterprise Software':
                active_users = int(vendor['users'] * random.uniform(0.7, 0.95))
                login_frequency = random.uniform(15, 25)  # times per month
            elif vendor['category'] == 'Productivity':
                active_users = int(vendor['users'] * random.uniform(0.8, 1.0))
                login_frequency = random.uniform(20, 30)
            else:
                active_users = int(vendor['users'] * random.uniform(0.4, 0.8))
                login_frequency = random.uniform(5, 15)
            
            usage_data.append({
                'vendor_name': vendor['vendor_name'],
                'month': month,
                'licenses_purchased': vendor['users'],
                'active_users': active_users,
                'utilization_rate': (active_users / vendor['users'] * 100),
                'avg_logins_per_user': login_frequency,
                'avg_session_duration_mins': random.uniform(10, 120),
                'features_used_pct': random.uniform(20, 80),
                'mobile_usage_pct': random.uniform(10, 60),
                'cost_per_active_user': vendor['annual_spend'] / 12 / max(active_users, 1)
            })
    
    usage_df = pd.DataFrame(usage_data)
    
    # 2. EFFICIENCY IMPACT METRICS
    print("2. Creating Efficiency Impact Metrics...")
    
    efficiency_data = []
    efficiency_systems = [
        ('Office 365', 'Document collaboration time reduced by 35%', 2.5, 'High'),
        ('Canvas LMS', 'Grading time reduced by 40%', 3.2, 'High'),
        ('Banner ERP', 'Registration processing time reduced by 50%', 4.1, 'Critical'),
        ('Zoom', 'Meeting scheduling time reduced by 60%', 1.8, 'Medium'),
        ('ServiceNow', 'Ticket resolution time improved by 45%', 2.9, 'High'),
        ('Salesforce', 'Lead processing time reduced by 55%', 3.5, 'High'),
        ('Workday', 'HR processes accelerated by 40%', 3.8, 'Critical'),
        ('Tableau', 'Report generation time reduced by 70%', 2.2, 'Medium')
    ]
    
    for system_name, efficiency_gain, time_saved_hrs, impact_level in efficiency_systems:
        efficiency_data.append({
            'system_name': system_name,
            'process_improved': efficiency_gain,
            'hours_saved_per_user_monthly': time_saved_hrs,
            'impact_level': impact_level,
            'adoption_rate': random.uniform(60, 95),
            'user_satisfaction_score': random.uniform(3.5, 4.8),
            'training_completion_rate': random.uniform(70, 95),
            'support_tickets_per_user': random.uniform(0.1, 0.8),
            'process_error_reduction': random.uniform(20, 70)
        })
    
    efficiency_df = pd.DataFrame(efficiency_data)
    
    # 3. ROI CALCULATION DATA
    print("3. Creating ROI Calculation Data...")
    
    roi_data = []
    for _, vendor in vendors.iterrows():
        # Calculate various ROI components
        if vendor['vendor_name'] in [e[0] for e in efficiency_systems]:
            # Get efficiency data
            eff_data = efficiency_df[efficiency_df['system_name'] == vendor['vendor_name']].iloc[0]
            
            # Calculate monetary value
            hours_saved_annually = eff_data['hours_saved_per_user_monthly'] * 12 * vendor['users']
            labor_cost_saved = hours_saved_annually * 35  # $35/hour average
            
            # Additional benefits
            error_reduction_savings = vendor['annual_spend'] * 0.1  # 10% savings from fewer errors
            productivity_gains = labor_cost_saved * 0.5  # 50% of time saved translates to productivity
            
            total_benefits = labor_cost_saved + error_reduction_savings + productivity_gains
            roi_percentage = ((total_benefits - vendor['annual_spend']) / vendor['annual_spend']) * 100
            
            roi_data.append({
                'vendor_name': vendor['vendor_name'],
                'annual_cost': vendor['annual_spend'],
                'labor_hours_saved': hours_saved_annually,
                'labor_cost_savings': labor_cost_saved,
                'error_reduction_savings': error_reduction_savings,
                'productivity_gains': productivity_gains,
                'total_annual_benefits': total_benefits,
                'net_benefit': total_benefits - vendor['annual_spend'],
                'roi_percentage': roi_percentage,
                'payback_period_months': (vendor['annual_spend'] / total_benefits * 12) if total_benefits > 0 else 999
            })
    
    roi_df = pd.DataFrame(roi_data)
    
    # 4. USER SATISFACTION & ADOPTION
    print("4. Creating User Satisfaction & Adoption Metrics...")
    
    satisfaction_data = []
    departments = ['IT', 'Academic Affairs', 'Student Services', 'Finance', 'Administration']
    
    for dept in departments:
        for _, vendor in vendors.iterrows():
            satisfaction_data.append({
                'department': dept,
                'vendor_name': vendor['vendor_name'],
                'satisfaction_score': random.uniform(2.5, 5.0),
                'would_recommend': random.uniform(60, 95),
                'ease_of_use': random.uniform(2.5, 5.0),
                'meets_needs': random.uniform(70, 95),
                'training_satisfaction': random.uniform(3.0, 5.0),
                'support_quality': random.uniform(3.0, 5.0)
            })
    
    satisfaction_df = pd.DataFrame(satisfaction_data)
    
    # 5. COMPARATIVE ANALYSIS
    print("5. Creating Comparative Analysis...")
    
    comparison_data = []
    for _, vendor in vendors.head(10).iterrows():
        usage_stats = usage_df[usage_df['vendor_name'] == vendor['vendor_name']]
        if not usage_stats.empty:
            avg_utilization = usage_stats['utilization_rate'].mean()
            
            comparison_data.append({
                'vendor_name': vendor['vendor_name'],
                'category': vendor['category'],
                'annual_spend': vendor['annual_spend'],
                'licenses': vendor['users'],
                'avg_utilization': avg_utilization,
                'cost_per_license': vendor['annual_spend'] / vendor['users'],
                'actual_cost_per_active_user': vendor['annual_spend'] / (vendor['users'] * avg_utilization / 100),
                'utilization_category': 'High' if avg_utilization > 75 else 'Medium' if avg_utilization > 50 else 'Low',
                'optimization_opportunity': 'Yes' if avg_utilization < 60 else 'No'
            })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # 6. EXECUTIVE INSIGHTS
    print("\n📈 GENERATING EXECUTIVE INSIGHTS...")
    
    # Calculate key insights
    total_licenses = vendors['users'].sum()
    avg_utilization = usage_df['utilization_rate'].mean()
    wasted_licenses = int(total_licenses * (1 - avg_utilization/100))
    wasted_spend = vendors['annual_spend'].sum() * (1 - avg_utilization/100)
    
    high_roi_systems = roi_df[roi_df['roi_percentage'] > 100]
    low_usage_high_cost = comparison_df[
        (comparison_df['avg_utilization'] < 50) & 
        (comparison_df['annual_spend'] > 50000)
    ]
    
    # Save all enhanced data
    with pd.ExcelWriter('PQC_Usage_Efficiency_ROI_Data.xlsx', engine='xlsxwriter') as writer:
        usage_df.to_excel(writer, sheet_name='Software_Usage', index=False)
        efficiency_df.to_excel(writer, sheet_name='Efficiency_Gains', index=False)
        roi_df.to_excel(writer, sheet_name='ROI_Analysis', index=False)
        satisfaction_df.to_excel(writer, sheet_name='User_Satisfaction', index=False)
        comparison_df.to_excel(writer, sheet_name='Usage_Comparison', index=False)
        
        # Create executive summary sheet
        exec_summary = pd.DataFrame({
            'Key Metric': [
                'Total Software Licenses',
                'Average Utilization Rate',
                'Wasted Licenses',
                'Annual Spend on Unused Licenses',
                'Systems with >100% ROI',
                'Average User Satisfaction',
                'High Cost/Low Usage Systems',
                'Total Hours Saved Annually',
                'Total ROI from Efficiency Gains'
            ],
            'Value': [
                f'{total_licenses:,}',
                f'{avg_utilization:.1f}%',
                f'{wasted_licenses:,}',
                f'${wasted_spend:,.0f}',
                len(high_roi_systems),
                f'{satisfaction_df["satisfaction_score"].mean():.1f}/5.0',
                len(low_usage_high_cost),
                f'{roi_df["labor_hours_saved"].sum():,.0f}',
                f'${roi_df["net_benefit"].sum():,.0f}'
            ]
        })
        exec_summary.to_excel(writer, sheet_name='Executive_Summary', index=False)
    
    print("\n" + "="*60)
    print("💡 KEY INSIGHTS FOR EXECUTIVES:")
    print("="*60)
    
    print(f"\n📊 USAGE INSIGHTS:")
    print(f"- Only {avg_utilization:.0f}% of licenses are actively used")
    print(f"- {wasted_licenses:,} licenses are unused (${wasted_spend:,.0f} wasted)")
    print(f"- Top underutilized: {low_usage_high_cost['vendor_name'].iloc[0] if not low_usage_high_cost.empty else 'None'}")
    
    print(f"\n💰 ROI INSIGHTS:")
    print(f"- {len(high_roi_systems)} systems delivering >100% ROI")
    print(f"- Total efficiency gains: ${roi_df['total_annual_benefits'].sum():,.0f}")
    print(f"- Best ROI: {roi_df.loc[roi_df['roi_percentage'].idxmax(), 'vendor_name']} ({roi_df['roi_percentage'].max():.0f}%)")
    
    print(f"\n⏱️ EFFICIENCY INSIGHTS:")
    print(f"- {roi_df['labor_hours_saved'].sum():,.0f} hours saved annually")
    print(f"- Average process improvement: 48%")
    print(f"- Fastest payback: {roi_df['payback_period_months'].min():.0f} months")
    
    print(f"\n😊 SATISFACTION INSIGHTS:")
    print(f"- Average user satisfaction: {satisfaction_df['satisfaction_score'].mean():.1f}/5.0")
    print(f"- Would recommend: {satisfaction_df['would_recommend'].mean():.0f}%")
    print(f"- Training satisfaction: {satisfaction_df['training_satisfaction'].mean():.1f}/5.0")
    
    print("\n✅ Created: PQC_Usage_Efficiency_ROI_Data.xlsx")
    print("This file contains 6 sheets with comprehensive usage and ROI analytics!")

# Generate the enhanced data
generate_usage_and_impact_data()

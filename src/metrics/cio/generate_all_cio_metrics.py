#!/usr/bin/env python3
"""
Complete CIO Metrics Data Generator
Generates all proper time-series data files for the CIO dashboard
Based on your existing metric definitions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Generating comprehensive CIO metrics data in: {current_dir}")
print("=" * 70)

# Generate date range for the last 90 days
end_date = datetime.now()
start_date = end_date - timedelta(days=90)
dates = pd.date_range(start=start_date, end=end_date, freq='D')

# Also create weekly and monthly date ranges for different metrics
weekly_dates = pd.date_range(start=start_date, end=end_date, freq='W')
monthly_dates = pd.date_range(start=start_date, end=end_date, freq='M')

print("\nGenerating CIO Metric Data Files:")
print("-" * 40)

# ============================================
# 1. APP COST ANALYSIS METRICS
# ============================================
print("\n1. app_cost_analysis_metrics.csv")

applications = ['Office 365', 'Canvas LMS', 'Zoom', 'Blackboard', 
                'Cisco WebEx', 'Google Workspace', 'Slack', 'Adobe Creative Cloud',
                'ServiceNow', 'Tableau', 'Oracle Database', 'VMware vSphere']

app_cost_data = []
for date in dates:
    for app in applications:
        # Base costs for each application
        base_costs = {
            'Office 365': 285000/365, 'Canvas LMS': 220000/365, 'Zoom': 75000/365,
            'Blackboard': 180000/365, 'Cisco WebEx': 45000/365, 'Google Workspace': 90000/365,
            'Slack': 60000/365, 'Adobe Creative Cloud': 120000/365, 'ServiceNow': 110000/365,
            'Tableau': 90000/365, 'Oracle Database': 150000/365, 'VMware vSphere': 95000/365
        }
        
        daily_cost = base_costs.get(app, 100000/365)
        users = np.random.randint(50, 500)
        licenses = users + np.random.randint(10, 100)
        
        app_cost_data.append({
            'date': date,
            'application': app,
            'daily_cost': daily_cost * np.random.uniform(0.95, 1.05),
            'monthly_cost': daily_cost * 30 * np.random.uniform(0.95, 1.05),
            'annual_cost': daily_cost * 365,
            'licenses_total': licenses,
            'licenses_used': users,
            'utilization_rate': (users/licenses) * 100,
            'cost_per_user': (daily_cost * 30) / users if users > 0 else 0,
            'redundancy_index': np.random.uniform(0.1, 0.8),
            'consolidation_potential': np.random.choice(['Yes', 'No']),
            'support_cost': daily_cost * 0.15,
            'compliance_cost': daily_cost * 0.05
        })

df_app_cost = pd.DataFrame(app_cost_data)
df_app_cost.to_csv(os.path.join(current_dir, 'app_cost_analysis_metrics.csv'), index=False)
print(f"  ✓ Created ({len(df_app_cost)} rows)")

# ============================================
# 2. BUSINESS UNIT IT SPEND
# ============================================
print("\n2. business_unit_it_spend.csv")

business_units = ['Academic Affairs', 'Student Affairs', 'IT Operations', 
                  'Finance & Admin', 'Registrar', 'Institutional Research', 
                  'Library', 'Athletics']

bu_spend_data = []
for date in dates:
    for unit in business_units:
        base_budgets = {
            'Academic Affairs': 150000/365, 'Student Affairs': 80000/365,
            'IT Operations': 200000/365, 'Finance & Admin': 100000/365,
            'Registrar': 60000/365, 'Institutional Research': 70000/365,
            'Library': 90000/365, 'Athletics': 70000/365
        }
        
        daily_budget = base_budgets.get(unit, 75000/365)
        daily_spend = daily_budget * np.random.uniform(0.85, 1.15)
        fte_count = np.random.randint(10, 100)
        
        bu_spend_data.append({
            'date': date,
            'business_unit': unit,
            'daily_budget': daily_budget,
            'daily_spend': daily_spend,
            'monthly_budget': daily_budget * 30,
            'monthly_spend': daily_spend * 30,
            'operational_spend': daily_spend * 0.7,
            'project_spend': daily_spend * 0.3,
            'budget_variance_pct': ((daily_spend - daily_budget) / daily_budget) * 100,
            'fte_count': fte_count,
            'spend_per_fte': (daily_spend * 30) / fte_count,
            'growth_rate': np.random.uniform(-5, 15),
            'innovation_allocation_pct': np.random.uniform(5, 25),
            'cost_efficiency_index': np.random.uniform(0.6, 1.0)
        })

df_bu_spend = pd.DataFrame(bu_spend_data)
df_bu_spend.to_csv(os.path.join(current_dir, 'business_unit_it_spend.csv'), index=False)
print(f"  ✓ Created ({len(df_bu_spend)} rows)")

# ============================================
# 3. DIGITAL TRANSFORMATION METRICS
# ============================================
print("\n3. digital_transformation_metrics.csv")

dt_metrics_data = []
initiatives = ['Online BA in Psychology', 'Hybrid MBA', 'Virtual STEM Labs', 
               'AI Tutoring Platform', 'Learning Analytics Implementation']

for i, date in enumerate(dates):
    progress = i / len(dates)
    
    # Overall metrics
    dt_metrics_data.append({
        'date': date,
        'metric_type': 'overall',
        'initiative': 'All',
        'digital_maturity': np.random.choice(['Ad hoc', 'Basic', 'Established', 'Leading']),
        'transformation_score': min(85, 65 + progress * 15 + np.random.normal(0, 2)),
        'online_adoption_rate': min(90, 40 + progress * 35 + np.random.normal(0, 3)),
        'student_participation_pct': min(95, 60 + progress * 25 + np.random.normal(0, 2)),
        'faculty_participation_pct': min(85, 55 + progress * 20 + np.random.normal(0, 2)),
        'platform_utilization_pct': min(90, 50 + progress * 30 + np.random.normal(0, 3)),
        'digital_literacy_students': min(4.8, 3.0 + progress * 1.2 + np.random.normal(0, 0.1)),
        'digital_literacy_faculty': min(4.5, 2.8 + progress * 1.2 + np.random.normal(0, 0.1)),
        'accessibility_compliance_pct': min(98, 85 + progress * 10 + np.random.normal(0, 1)),
        'online_completion_rate': min(92, 75 + progress * 12 + np.random.normal(0, 2)),
        'satisfaction_score': min(4.8, 3.5 + progress * 1.0 + np.random.normal(0, 0.1)),
        'support_ticket_resolution_hrs': max(2, 24 - progress * 15 + np.random.normal(0, 2)),
        'virtual_engagement_rate': min(85, 45 + progress * 30 + np.random.normal(0, 3)),
        'remote_enablement_pct': min(95, 70 + progress * 20 + np.random.normal(0, 2)),
        'innovation_milestones': np.random.randint(1 + int(progress * 3), 6 + int(progress * 3)),
        'digital_budget_allocation_pct': min(30, 15 + progress * 10 + np.random.normal(0, 1)),
        'digital_credentials_volume': np.random.randint(100 + int(progress * 200), 500 + int(progress * 400))
    })

df_dt_metrics = pd.DataFrame(dt_metrics_data)
df_dt_metrics.to_csv(os.path.join(current_dir, 'digital_transformation_metrics.csv'), index=False)
print(f"  ✓ Created ({len(df_dt_metrics)} rows)")

# ============================================
# 4. RISK METRICS
# ============================================
print("\n4. risk_metrics.csv")

risk_categories = ['Security', 'Compliance', 'Operational', 'Financial', 'Strategic']
projects_for_risk = ['Student Portal Upgrade', 'Cybersecurity Enhancement', 
                      'Cloud Migration', 'Network Infrastructure', 'LMS Modernization']

risk_data = []
for date in dates:
    for category in risk_categories:
        for project in projects_for_risk:
            severity = np.random.randint(1, 10)
            probability = np.random.uniform(0.1, 0.9)
            
            risk_data.append({
                'date': date,
                'project': project,
                'risk_category': category,
                'risk_exposure_level': severity * probability,
                'risk_heat_map': np.random.choice(['Low', 'Medium', 'High', 'Critical']),
                'active_risks_count': np.random.randint(0, 8),
                'severity_score': severity,
                'probability_score': probability,
                'mitigation_status': np.random.choice(['Open', 'In Progress', 'Resolved']),
                'time_to_closure_days': np.random.randint(1, 50),
                'mitigation_progress_pct': np.random.uniform(0, 100),
                'control_effectiveness_pct': np.random.uniform(60, 95),
                'residual_risk_level': severity * probability * 0.3,
                'incident_response_hrs': np.random.randint(1, 24),
                'escalated_count': np.random.randint(0, 3),
                'compliance_adherence_pct': np.random.uniform(85, 100),
                'financial_impact_estimate': np.random.randint(5000, 150000),
                'kri_indicator': np.random.choice(['Cost Overrun', 'Schedule Delay', 'Quality Issue', 'Resource Gap'])
            })

df_risk = pd.DataFrame(risk_data)
df_risk.to_csv(os.path.join(current_dir, 'risk_metrics.csv'), index=False)
print(f"  ✓ Created ({len(df_risk)} rows)")

# ============================================
# 5. VENDOR METRICS
# ============================================
print("\n5. vendor_metrics.csv")

vendors = ['Microsoft', 'AWS', 'Adobe', 'Blackboard', 'Cisco', 
           'Zoom', 'Oracle', 'Salesforce', 'VMware', 'ServiceNow']

vendor_data = []
for date in dates:
    for vendor in vendors:
        base_annual_spend = {
            'Microsoft': 450000, 'AWS': 320000, 'Adobe': 180000,
            'Blackboard': 220000, 'Cisco': 200000, 'Zoom': 85000,
            'Oracle': 150000, 'Salesforce': 120000, 'VMware': 95000,
            'ServiceNow': 110000
        }.get(vendor, 100000)
        
        vendor_data.append({
            'date': date,
            'vendor': vendor,
            'daily_spend': base_annual_spend / 365 * np.random.uniform(0.95, 1.05),
            'annual_spend': base_annual_spend,
            'satisfaction_score': np.random.uniform(3.2, 4.9),
            'sla_compliance_pct': np.random.uniform(85, 99.9),
            'contract_renewal_rate': np.random.uniform(75, 100),
            'delivered_value_ratio': np.random.uniform(0.8, 1.3),
            'incident_response_hrs': np.random.uniform(0.5, 8),
            'issue_resolution_days': np.random.uniform(0.5, 5),
            'penalty_occurrences': np.random.randint(0, 3),
            'dispute_count': np.random.randint(0, 2),
            'innovation_rating': np.random.uniform(3.0, 5.0),
            'cost_variance_pct': np.random.uniform(-10, 10),
            'uptime_pct': np.random.uniform(97.0, 99.99),
            'contract_breach_count': np.random.randint(0, 2),
            'vendor_longevity_years': np.random.randint(1, 10),
            'savings_realized': np.random.uniform(5000, 50000),
            'spend_growth_rate': np.random.uniform(-5, 15),
            'compliance_score': np.random.uniform(85, 100)
        })

df_vendor = pd.DataFrame(vendor_data)
df_vendor.to_csv(os.path.join(current_dir, 'vendor_metrics.csv'), index=False)
print(f"  ✓ Created ({len(df_vendor)} rows)")

# ============================================
# 6. STRATEGIC ALIGNMENT METRICS
# ============================================
print("\n6. strategic_alignment_metrics.csv")

initiatives = ['Student Portal Upgrade', 'AI Tutoring', 'LMS Modernization', 
               'Mobile App Development', 'Library Digital Access', 'Cloud Migration',
               'Data Analytics Platform', 'Virtual Reality Lab']

strategic_data = []
for i, date in enumerate(dates):
    progress = i / len(dates)
    
    for initiative in initiatives:
        strategic_data.append({
            'date': date,
            'initiative': initiative,
            'alignment_score': min(10, 7.5 + progress * 1.5 + np.random.normal(0, 0.5)),
            'mission_relevance_rating': min(5, 3.5 + progress * 1.0 + np.random.normal(0, 0.2)),
            'student_experience_impact': min(10, 6.5 + progress * 2.5 + np.random.normal(0, 0.5)),
            'underserved_benefit_index': min(1.0, 0.5 + progress * 0.3 + np.random.normal(0, 0.1)),
            'equity_advancement_score': min(10, 6.0 + progress * 3.0 + np.random.normal(0, 0.5)),
            'learning_outcomes_improvement_pct': min(15, 5 + progress * 8 + np.random.normal(0, 1)),
            'digital_inclusion_rating': min(5, 3.0 + progress * 1.5 + np.random.normal(0, 0.2)),
            'retention_projection_pct': min(10, 2 + progress * 6 + np.random.normal(0, 0.5)),
            'community_engagement_level': min(10, 5.5 + progress * 3.0 + np.random.normal(0, 0.5)),
            'grant_funder_fit': min(5, 3.2 + progress * 1.5 + np.random.normal(0, 0.2)),
            'stakeholder_support_level': min(5, 3.5 + progress * 1.2 + np.random.normal(0, 0.2)),
            'sustainability_factor': min(10, 6.5 + progress * 2.5 + np.random.normal(0, 0.5)),
            'accessibility_rating': min(5, 3.8 + progress * 1.0 + np.random.normal(0, 0.1)),
            'holistic_support_integration': min(10, 6.0 + progress * 3.0 + np.random.normal(0, 0.5)),
            'cost_per_student_benefited': max(30, 150 - progress * 80 + np.random.normal(0, 10))
        })

df_strategic = pd.DataFrame(strategic_data)
df_strategic.to_csv(os.path.join(current_dir, 'strategic_alignment_metrics.csv'), index=False)
print(f"  ✓ Created ({len(df_strategic)} rows)")

# ============================================
# 7. RUN/GROW/TRANSFORM (RGT) METRICS
# ============================================
print("\n7. rgt_portfolio_metrics.csv")

rgt_data = []
rgt_categories = ['RUN', 'GROW', 'TRANSFORM']

for date in monthly_dates:
    total_budget = 3000000  # Annual IT budget
    
    # Generate realistic RGT distribution that trends toward optimal
    month_progress = (date - monthly_dates[0]).days / (monthly_dates[-1] - monthly_dates[0]).days
    
    # Starting distribution (suboptimal)
    run_start, grow_start, transform_start = 75, 20, 5
    # Target distribution (optimal)
    run_target, grow_target, transform_target = 65, 25, 15
    
    # Calculate current distribution
    run_pct = run_start + (run_target - run_start) * month_progress + np.random.normal(0, 2)
    grow_pct = grow_start + (grow_target - grow_start) * month_progress + np.random.normal(0, 2)
    transform_pct = transform_start + (transform_target - transform_start) * month_progress + np.random.normal(0, 1)
    
    # Normalize to 100%
    total = run_pct + grow_pct + transform_pct
    run_pct, grow_pct, transform_pct = run_pct/total*100, grow_pct/total*100, transform_pct/total*100
    
    for category in rgt_categories:
        if category == 'RUN':
            pct, budget = run_pct, total_budget * run_pct / 100
            project_count = np.random.randint(8, 15)
            avg_roi = np.random.uniform(5, 15)
        elif category == 'GROW':
            pct, budget = grow_pct, total_budget * grow_pct / 100
            project_count = np.random.randint(5, 10)
            avg_roi = np.random.uniform(15, 25)
        else:  # TRANSFORM
            pct, budget = transform_pct, total_budget * transform_pct / 100
            project_count = np.random.randint(2, 6)
            avg_roi = np.random.uniform(20, 35)
        
        rgt_data.append({
            'date': date,
            'category': category,
            'spend_percentage': pct,
            'budget_allocated': budget,
            'project_count': project_count,
            'average_roi': avg_roi,
            'risk_score': np.random.uniform(2, 8),
            'strategic_alignment': np.random.uniform(6, 10),
            'success_rate': np.random.uniform(60, 95),
            'time_to_value_months': np.random.randint(3, 24),
            'benefits_realized': budget * (avg_roi / 100),
            'portfolio_balance_score': 10 - abs(pct - {'RUN': 65, 'GROW': 25, 'TRANSFORM': 15}[category]) / 5
        })

df_rgt = pd.DataFrame(rgt_data)
df_rgt.to_csv(os.path.join(current_dir, 'rgt_portfolio_metrics.csv'), index=False)
print(f"  ✓ Created ({len(df_rgt)} rows)")

# ============================================
# 8. PROJECT TIMELINE & BUDGET PERFORMANCE
# ============================================
print("\n8. project_timeline_budget_performance.csv")

# This one already exists in your files, but let's ensure it has the right format
projects_data = {
    'Project_ID': ['PQC-001', 'PQC-002', 'PQC-003', 'PQC-004', 'PQC-005',
                   'PQC-006', 'PQC-007', 'PQC-008', 'PQC-009', 'PQC-010'],
    'Project_Name': [
        'Student Portal Upgrade', 'Cloud Migration Phase 1', 'Cybersecurity Enhancement',
        'LMS Modernization', 'Network Infrastructure', 'AI Tutoring System',
        'Campus WiFi Expansion', 'Data Analytics Platform', 'Mobile App Development',
        'ERP System Integration'
    ],
    'Status': ['In Progress', 'Completed', 'In Progress', 'Planning', 'In Progress',
               'Planning', 'Completed', 'In Progress', 'Planning', 'In Progress'],
    'Total_Budget': [250000, 450000, 300000, 180000, 220000,
                     400000, 150000, 350000, 120000, 280000],
    'Spent_to_Date': [175000, 445000, 125000, 25000, 165000,
                      50000, 148000, 210000, 15000, 200000],
    'Start_Date': pd.to_datetime(['2024-01-15', '2023-09-01', '2024-02-01', '2024-06-01', '2023-12-01',
                                  '2024-07-01', '2023-08-15', '2024-03-01', '2024-08-01', '2024-01-01']),
    'End_Date': pd.to_datetime(['2024-08-30', '2024-03-15', '2024-12-31', '2025-01-31', '2024-09-30',
                                '2025-03-31', '2023-12-31', '2024-11-30', '2025-02-28', '2024-10-31'])
}

projects_df = pd.DataFrame(projects_data)
today = datetime.now()
projects_df['Duration_days'] = (projects_df['End_Date'] - projects_df['Start_Date']).dt.days
projects_df['Elapsed_days'] = (today - projects_df['Start_Date']).dt.days.clip(lower=0)
projects_df['Timeline_Completion_%'] = (projects_df['Elapsed_days'] / projects_df['Duration_days'] * 100).clip(upper=100).round(1)
projects_df['Budget_Variance_%'] = ((projects_df['Spent_to_Date'] - projects_df['Total_Budget']) / projects_df['Total_Budget'] * 100).round(1)
projects_df['Budget_Status'] = projects_df['Budget_Variance_%'].apply(
    lambda x: 'Over Budget' if x > 5 else ('Under Budget' if x < -5 else 'On Track')
)
projects_df['Time_Status'] = projects_df.apply(
    lambda row: 'Delayed' if row['Timeline_Completion_%'] > 100 and row['Status'] != 'Completed' else 
                'On Track' if row['Timeline_Completion_%'] < 100 or row['Status'] == 'Completed' else 
                'Unknown', axis=1
)

projects_df.to_csv(os.path.join(current_dir, 'project_timeline_budget_performance.csv'), index=False)
print(f"  ✓ Created ({len(projects_df)} rows)")

# ============================================
# 9. COMPREHENSIVE CIO METRICS (All Strategic Partner Metrics)
# ============================================
print("\n9. cio_comprehensive_metrics.csv")

comprehensive_data = []
for date in dates:
    i = (date - dates[0]).days / (dates[-1] - dates[0]).days
    
    # Calculate portfolio drift
    current_run = 65 + np.random.normal(0, 3)
    current_grow = 25 + np.random.normal(0, 2)
    current_transform = 10 + np.random.normal(0, 2)
    
    portfolio_drift = abs(current_run - 65) + abs(current_grow - 25) + abs(current_transform - 15)
    
    comprehensive_data.append({
        'date': date,
        # Portfolio Balance Metrics
        'rgt_run_pct': current_run,
        'rgt_grow_pct': current_grow,
        'rgt_transform_pct': current_transform,
        'portfolio_drift': portfolio_drift,
        'portfolio_balance_score': max(0, 10 - portfolio_drift/10),
        
        # Financial Analysis
        'cost_per_fte_run': np.random.uniform(800, 1200),
        'cost_per_fte_grow': np.random.uniform(1000, 1500),
        'cost_per_fte_transform': np.random.uniform(1200, 2000),
        'roi_run': np.random.uniform(5, 15),
        'roi_grow': np.random.uniform(15, 25),
        'roi_transform': np.random.uniform(20, 35),
        'budget_variance_run': np.random.uniform(-10, 10),
        'budget_variance_grow': np.random.uniform(-15, 15),
        'budget_variance_transform': np.random.uniform(-20, 20),
        'total_tco': np.random.uniform(2500000, 3500000),
        
        # Strategic Metrics
        'strategic_alignment_pct': min(95, 70 + i * 20 + np.random.normal(0, 2)),
        'business_capability_coverage': min(95, 75 + i * 15 + np.random.normal(0, 2)),
        'innovation_index': min(8.5, 7.0 + i * 1.0 + np.random.normal(0, 0.2)),
        
        # Risk Management
        'portfolio_risk_score': max(3, 7 - i * 3 + np.random.normal(0, 0.5)),
        'technical_debt_run': np.random.uniform(10, 25),
        'technical_debt_grow': np.random.uniform(5, 15),
        'technical_debt_transform': np.random.uniform(2, 8),
        'compliance_gap_pct': max(0, 15 - i * 10 + np.random.normal(0, 1)),
        
        # Project Performance
        'time_to_value_run_months': np.random.uniform(3, 6),
        'time_to_value_grow_months': np.random.uniform(6, 12),
        'time_to_value_transform_months': np.random.uniform(12, 24),
        'success_rate_run': min(98, 90 + i * 5 + np.random.normal(0, 1)),
        'success_rate_grow': min(92, 80 + i * 8 + np.random.normal(0, 2)),
        'success_rate_transform': min(85, 65 + i * 15 + np.random.normal(0, 3)),
        
        # Value Realization
        'benefits_realization_pct': min(95, 70 + i * 20 + np.random.normal(0, 2)),
        'business_impact_score': min(9.5, 7.0 + i * 2.0 + np.random.normal(0, 0.3)),
        'stakeholder_satisfaction': min(4.8, 3.5 + i * 1.0 + np.random.normal(0, 0.1)),
        
        # Digital Transformation (Summary)
        'digital_transformation_score': min(85, 65 + i * 15 + np.random.normal(0, 2)),
        'digital_maturity_level': np.random.choice(['Basic', 'Established', 'Leading'], p=[0.3-i*0.2, 0.5, 0.2+i*0.2]),
        'online_learning_adoption_pct': min(90, 40 + i * 40 + np.random.normal(0, 3)),
        'digital_engagement_score': min(95, 70 + i * 20 + np.random.normal(0, 2)),
        
        # Additional Executive Metrics
        'vendor_satisfaction_avg': min(4.8, 3.8 + i * 0.8 + np.random.normal(0, 0.1)),
        'cost_optimization_savings': np.random.uniform(50000, 200000),
        'compliance_score': min(98, 85 + i * 10 + np.random.normal(0, 1))
    })

df_comprehensive = pd.DataFrame(comprehensive_data)
df_comprehensive.to_csv(os.path.join(current_dir, 'cio_comprehensive_metrics.csv'), index=False)
print(f"  ✓ Created ({len(df_comprehensive)} rows)")

# ============================================
# CLEANUP: Rename old example files
# ============================================
print("\n10. Cleaning up old example files...")
example_files = [
    'app_cost_analysis_dashboard_examples.csv',
    'business_unit_it_spend_examples.csv',
    'digital_transformation_dashboard_examples.csv',
    'risk_dashboard_metrics_examples.csv',
    'strategic_alignment_dashboard_examples.csv',
    'vendor_dashboard_metrics_examples.csv'
]

for file in example_files:
    file_path = os.path.join(current_dir, file)
    if os.path.exists(file_path):
        backup_path = file_path.replace('.csv', '_backup.csv')
        try:
            os.rename(file_path, backup_path)
            print(f"  ✓ Renamed {file} to backup")
        except:
            print(f"  ⚠ Could not rename {file}")

print("\n" + "=" * 70)
print("✅ SUCCESS! All CIO metric data files generated")
print("=" * 70)

# List all created files
print("\nCreated data files:")
created_files = [
    'app_cost_analysis_metrics.csv',
    'business_unit_it_spend.csv',
    'digital_transformation_metrics.csv',
    'risk_metrics.csv',
    'vendor_metrics.csv',
    'strategic_alignment_metrics.csv',
    'rgt_portfolio_metrics.csv',
    'project_timeline_budget_performance.csv',
    'cio_summary_metrics.csv'
]

total_size = 0
for file in created_files:
    file_path = os.path.join(current_dir, file)
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        total_size += size
        df_temp = pd.read_csv(file_path)
        print(f"  ✓ {file}: {len(df_temp)} rows, {len(df_temp.columns)} columns ({size:,} bytes)")

print(f"\nTotal: {len(created_files)} files, {total_size:,} bytes")
print("\n🚀 Next steps:")
print("1. Go back to project root: cd ../../..")  
print("2. Delete config.toml: rm .streamlit/config.toml")
print("3. Restart dashboard: streamlit run src/dashboard/fully_integrated_dashboard.py")
print("\nYour CIO dashboard should now display all metrics properly!")
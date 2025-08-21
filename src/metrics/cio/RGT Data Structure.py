# Creating comprehensive sample data structure to support RGT analysis
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

print("COMPREHENSIVE RGT SAMPLE DATA STRUCTURE FOR PAUL QUINN COLLEGE")
print("=" * 70)
print()

# Set random seed for reproducible results
np.random.seed(42)
random.seed(42)

# 1. Enhanced Projects Data with RGT Classification
projects_data = {
    'Project_ID': ['PQC-001', 'PQC-002', 'PQC-003', 'PQC-004', 'PQC-005', 
                   'PQC-006', 'PQC-007', 'PQC-008', 'PQC-009', 'PQC-010',
                   'PQC-011', 'PQC-012', 'PQC-013', 'PQC-014', 'PQC-015'],
    
    'Project_Name': [
        'Student Portal Upgrade', 'Cloud Migration Phase 1', 'Cybersecurity Enhancement',
        'LMS Modernization', 'Network Infrastructure', 'AI Tutoring System',
        'Campus WiFi Expansion', 'Data Analytics Platform', 'Mobile App Development',
        'ERP System Integration', 'Virtual Reality Lab', 'Blockchain Certificates',
        'Server Maintenance', 'Backup System Upgrade', 'Help Desk Modernization'
    ],
    
    'RGT_Category': [
        'GROW', 'TRANSFORM', 'RUN', 'GROW', 'RUN',
        'TRANSFORM', 'GROW', 'TRANSFORM', 'GROW', 'GROW',
        'TRANSFORM', 'TRANSFORM', 'RUN', 'RUN', 'RUN'
    ],
    
    'RGT_Category_Confidence': [0.95, 0.90, 0.98, 0.85, 0.95,
                                0.80, 0.90, 0.85, 0.88, 0.92,
                                0.75, 0.82, 0.98, 0.95, 0.93],
    
    'Business_Capability': [
        'Student Services', 'Infrastructure', 'Security', 'Academic Delivery', 'Infrastructure',
        'Academic Delivery', 'Infrastructure', 'Data & Analytics', 'Student Services', 'Finance & Admin',
        'Academic Delivery', 'Academic Delivery', 'Infrastructure', 'Infrastructure', 'Student Services'
    ],
    
    'Department': [
        'Student Affairs', 'IT Operations', 'IT Security', 'Academic Affairs', 'IT Operations',
        'Academic Affairs', 'IT Operations', 'Institutional Research', 'Student Affairs', 'Finance',
        'Academic Affairs', 'Registrar', 'IT Operations', 'IT Operations', 'IT Operations'
    ],
    
    'Status': ['In Progress', 'Completed', 'In Progress', 'Planning', 'In Progress',
               'Planning', 'Completed', 'In Progress', 'Planning', 'In Progress',
               'Planning', 'Planning', 'Completed', 'In Progress', 'In Progress'],
    
    'Total_Budget': [250000, 450000, 300000, 180000, 220000,
                     400000, 150000, 350000, 120000, 280000,
                     500000, 300000, 80000, 100000, 90000],
    
    'Spent_to_Date': [175000, 445000, 125000, 25000, 165000,
                      50000, 148000, 210000, 15000, 200000,
                      75000, 45000, 78000, 70000, 60000],
    
    'Planned_Benefits_Annual': [150000, 200000, 180000, 120000, 100000,
                                300000, 80000, 250000, 90000, 160000,
                                200000, 150000, 50000, 60000, 40000],
    
    'Risk_Score': [3.2, 6.8, 4.5, 2.1, 3.8,
                   7.5, 2.8, 5.9, 4.2, 3.9,
                   8.2, 7.1, 1.5, 2.3, 2.0],
    
    'Strategic_Alignment_Score': [8.5, 9.2, 7.8, 8.9, 6.5,
                                  9.5, 7.2, 9.1, 8.7, 7.9,
                                  9.3, 8.8, 6.8, 6.2, 7.1],
    
    'Start_Date': pd.to_datetime(['2024-01-15', '2023-09-01', '2024-02-01', '2024-06-01', '2023-12-01',
                                  '2024-07-01', '2023-08-15', '2024-03-01', '2024-08-01', '2024-01-01',
                                  '2024-09-01', '2024-10-01', '2023-06-01', '2024-04-01', '2024-05-01']),
    
    'End_Date': pd.to_datetime(['2024-08-30', '2024-03-15', '2024-12-31', '2025-01-31', '2024-09-30',
                                '2025-03-31', '2023-12-31', '2024-11-30', '2025-02-28', '2024-10-31',
                                '2025-06-30', '2025-04-30', '2023-12-31', '2024-12-31', '2024-12-31'])
}

df_projects = pd.DataFrame(projects_data)

# 2. Enhanced Vendors Data with RGT Categorization
vendors_data = {
    'Vendor_Name': ['Microsoft', 'AWS', 'Adobe', 'Blackboard', 'Cisco', 'Zoom',
                    'Oracle', 'Salesforce', 'VMware', 'Palo Alto Networks',
                    'ServiceNow', 'Tableau', 'Others'],
    
    'Primary_RGT_Category': ['RUN', 'TRANSFORM', 'GROW', 'RUN', 'RUN', 'GROW',
                             'RUN', 'GROW', 'RUN', 'RUN',
                             'GROW', 'TRANSFORM', 'RUN'],
    
    'Annual_Spend_2024': [450000, 320000, 180000, 220000, 200000, 85000,
                          150000, 120000, 95000, 80000,
                          110000, 90000, 265000],
    
    'Annual_Spend_2023': [420000, 280000, 170000, 210000, 190000, 75000,
                          140000, 100000, 90000, 70000,
                          95000, 75000, 245000],
    
    'Annual_Spend_2022': [400000, 220000, 160000, 200000, 180000, 65000,
                          130000, 80000, 85000, 60000,
                          80000, 60000, 225000],
    
    'Contract_End': pd.to_datetime(['2025-06-30', '2025-12-31', '2024-12-31', '2025-03-31', '2025-09-30',
                                    '2024-11-30', '2025-08-31', '2025-05-31', '2025-01-31', '2025-07-31',
                                    '2025-10-31', '2025-04-30', '2025-02-28']),
    
    'Contract_Value': [1350000, 960000, 540000, 660000, 600000, 255000,
                       450000, 360000, 285000, 240000,
                       330000, 270000, 795000],
    
    'Satisfaction_Score': [4.2, 4.7, 3.8, 3.4, 4.1, 4.8,
                           3.9, 4.3, 3.7, 4.0,
                           4.2, 4.5, 3.6],
    
    'Business_Capability_Support': [
        'Productivity, Collaboration', 'Infrastructure, Analytics', 'Creative, Marketing',
        'Academic Delivery', 'Infrastructure, Security', 'Communication, Collaboration',
        'Database, ERP', 'CRM, Student Services', 'Infrastructure, Virtualization',
        'Security, Network Protection', 'IT Service Management', 'Analytics, Reporting',
        'Various Support Services'
    ]
}

df_vendors = pd.DataFrame(vendors_data)

# 3. Enhanced Usage Data with License Optimization
usage_data = {
    'System_Name': ['Office 365', 'Canvas LMS', 'Zoom Pro', 'Adobe Creative Cloud',
                    'AWS Services', 'Cisco WebEx', 'Salesforce', 'Oracle Database',
                    'VMware vSphere', 'ServiceNow', 'Tableau Desktop', 'Student Portal'],
    
    'RGT_Category': ['RUN', 'RUN', 'GROW', 'GROW',
                     'TRANSFORM', 'GROW', 'GROW', 'RUN',
                     'RUN', 'GROW', 'TRANSFORM', 'GROW'],
    
    'Total_Licenses': [950, 900, 750, 200, 500, 300, 150, 50, 100, 75, 125, 1000],
    
    'Active_Users_Current': [880, 820, 680, 145, 350, 210, 120, 45, 85, 65, 95, 850],
    
    'Active_Users_Peak': [920, 850, 720, 165, 420, 250, 135, 48, 90, 70, 110, 920],
    
    'License_Cost_Annual': [285000, 220000, 75000, 120000, 0, 45000, 180000, 150000, 95000, 110000, 90000, 0],
    
    'Usage_Trend_3M': ['Stable', 'Growing', 'Growing', 'Declining', 'Growing', 'Stable', 
                       'Growing', 'Stable', 'Stable', 'Growing', 'Growing', 'Growing'],
    
    'Business_Critical_Score': [9.5, 9.8, 8.2, 6.5, 8.9, 7.1, 7.8, 8.7, 8.4, 7.9, 6.8, 9.2],
    
    'Renewal_Date': pd.to_datetime(['2025-03-31', '2025-07-31', '2024-12-31', '2025-01-31',
                                    '2025-06-30', '2025-04-30', '2025-05-31', '2025-08-31',
                                    '2025-02-28', '2025-09-30', '2025-04-30', 'N/A'])
}

df_usage = pd.DataFrame(usage_data)

# 4. Calculate comprehensive RGT metrics
print("1. PROJECT PORTFOLIO RGT DISTRIBUTION")
print("-" * 40)

rgt_summary = df_projects.groupby('RGT_Category').agg({
    'Total_Budget': ['count', 'sum'],
    'Spent_to_Date': 'sum',
    'Risk_Score': 'mean',
    'Strategic_Alignment_Score': 'mean'
}).round(2)

rgt_summary.columns = ['Project_Count', 'Total_Budget', 'Total_Spent', 'Avg_Risk', 'Avg_Alignment']
print(rgt_summary)

# Calculate percentages
total_budget = df_projects['Total_Budget'].sum()
rgt_percentages = df_projects.groupby('RGT_Category')['Total_Budget'].sum() / total_budget * 100

print(f"\n2. RGT SPEND DISTRIBUTION (% of Total Budget)")
print("-" * 50)
for category, percentage in rgt_percentages.items():
    print(f"{category}: {percentage:.1f}%")

# Calculate deviations from optimal
optimal_targets = {'RUN': 65, 'GROW': 25, 'TRANSFORM': 15}
print(f"\n3. DEVIATION FROM OPTIMAL TARGETS")
print("-" * 40)

for category in optimal_targets:
    current = rgt_percentages.get(category, 0)
    target = optimal_targets[category]
    deviation = abs(current - target)
    status = "✅ Within Range" if deviation <= 5 else "⚠️ Needs Attention" if deviation <= 10 else "🚨 Critical"
    print(f"{category}: Current {current:.1f}% vs Target {target}% | Deviation: {deviation:.1f}% | {status}")

# Save all enhanced datasets
df_projects.to_csv('enhanced_projects_rgt.csv', index=False)
df_vendors.to_csv('enhanced_vendors_rgt.csv', index=False)  
df_usage.to_csv('enhanced_usage_rgt.csv', index=False)

print(f"\n✅ Enhanced RGT datasets saved:")
print("   • enhanced_projects_rgt.csv")
print("   • enhanced_vendors_rgt.csv") 
print("   • enhanced_usage_rgt.csv")

# Sample advanced calculations for dashboard
print(f"\n4. ADVANCED RGT CALCULATIONS FOR DASHBOARD")
print("-" * 50)

# Portfolio Balance Score calculation
def calculate_portfolio_balance_score(current_dist, optimal_targets):
    total_deviation = sum(abs(current_dist.get(cat, 0) - target) for cat, target in optimal_targets.items())
    max_possible_deviation = sum(optimal_targets.values())  # If everything was in one category
    balance_score = max(0, 10 - (total_deviation / max_possible_deviation * 10))
    return balance_score

balance_score = calculate_portfolio_balance_score(rgt_percentages, optimal_targets)
print(f"Portfolio Balance Score: {balance_score:.2f}/10.0")

# ROI by Category calculation (simplified)
df_projects['Projected_ROI'] = (df_projects['Planned_Benefits_Annual'] - df_projects['Total_Budget']) / df_projects['Total_Budget'] * 100
roi_by_category = df_projects.groupby('RGT_Category')['Projected_ROI'].mean()

print(f"\nAverage Projected ROI by Category:")
for category, roi in roi_by_category.items():
    print(f"  {category}: {roi:.1f}%")

print(f"\n💡 This comprehensive framework provides {len(df_rgt_metrics)} metrics")
print(f"   across {len(df_rgt_metrics['Metric_Category'].unique())} categories for deep RGT analysis")
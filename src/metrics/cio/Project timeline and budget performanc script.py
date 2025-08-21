import pandas as pd
from datetime import datetime

# Sample enhanced projects data (from previous runs)
projects_data = {
    'Project_ID': ['PQC-001', 'PQC-002', 'PQC-003', 'PQC-004', 'PQC-005'],
    'Project_Name': [
        'Student Portal Upgrade', 'Cloud Migration Phase 1', 'Cybersecurity Enhancement',
        'LMS Modernization', 'Network Infrastructure'],
    'Status': ['In Progress', 'Completed', 'In Progress', 'Planning', 'In Progress'],
    'Total_Budget': [250000, 450000, 300000, 180000, 220000],
    'Spent_to_Date': [175000, 445000, 125000, 25000, 165000],
    'Start_Date': pd.to_datetime(['2024-01-15', '2023-09-01', '2024-02-01', '2024-06-01', '2023-12-01']),
    'End_Date': pd.to_datetime(['2024-08-30', '2024-03-15', '2024-12-31', '2025-01-31', '2024-09-30'])
}

projects = pd.DataFrame(projects_data)

# Calculate timeline metrics
today = pd.to_datetime('2025-08-19')
projects['Duration_days'] = (projects['End_Date'] - projects['Start_Date']).dt.days
projects['Elapsed_days'] = (today - projects['Start_Date']).dt.days.clip(lower=0)
projects['Timeline_Completion_%'] = (projects['Elapsed_days'] / projects['Duration_days'] * 100).clip(upper=100).round(1)

# Budget metrics
projects['Budget_Variance_%'] = ((projects['Spent_to_Date'] - projects['Total_Budget']) / projects['Total_Budget'] * 100).round(1)
projects['Budget_Status'] = projects['Budget_Variance_%'].apply(
    lambda x: 'Over Budget' if x > 5 else ('Under Budget' if x < -5 else 'On Track')
)

# Real-time project status
projects['Time_Status'] = projects.apply(
    lambda row: 'Delayed' if row['Timeline_Completion_%'] > 100 and row['Status'] != 'Completed' else 
                'On Track' if row['Timeline_Completion_%'] < 100 or row['Status'] == 'Completed' else 
                'Unknown', axis=1
)

# Save to CSV for dashboard integration
projects.to_csv('project_timeline_budget_performance.csv', index=False)
print("PROJECT TIMELINE & BUDGET PERFORMANCE METRICS CALCULATED & SAVED.")
print(projects[['Project_ID','Project_Name','Status','Duration_days','Elapsed_days','Timeline_Completion_%','Total_Budget','Spent_to_Date','Budget_Variance_%','Budget_Status','Time_Status']])
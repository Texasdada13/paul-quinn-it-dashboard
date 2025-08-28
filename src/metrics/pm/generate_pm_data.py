#!/usr/bin/env python3
"""
Project Manager Metrics Data Generator
Creates comprehensive project management data following the enterprise blueprint
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import uuid

# Set random seed for reproducibility
np.random.seed(42)

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Generating Project Manager metrics data in: {current_dir}")
print("=" * 70)

# Generate date range
end_date = datetime.now()
start_date = end_date - timedelta(days=365)  # Full year of data
dates = pd.date_range(start=start_date, end=end_date, freq='D')
weekly_dates = pd.date_range(start=start_date, end=end_date, freq='W')
monthly_dates = pd.date_range(start=start_date, end=end_date, freq='M')

print("\nGenerating Project Manager Data Files:")
print("-" * 40)

# Base project data
projects = [
    {
        'id': 'PQC-001', 'name': 'Student Portal Upgrade', 'type': 'Infrastructure',
        'priority': 'High', 'budget': 250000, 'start_date': '2024-01-15', 'end_date': '2024-08-30'
    },
    {
        'id': 'PQC-002', 'name': 'Cloud Migration Phase 1', 'type': 'Transformation', 
        'priority': 'High', 'budget': 450000, 'start_date': '2023-09-01', 'end_date': '2024-03-15'
    },
    {
        'id': 'PQC-003', 'name': 'Cybersecurity Enhancement', 'type': 'Security',
        'priority': 'Critical', 'budget': 300000, 'start_date': '2024-02-01', 'end_date': '2024-12-31'
    },
    {
        'id': 'PQC-004', 'name': 'LMS Modernization', 'type': 'Academic',
        'priority': 'Medium', 'budget': 180000, 'start_date': '2024-06-01', 'end_date': '2025-01-31'
    },
    {
        'id': 'PQC-005', 'name': 'Network Infrastructure', 'type': 'Infrastructure',
        'priority': 'High', 'budget': 220000, 'start_date': '2023-12-01', 'end_date': '2024-09-30'
    },
    {
        'id': 'PQC-006', 'name': 'AI Tutoring System', 'type': 'Innovation',
        'priority': 'Medium', 'budget': 400000, 'start_date': '2024-07-01', 'end_date': '2025-03-31'
    },
    {
        'id': 'PQC-007', 'name': 'Campus WiFi Expansion', 'type': 'Infrastructure',
        'priority': 'Low', 'budget': 150000, 'start_date': '2023-08-15', 'end_date': '2023-12-31'
    },
    {
        'id': 'PQC-008', 'name': 'Data Analytics Platform', 'type': 'Analytics',
        'priority': 'High', 'budget': 350000, 'start_date': '2024-03-01', 'end_date': '2024-11-30'
    }
]

# ============================================
# 1. PROJECT CHARTER METRICS
# ============================================
print("\n1. project_charter_metrics.csv")

charter_data = []
for project in projects:
    charter_data.append({
        'project_id': project['id'],
        'project_name': project['name'],
        'project_type': project['type'],
        'priority': project['priority'],
        'requesting_department': np.random.choice(['Academic Affairs', 'IT Operations', 'Student Services', 'Administration']),
        'executive_sponsor': np.random.choice(['Dr. Smith', 'Ms. Johnson', 'Mr. Davis', 'Dr. Williams']),
        'project_manager': np.random.choice(['Alice Chen', 'Bob Rodriguez', 'Carol Kim', 'David Thompson']),
        'total_budget': project['budget'],
        'project_start_date': project['start_date'],
        'target_end_date': project['end_date'],
        'approval_status': np.random.choice(['Approved', 'Pending', 'Under Review'], p=[0.8, 0.1, 0.1]),
        'business_justification_score': np.random.uniform(7.0, 9.5),
        'strategic_alignment_score': np.random.uniform(6.5, 9.0),
        'scope_clarity_rating': np.random.uniform(7.0, 10.0),
        'stakeholder_buy_in': np.random.uniform(70, 95),
        'success_criteria_defined': np.random.choice(['Yes', 'Partial', 'No'], p=[0.7, 0.2, 0.1]),
        'charter_approval_date': pd.to_datetime(project['start_date']) - timedelta(days=np.random.randint(30, 90)),
        'last_updated': datetime.now() - timedelta(days=np.random.randint(1, 30))
    })

df_charter = pd.DataFrame(charter_data)
df_charter.to_csv(os.path.join(current_dir, 'project_charter_metrics.csv'), index=False)
print(f"  ✓ Created ({len(df_charter)} rows)")

# ============================================
# 2. PROJECT TIMELINE & BUDGET PERFORMANCE
# ============================================
print("\n2. project_timeline_budget_performance.csv")

timeline_data = []
for project in projects:
    project_start = pd.to_datetime(project['start_date'])
    project_end = pd.to_datetime(project['end_date'])
    duration = (project_end - project_start).days
    elapsed = min(duration, (datetime.now() - project_start).days)
    
    # Calculate realistic spend pattern
    if elapsed > 0:
        spend_rate = np.random.uniform(0.8, 1.2)  # Some variance in spend rate
        spent_to_date = min(project['budget'], (elapsed / duration) * project['budget'] * spend_rate)
    else:
        spent_to_date = 0
    
    # Determine status
    if elapsed >= duration:
        status = 'Completed'
    elif elapsed > duration * 0.1:
        status = 'In Progress'
    else:
        status = 'Planning'
    
    timeline_completion = min(100, (elapsed / duration) * 100) if duration > 0 else 0
    budget_variance = ((spent_to_date - (elapsed / duration * project['budget'])) / project['budget'] * 100) if project['budget'] > 0 else 0
    
    timeline_data.append({
        'project_id': project['id'],
        'project_name': project['name'],
        'status': status,
        'total_budget': project['budget'],
        'spent_to_date': spent_to_date,
        'start_date': project['start_date'],
        'target_end_date': project['end_date'],
        'current_end_date': project['end_date'],  # Could be different if delayed
        'duration_days': duration,
        'elapsed_days': max(0, elapsed),
        'timeline_completion_pct': timeline_completion,
        'budget_variance_pct': budget_variance,
        'budget_status': 'Over Budget' if budget_variance > 5 else ('Under Budget' if budget_variance < -5 else 'On Track'),
        'schedule_status': 'On Track' if status == 'Completed' or timeline_completion <= 100 else 'Delayed',
        'health_score': np.random.uniform(6.5, 9.5),
        'team_size': np.random.randint(3, 12),
        'deliverables_completed': np.random.randint(0, 8),
        'deliverables_total': np.random.randint(5, 15),
        'last_updated': datetime.now()
    })

df_timeline = pd.DataFrame(timeline_data)
df_timeline.to_csv(os.path.join(current_dir, 'project_timeline_budget_performance.csv'), index=False)
print(f"  ✓ Created ({len(df_timeline)} rows)")

# ============================================
# 3. REQUIREMENTS TRACEABILITY MATRIX
# ============================================
print("\n3. requirements_traceability_matrix.csv")

requirements_data = []
requirement_types = ['Functional', 'Non-Functional', 'Business', 'Technical', 'Compliance']
statuses = ['Identified', 'Approved', 'In Development', 'Testing', 'Completed']

for project in projects:
    num_requirements = np.random.randint(8, 25)
    for i in range(num_requirements):
        requirements_data.append({
            'project_id': project['id'],
            'project_name': project['name'],
            'requirement_id': f"{project['id']}-REQ-{i+1:03d}",
            'requirement_name': f"Requirement {i+1}",
            'requirement_type': np.random.choice(requirement_types),
            'priority': np.random.choice(['Critical', 'High', 'Medium', 'Low'], p=[0.2, 0.3, 0.4, 0.1]),
            'status': np.random.choice(statuses, p=[0.1, 0.2, 0.3, 0.2, 0.2]),
            'source': np.random.choice(['Business User', 'Technical Team', 'Compliance', 'Stakeholder']),
            'owner': np.random.choice(['Alice Chen', 'Bob Rodriguez', 'Carol Kim', 'David Thompson']),
            'completion_pct': np.random.uniform(0, 100),
            'test_coverage_pct': np.random.uniform(0, 90),
            'date_identified': pd.to_datetime(project['start_date']) + timedelta(days=np.random.randint(0, 60)),
            'target_completion': pd.to_datetime(project['end_date']) - timedelta(days=np.random.randint(30, 90)),
            'effort_estimate_hours': np.random.randint(8, 120),
            'actual_effort_hours': np.random.randint(5, 150),
            'complexity_score': np.random.randint(1, 10),
            'risk_level': np.random.choice(['Low', 'Medium', 'High'], p=[0.5, 0.3, 0.2])
        })

df_requirements = pd.DataFrame(requirements_data)
df_requirements.to_csv(os.path.join(current_dir, 'requirements_traceability_matrix.csv'), index=False)
print(f"  ✓ Created ({len(df_requirements)} rows)")

# ============================================
# 4. RAID LOG (Risks, Actions, Issues, Decisions)
# ============================================
print("\n4. raid_log_metrics.csv")

raid_data = []
raid_types = ['Risk', 'Action', 'Issue', 'Decision']
severities = ['Low', 'Medium', 'High', 'Critical']
statuses = ['Open', 'In Progress', 'Resolved', 'Closed']

for project in projects:
    num_items = np.random.randint(10, 30)
    for i in range(num_items):
        item_type = np.random.choice(raid_types)
        severity = np.random.choice(severities, p=[0.4, 0.3, 0.2, 0.1])
        status = np.random.choice(statuses, p=[0.2, 0.3, 0.3, 0.2])
        
        raid_data.append({
            'project_id': project['id'],
            'project_name': project['name'],
            'raid_id': f"{project['id']}-{item_type[:1]}-{i+1:03d}",
            'type': item_type,
            'title': f"{item_type} {i+1} for {project['name']}",
            'description': f"Sample {item_type.lower()} description",
            'severity': severity,
            'status': status,
            'owner': np.random.choice(['Alice Chen', 'Bob Rodriguez', 'Carol Kim', 'David Thompson']),
            'date_identified': pd.to_datetime(project['start_date']) + timedelta(days=np.random.randint(0, 200)),
            'target_date': datetime.now() + timedelta(days=np.random.randint(1, 90)),
            'actual_resolution_date': datetime.now() - timedelta(days=np.random.randint(1, 60)) if status in ['Resolved', 'Closed'] else None,
            'days_open': np.random.randint(1, 120),
            'impact_score': np.random.randint(1, 10),
            'probability_score': np.random.randint(1, 10) if item_type == 'Risk' else None,
            'mitigation_plan': 'Sample mitigation plan',
            'category': np.random.choice(['Technical', 'Resource', 'Schedule', 'Budget', 'Quality']),
            'escalated': np.random.choice([True, False], p=[0.2, 0.8])
        })

df_raid = pd.DataFrame(raid_data)
df_raid.to_csv(os.path.join(current_dir, 'raid_log_metrics.csv'), index=False)
print(f"  ✓ Created ({len(df_raid)} rows)")

# ============================================
# 5. RESOURCE ALLOCATION METRICS
# ============================================
print("\n5. resource_allocation_metrics.csv")

resource_data = []
roles = ['Project Manager', 'Business Analyst', 'Developer', 'QA Tester', 'Designer', 'Architect']

for project in projects:
    team_size = np.random.randint(4, 12)
    for i in range(team_size):
        resource_data.append({
            'project_id': project['id'],
            'project_name': project['name'],
            'resource_id': f"RES-{i+1:03d}",
            'resource_name': f"Team Member {i+1}",
            'role': np.random.choice(roles),
            'allocation_pct': np.random.uniform(25, 100),
            'hourly_rate': np.random.uniform(75, 150),
            'total_allocated_hours': np.random.uniform(100, 800),
            'hours_consumed': np.random.uniform(50, 600),
            'utilization_pct': np.random.uniform(70, 95),
            'cost_to_date': np.random.uniform(5000, 80000),
            'efficiency_score': np.random.uniform(7.0, 9.5),
            'skill_match_score': np.random.uniform(7.5, 10.0),
            'availability_pct': np.random.uniform(80, 100),
            'start_date': pd.to_datetime(project['start_date']) + timedelta(days=np.random.randint(0, 30)),
            'end_date': pd.to_datetime(project['end_date']) - timedelta(days=np.random.randint(0, 30)),
            'department': np.random.choice(['IT', 'Business', 'External Contractor']),
            'certification_level': np.random.choice(['Junior', 'Mid-Level', 'Senior', 'Expert'])
        })

df_resources = pd.DataFrame(resource_data)
df_resources.to_csv(os.path.join(current_dir, 'resource_allocation_metrics.csv'), index=False)
print(f"  ✓ Created ({len(df_resources)} rows)")

# ============================================
# 6. STAKEHOLDER COMMUNICATION METRICS
# ============================================
print("\n6. stakeholder_communication_metrics.csv")

communication_data = []
stakeholder_types = ['Executive Sponsor', 'Business Owner', 'End User', 'IT Team', 'Vendor']
communication_types = ['Status Report', 'Meeting', 'Email Update', 'Presentation', 'Workshop']

for date in weekly_dates[-26:]:  # Last 6 months of weekly data
    for project in projects[:6]:  # Don't generate for all projects to keep data realistic
        num_communications = np.random.randint(1, 5)
        for i in range(num_communications):
            communication_data.append({
                'date': date,
                'project_id': project['id'],
                'project_name': project['name'],
                'communication_id': f"{project['id']}-COMM-{uuid.uuid4().hex[:6]}",
                'stakeholder_type': np.random.choice(stakeholder_types),
                'communication_type': np.random.choice(communication_types),
                'frequency': np.random.choice(['Weekly', 'Bi-weekly', 'Monthly', 'Ad-hoc']),
                'attendance_pct': np.random.uniform(60, 95),
                'engagement_score': np.random.uniform(6.0, 9.5),
                'satisfaction_score': np.random.uniform(7.0, 9.0),
                'action_items_generated': np.random.randint(0, 8),
                'issues_escalated': np.random.randint(0, 3),
                'feedback_received': np.random.choice([True, False], p=[0.7, 0.3]),
                'delivery_method': np.random.choice(['In-Person', 'Virtual', 'Email', 'Dashboard']),
                'response_time_hours': np.random.uniform(2, 48),
                'follow_up_required': np.random.choice([True, False], p=[0.4, 0.6])
            })

df_communication = pd.DataFrame(communication_data)
df_communication.to_csv(os.path.join(current_dir, 'stakeholder_communication_metrics.csv'), index=False)
print(f"  ✓ Created ({len(df_communication)} rows)")

# ============================================
# 7. PROJECT PORTFOLIO DASHBOARD METRICS
# ============================================
print("\n7. project_portfolio_dashboard_metrics.csv")

portfolio_data = []
for date in monthly_dates[-12:]:  # Last 12 months
    active_projects = np.random.randint(5, 8)
    completed_projects = np.random.randint(2, 5)
    planned_projects = np.random.randint(1, 4)
    
    portfolio_data.append({
        'date': date,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'planned_projects': planned_projects,
        'total_portfolio_budget': np.random.uniform(2000000, 3500000),
        'total_spent_ytd': np.random.uniform(1200000, 2800000),
        'budget_variance_pct': np.random.uniform(-10, 15),
        'avg_project_health_score': np.random.uniform(7.5, 9.0),
        'on_time_delivery_rate': np.random.uniform(75, 90),
        'on_budget_delivery_rate': np.random.uniform(70, 85),
        'stakeholder_satisfaction_avg': np.random.uniform(7.8, 9.2),
        'resource_utilization_pct': np.random.uniform(80, 95),
        'high_risk_projects': np.random.randint(0, 3),
        'overdue_milestones': np.random.randint(0, 8),
        'change_requests_pending': np.random.randint(2, 12),
        'benefits_realization_pct': np.random.uniform(65, 85),
        'innovation_projects_pct': np.random.uniform(15, 35)
    })

df_portfolio = pd.DataFrame(portfolio_data)
df_portfolio.to_csv(os.path.join(current_dir, 'project_portfolio_dashboard_metrics.csv'), index=False)
print(f"  ✓ Created ({len(df_portfolio)} rows)")

print("\n" + "=" * 70)
print("✅ SUCCESS! All Project Manager metric data files generated")
print("=" * 70)

# List created files
created_files = [
    'project_charter_metrics.csv',
    'project_timeline_budget_performance.csv',
    'requirements_traceability_matrix.csv',
    'raid_log_metrics.csv',
    'resource_allocation_metrics.csv',
    'stakeholder_communication_metrics.csv',
    'project_portfolio_dashboard_metrics.csv'
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
print(f"\n🚀 Next step: Create display functions in pm_metrics_display.py")
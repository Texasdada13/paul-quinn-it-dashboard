"""
Robust Mock Data Generator for Paul Quinn College
Creates comprehensive, realistic data showing full potential of the platform
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_robust_mock_data():
    """Generate comprehensive mock data for all aspects of IT effectiveness"""
    
    print("🎓 Generating Robust Mock Data for Paul Quinn College...")
    print("=" * 60)
    
    # 1. COMPREHENSIVE VENDOR DATA (50+ vendors)
    print("\n1. Creating Vendor Database...")
    
    vendor_categories = {
        'Enterprise Software': ['Oracle', 'Microsoft', 'Salesforce', 'Workday', 'Banner by Ellucian'],
        'Academic Software': ['Canvas LMS', 'Blackboard', 'Turnitin', 'Respondus', 'Panopto'],
        'Productivity': ['Office 365', 'Google Workspace', 'Zoom', 'Slack', 'Adobe Creative Cloud'],
        'Infrastructure': ['VMware', 'Cisco', 'Dell EMC', 'HPE', 'Fortinet'],
        'Cloud Services': ['AWS', 'Azure', 'Google Cloud', 'Dropbox Business', 'Box'],
        'Security': ['CrowdStrike', 'Okta', 'Duo Security', 'Proofpoint', 'Splunk'],
        'Specialized': ['Tableau', 'MATLAB', 'SPSS', 'AutoCAD', 'ArcGIS'],
        'IT Services': ['CDW', 'SHI', 'Insight', 'Connection', 'Zones']
    }
    
    vendors_data = []
    for category, vendor_list in vendor_categories.items():
        for vendor in vendor_list:
            # Realistic spend distribution
            if vendor in ['Oracle', 'Banner by Ellucian', 'Microsoft']:
                annual_spend = random.randint(100000, 300000)
            elif category == 'IT Services':
                annual_spend = random.randint(50000, 150000)
            else:
                annual_spend = random.randint(5000, 75000)
            
            vendors_data.append({
                'vendor_id': f'V{len(vendors_data)+1:03d}',
                'vendor_name': vendor,
                'category': category,
                'subcategory': random.choice(['Core', 'Supporting', 'Strategic']),
                'annual_spend': annual_spend,
                'contract_start': datetime.now() - timedelta(days=random.randint(30, 730)),
                'contract_end': datetime.now() + timedelta(days=random.randint(30, 730)),
                'payment_terms': random.choice(['Annual', 'Monthly', 'Quarterly']),
                'risk_level': np.random.choice(['Low', 'Medium', 'High'], p=[0.6, 0.3, 0.1]),
                'satisfaction_score': round(random.uniform(3.0, 5.0), 1),
                'users': random.randint(10, 1200),
                'compliance_status': random.choice(['Compliant', 'Review Needed', 'Non-Compliant']),
                'auto_renewal': random.choice(['Yes', 'No']),
                'business_critical': random.choice(['Yes', 'No']),
                'last_review_date': datetime.now() - timedelta(days=random.randint(30, 180))
            })
    
    vendors_df = pd.DataFrame(vendors_data)
    
    # 2. DETAILED PROJECT PORTFOLIO (30+ projects)
    print("2. Creating Project Portfolio...")
    
    project_types = {
        'Infrastructure': ['Network Upgrade', 'Server Refresh', 'Storage Expansion', 'Disaster Recovery'],
        'Applications': ['ERP Upgrade', 'CRM Implementation', 'Portal Development', 'Mobile App'],
        'Security': ['Firewall Upgrade', 'Identity Management', 'Security Training', 'Pen Testing'],
        'Academic': ['LMS Migration', 'Virtual Labs', 'Classroom Tech', 'Student Success Platform'],
        'Digital Transform': ['Cloud Migration', 'Process Automation', 'AI Pilot', 'Analytics Platform']
    }
    
    projects_data = []
    for category, project_list in project_types.items():
        for project in project_list:
            budget = random.randint(25000, 500000)
            progress = random.uniform(0.1, 0.95)
            
            projects_data.append({
                'project_id': f'P{len(projects_data)+1:03d}',
                'project_name': f'{project} {random.choice(["Phase 1", "Phase 2", "2024", "Initiative"])}',
                'category': category,
                'type': random.choice(['Run', 'Grow', 'Transform']),
                'department': random.choice(['IT', 'Academic Affairs', 'Student Services', 'Finance', 'Administration']),
                'status': np.random.choice(['Planning', 'In Progress', 'At Risk', 'On Hold', 'Completed'], 
                                         p=[0.2, 0.5, 0.1, 0.1, 0.1]),
                'health': np.random.choice(['Green', 'Yellow', 'Red'], p=[0.6, 0.3, 0.1]),
                'priority': random.choice(['High', 'Medium', 'Low']),
                'budget': budget,
                'spent_to_date': int(budget * progress * random.uniform(0.8, 1.2)),
                'percent_complete': int(progress * 100),
                'start_date': datetime.now() - timedelta(days=random.randint(30, 365)),
                'target_end_date': datetime.now() + timedelta(days=random.randint(30, 365)),
                'business_value_score': random.randint(1, 10),
                'risk_score': random.randint(1, 10),
                'resource_count': random.randint(1, 10),
                'dependencies': random.randint(0, 5)
            })
    
    projects_df = pd.DataFrame(projects_data)
    
    # 3. SYSTEMS PERFORMANCE DATA
    print("3. Creating Systems Performance Data...")
    
    systems = [
        ('Banner ERP', 'Enterprise Application', 1200, 'Mission Critical'),
        ('Canvas LMS', 'Academic System', 5000, 'Mission Critical'),
        ('Office 365', 'Productivity', 1500, 'Business Critical'),
        ('Student Portal', 'Custom Application', 5000, 'Business Critical'),
        ('Financial Aid System', 'Enterprise Application', 800, 'Mission Critical'),
        ('Library System', 'Academic System', 3000, 'Important'),
        ('HR System', 'Enterprise Application', 500, 'Business Critical'),
        ('Ticketing System', 'IT Service', 1500, 'Important'),
        ('Backup System', 'Infrastructure', 50, 'Mission Critical'),
        ('Email System', 'Communication', 1500, 'Mission Critical')
    ]
    
    systems_data = []
    performance_data = []
    
    for system_name, system_type, users, criticality in systems:
        # System inventory
        systems_data.append({
            'system_name': system_name,
            'system_type': system_type,
            'users': users,
            'criticality': criticality,
            'age_years': random.randint(1, 10),
            'last_upgrade': datetime.now() - timedelta(days=random.randint(90, 730)),
            'vendor': random.choice(list(vendors_df['vendor_name'])),
            'hosting': random.choice(['On-Premise', 'Cloud', 'Hybrid']),
            'recovery_time_objective': random.choice(['4 hours', '8 hours', '24 hours', '72 hours']),
            'annual_cost': random.randint(10000, 200000)
        })
        
        # Monthly performance metrics - Fixed frequency parameter
        for month in pd.date_range(start='2024-01-01', end='2024-12-31', freq='ME'):
            performance_data.append({
                'system_name': system_name,
                'month': month,
                'availability_pct': random.uniform(98.5, 99.99),
                'response_time_ms': random.uniform(100, 1000),
                'incidents': random.randint(0, 10),
                'tickets': random.randint(5, 50),
                'user_satisfaction': random.uniform(3.5, 5.0),
                'cpu_utilization': random.uniform(20, 80),
                'storage_utilization': random.uniform(30, 90)
            })
    
    systems_df = pd.DataFrame(systems_data)
    performance_df = pd.DataFrame(performance_data)
    
    # 4. FINANCIAL TRENDING DATA
    print("4. Creating Financial Trending Data...")
    
    financial_data = []
    categories = ['Hardware', 'Software', 'Cloud Services', 'Professional Services', 'Salaries', 'Other']
    
    for year in range(2021, 2025):
        for month in range(1, 13):
            if year == 2024 and month > 6:  # Only up to June 2024
                break
            
            for category in categories:
                base_amount = {
                    'Hardware': 30000,
                    'Software': 50000,
                    'Cloud Services': 20000,
                    'Professional Services': 15000,
                    'Salaries': 150000,
                    'Other': 10000
                }[category]
                
                financial_data.append({
                    'date': datetime(year, month, 1),
                    'category': category,
                    'budget': base_amount * (1 + (year - 2021) * 0.05),  # 5% annual increase
                    'actual': base_amount * (1 + (year - 2021) * 0.05) * random.uniform(0.85, 1.15),
                    'forecast': base_amount * (1 + (year - 2021) * 0.05) * 1.02
                })
    
    financial_df = pd.DataFrame(financial_data)
    
    # 5. HELP DESK & INCIDENT DATA
    print("5. Creating Help Desk Data...")
    
    ticket_data = []
    categories = ['Hardware', 'Software', 'Network', 'Account', 'Other']
    priorities = ['Low', 'Medium', 'High', 'Critical']
    
    for i in range(2000):  # 2000 tickets
        created_date = datetime.now() - timedelta(days=random.randint(0, 365))
        # Fixed: Use numpy's exponential instead of random's
        resolution_hours = np.random.exponential(scale=24)  # Most resolved quickly
        
        ticket_data.append({
            'ticket_id': f'T{i+1:05d}',
            'category': random.choice(categories),
            'priority': np.random.choice(priorities, p=[0.4, 0.4, 0.15, 0.05]),
            'created_date': created_date,
            'resolved_date': created_date + timedelta(hours=resolution_hours),
            'resolution_time_hours': resolution_hours,
            'satisfaction_rating': np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.05, 0.15, 0.35, 0.4]),
            'department': random.choice(['IT', 'Academic', 'Admin', 'Student Services', 'Finance']),
            'system_affected': random.choice(systems_df['system_name'].tolist()),
            'resolved_first_contact': random.choice(['Yes', 'No'])
        })
    
    tickets_df = pd.DataFrame(ticket_data)
    
    # 6. STAFF & SKILLS DATA
    print("6. Creating Staff & Skills Data...")
    
    staff_data = []
    skills = ['Network Admin', 'Database Admin', 'Security', 'Cloud', 'Programming', 
              'Project Management', 'Business Analysis', 'Help Desk']
    
    for i in range(25):  # 25 IT staff
        staff_data.append({
            'staff_id': f'S{i+1:03d}',
            'role': random.choice(['Admin', 'Analyst', 'Engineer', 'Manager', 'Director']),
            'years_experience': random.randint(1, 20),
            'certifications': random.randint(0, 5),
            'primary_skill': random.choice(skills),
            'utilization_pct': random.uniform(60, 95),
            'training_hours_ytd': random.randint(0, 80),
            'satisfaction_score': random.uniform(3.0, 5.0)
        })
    
    staff_df = pd.DataFrame(staff_data)
    
    # 7. BENCHMARK DATA
    print("7. Creating Benchmark Data...")
    
    benchmark_data = {
        'metric': ['IT Spend % Revenue', 'IT Staff per 100 Users', 'Ticket Resolution Time', 
                   'System Availability', 'Project Success Rate', 'User Satisfaction'],
        'paul_quinn': [0.86, 1.5, 18.5, 98.9, 75, 4.2],
        'peer_average': [3.5, 2.0, 24.0, 99.0, 70, 3.8],
        'best_in_class': [2.5, 1.2, 12.0, 99.5, 85, 4.5]
    }
    
    benchmark_df = pd.DataFrame(benchmark_data)
    
    # Save all data to Excel
    print("\n📊 Saving all data to Excel...")
    
    with pd.ExcelWriter('PQC_Robust_Mock_Data.xlsx', engine='xlsxwriter') as writer:
        vendors_df.to_excel(writer, sheet_name='Vendors', index=False)
        projects_df.to_excel(writer, sheet_name='Projects', index=False)
        systems_df.to_excel(writer, sheet_name='Systems', index=False)
        performance_df.to_excel(writer, sheet_name='System_Performance', index=False)
        financial_df.to_excel(writer, sheet_name='Financial_Trending', index=False)
        tickets_df.to_excel(writer, sheet_name='Help_Desk_Tickets', index=False)
        staff_df.to_excel(writer, sheet_name='IT_Staff', index=False)
        benchmark_df.to_excel(writer, sheet_name='Benchmarks', index=False)
    
    # Generate insights summary
    print("\n" + "="*60)
    print("📈 INSIGHTS FROM ROBUST DATA:")
    print("="*60)
    
    print(f"\n💰 FINANCIAL INSIGHTS:")
    print(f"- Total IT Spend: ${vendors_df['annual_spend'].sum():,.0f}")
    print(f"- Largest Category: {vendors_df.groupby('category')['annual_spend'].sum().idxmax()}")
    print(f"- High-Risk Vendors: {len(vendors_df[vendors_df['risk_level'] == 'High'])}")
    print(f"- Potential Savings: ${vendors_df['annual_spend'].sum() * 0.15:,.0f} (15% optimization)")
    
    print(f"\n📊 PROJECT INSIGHTS:")
    print(f"- Active Projects: {len(projects_df[projects_df['status'] == 'In Progress'])}")
    print(f"- At-Risk Projects: {len(projects_df[projects_df['health'] == 'Red'])}")
    print(f"- Portfolio Balance: {projects_df['type'].value_counts().to_dict()}")
    print(f"- Total Project Budget: ${projects_df['budget'].sum():,.0f}")
    
    print(f"\n⚡ OPERATIONAL INSIGHTS:")
    print(f"- Average System Availability: {performance_df['availability_pct'].mean():.2f}%")
    print(f"- Monthly Tickets: {len(tickets_df) / 12:.0f}")
    print(f"- First Contact Resolution: {(tickets_df['resolved_first_contact'] == 'Yes').mean() * 100:.1f}%")
    print(f"- Average Resolution Time: {tickets_df['resolution_time_hours'].mean():.1f} hours")
    
    print(f"\n🎯 STRATEGIC INSIGHTS:")
    print(f"- IT Spend as % Revenue: 0.86% (vs 3.5% peer average)")
    print(f"- Cost per User: ${vendors_df['annual_spend'].sum() / 5000:,.0f}")
    print(f"- Systems Requiring Upgrade: {len(systems_df[systems_df['age_years'] > 5])}")
    print(f"- Staff Utilization: {staff_df['utilization_pct'].mean():.1f}%")
    
    print("\n✅ Files Created:")
    print("1. PQC_Data_Collection_Template.xlsx - Send to client")
    print("2. PQC_Robust_Mock_Data.xlsx - Use for demos/development")

# Generate everything
generate_robust_mock_data()

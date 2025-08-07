"""Create sample data for testing"""

import pandas as pd
import os
import random
from datetime import datetime, timedelta

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
raw_data_folder = os.path.join(project_root, "02_Data", "raw")

# Create folder if it doesn't exist
os.makedirs(raw_data_folder, exist_ok=True)

print("Creating sample data for Paul Quinn College...\n")

# Create sample vendor data
vendors = {
    'Vendor Name': ['Microsoft', 'Adobe', 'Zoom', 'Canvas LMS', 'Dell', 
                    'CDW', 'AWS', 'Google Workspace', 'Blackboard', 'Apple',
                    'Cisco', 'VMware', 'Oracle', 'Salesforce', 'Dropbox'],
    'Category': ['Software', 'Software', 'Communication', 'Education', 'Hardware',
                 'Reseller', 'Cloud', 'Productivity', 'Education', 'Hardware',
                 'Network', 'Virtualization', 'Database', 'CRM', 'Storage'],
    'Annual Spend': [50000, 25000, 6000, 35000, 45000, 
                     30000, 40000, 15000, 28000, 20000,
                     55000, 18000, 42000, 12000, 8000],
    'Contract End Date': [datetime.now() + timedelta(days=random.randint(30, 365)) 
                          for _ in range(15)],
    'Risk Level': random.choices(['Low', 'Medium', 'High'], weights=[50, 35, 15], k=15),
    'Payment Terms': random.choices(['Net 30', 'Net 60', 'Annual', 'Monthly'], k=15)
}

# Save vendor data
vendor_df = pd.DataFrame(vendors)
vendor_file = os.path.join(raw_data_folder, "vendors.xlsx")
vendor_df.to_excel(vendor_file, index=False)
print(f"Created: {vendor_file}")
print(f"-> {len(vendor_df)} vendors with spending data")

# Create sample project data
projects = {
    'Project Name': [
        'Student Portal Upgrade', 
        'Network Infrastructure Refresh', 
        'Classroom Technology Phase 2',
        'Cybersecurity Enhancement',
        'Cloud Migration Phase 1',
        'ERP System Upgrade',
        'Wi-Fi Expansion Project',
        'Digital Learning Initiative'
    ],
    'Department': ['IT', 'IT', 'Academic Affairs', 'IT', 'IT', 
                   'Finance', 'IT', 'Academic Affairs'],
    'Budget': [75000, 120000, 85000, 50000, 95000, 
               150000, 65000, 40000],
    'Spent to Date': [45000, 110000, 40000, 48000, 30000,
                      125000, 20000, 35000],
    'Start Date': pd.to_datetime(['2024-01-15', '2024-02-01', '2024-03-15',
                                  '2024-01-01', '2024-04-01', '2023-11-01',
                                  '2024-05-01', '2024-02-15']),
    'Expected End Date': pd.to_datetime(['2024-12-31', '2024-11-30', '2024-10-31',
                                        '2024-09-30', '2024-12-31', '2024-08-31',
                                        '2024-10-31', '2024-07-31']),
    'Status': ['In Progress', 'In Progress', 'Planning', 'At Risk', 
               'In Progress', 'Delayed', 'Planning', 'In Progress'],
    'Project Manager': ['John Smith', 'Jane Doe', 'Mike Johnson', 'John Smith',
                       'Sarah Williams', 'Jane Doe', 'Mike Johnson', 'Sarah Williams']
}

# Save project data
project_df = pd.DataFrame(projects)
project_file = os.path.join(raw_data_folder, "projects.xlsx")
project_df.to_excel(project_file, index=False)
print(f"Created: {project_file}")
print(f"-> {len(project_df)} active IT projects")

# Create sample monthly spending data
months = pd.date_range('2024-01-01', '2024-06-30', freq='M')
spending_data = []

for _, vendor in vendor_df.iterrows():
    for month in months:
        spending_data.append({
            'Date': month,
            'Vendor': vendor['Vendor Name'],
            'Category': vendor['Category'],
            'Amount': vendor['Annual Spend'] / 12 * random.uniform(0.8, 1.2),
            'Invoice Number': f"INV-{month.strftime('%Y%m')}-{random.randint(1000, 9999)}",
            'Approved By': random.choice(['CFO', 'CIO', 'Finance Manager'])
        })

spending_df = pd.DataFrame(spending_data)
spending_file = os.path.join(raw_data_folder, "monthly_spending.xlsx")
spending_df.to_excel(spending_file, index=False)
print(f"Created: {spending_file}")
print(f"-> {len(spending_df)} monthly transactions")

print(f"\nAll files saved to: {raw_data_folder}")
print("\nNext steps:")
print("1. Run the ETL scripts to process this data")
print("2. Import the cleaned CSV files into Power BI")
print("3. Create dashboards for CFO, CIO, and CTO personas")

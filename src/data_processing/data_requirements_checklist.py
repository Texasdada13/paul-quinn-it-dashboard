"""
Data Requirements Checklist for Paul Quinn College
This script generates a checklist of required data for IT effectiveness measurement
"""

import pandas as pd
from datetime import datetime

# Define data requirements by category
data_requirements = {
    "Category": [],
    "Data Item": [],
    "Required For": [],
    "Format": [],
    "Frequency": [],
    "Current Source": [],
    "Priority": []
}

# Financial Data Requirements
financial_items = [
    ("Total IT Budget", "CFO Dashboard", "Excel/CSV", "Annual", "Finance System", "Critical"),
    ("IT Spend by Category", "Cost Analysis", "Excel/CSV", "Monthly", "AP System", "Critical"),
    ("Vendor Contract Values", "Vendor Analysis", "Excel/CSV", "Quarterly", "Contracts", "Critical"),
    ("Institution Revenue", "Benchmark %", "Number", "Annual", "Finance", "High"),
    ("Grant Allocations", "Compliance", "Excel/CSV", "As needed", "Grants Office", "Medium"),
    ("Historical Spend (3yr)", "Trending", "Excel/CSV", "One-time", "Finance", "High")
]

# Operational Data Requirements
operational_items = [
    ("Active Project List", "Portfolio Mgmt", "Excel/CSV", "Weekly", "PMO", "Critical"),
    ("System Uptime Logs", "Reliability", "CSV/API", "Daily", "Monitoring", "Critical"),
    ("License Utilization", "Optimization", "Report/API", "Monthly", "Vendors", "High"),
    ("Help Desk Tickets", "Service Quality", "CSV/Export", "Weekly", "Service Desk", "High"),
    ("User Count by System", "Adoption", "CSV", "Monthly", "IT/HR", "Medium"),
    ("Security Incidents", "Risk Mgmt", "Log/CSV", "Weekly", "Security", "High")
]

# Strategic Data Requirements
strategic_items = [
    ("Strategic Plan", "Alignment", "Document", "Annual", "Leadership", "High"),
    ("Peer Benchmarks", "Comparison", "Report", "Annual", "Research", "Medium"),
    ("Student Outcomes", "ROI Linkage", "CSV", "Semester", "Registrar", "High"),
    ("Staff Satisfaction", "Value Metric", "Survey", "Annual", "HR", "Medium"),
    ("Digital Roadmap", "Planning", "Document", "Annual", "IT Leadership", "High")
]

# Build the complete requirements list
for category, items in [("Financial", financial_items), 
                        ("Operational", operational_items), 
                        ("Strategic", strategic_items)]:
    for item in items:
        data_requirements["Category"].append(category)
        data_requirements["Data Item"].append(item[0])
        data_requirements["Required For"].append(item[1])
        data_requirements["Format"].append(item[2])
        data_requirements["Frequency"].append(item[3])
        data_requirements["Current Source"].append(item[4])
        data_requirements["Priority"].append(item[5])

# Create DataFrame
df = pd.DataFrame(data_requirements)

# Save to CSV
df.to_csv("paul_quinn_data_requirements.csv", index=False)

print("DATA REQUIREMENTS CHECKLIST FOR PAUL QUINN COLLEGE")
print("=" * 60)
print(f"Generated: {datetime.now().strftime('%B %d, %Y')}")
print("=" * 60)

# Show summary by priority
print("\nDATA PRIORITIES:")
priority_summary = df.groupby(['Priority', 'Category']).size().unstack(fill_value=0)
print(priority_summary)

print("\n\nCRITICAL DATA ITEMS (Must Have for MVP):")
critical = df[df['Priority'] == 'Critical']
for _, row in critical.iterrows():
    print(f"✓ {row['Data Item']} - {row['Current Source']} ({row['Format']})")

print("\n\nMINIMUM VIABLE DATASET:")
print("1. Current year IT budget broken down by category")
print("2. List of all vendors with contract values")
print("3. List of active IT projects with budgets/status")
print("4. System uptime reports for last 3 months")
print("5. License counts and usage reports")

print("\n\nQUESTIONS FOR PAUL QUINN:")
print("1. What financial system do you use? (Banner, Workday, etc.)")
print("2. Do you have a formal PMO tracking projects?")
print("3. What monitoring tools are in place?")
print("4. How do you currently track vendor contracts?")
print("5. What format are most reports in currently?")

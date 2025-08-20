"""
Combined spending analysis for Power BI
"""

import pandas as pd
import os

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
processed_folder = os.path.join(project_root, "02_Data", "processed")

print("Creating combined analysis for Power BI...\n")

# Read processed data
vendors = pd.read_csv(os.path.join(processed_folder, "clean_vendors.csv"))
projects = pd.read_csv(os.path.join(processed_folder, "clean_projects.csv"))
spending = pd.read_excel(os.path.join(project_root, "02_Data", "raw", "monthly_spending.xlsx"))

# Create summary metrics (note: column names now use underscores)
summary = {
    'Total Vendors': len(vendors),
    'Total Annual Vendor Spend': vendors['annual_spend'].sum(),
    'Active Projects': len(projects),
    'Total Project Budget': projects['budget'].sum(),
    'Total Project Spend': projects['spent_to_date'].sum(),
    'High Risk Items': len(vendors[vendors['risk_level'] == 'High']) + len(projects[projects['risk_flag'] == 'HIGH'])
}

# Save summary
summary_df = pd.DataFrame([summary])
summary_df.to_csv(os.path.join(processed_folder, "executive_summary.csv"), index=False)

print("Executive Summary:")
for key, value in summary.items():
    if 'Spend' in key or 'Budget' in key:
        print(f"- {key}: ${value:,.2f}")
    else:
        print(f"- {key}: {value}")

print(f"\nAll processed files ready for Power BI in: {processed_folder}")

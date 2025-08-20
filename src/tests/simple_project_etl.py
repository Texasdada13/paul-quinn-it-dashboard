import pandas as pd
import os
from datetime import datetime

print("Simple Project ETL - Starting...\n")

# Read projects
projects_path = "02_Data/raw/projects.xlsx"
print(f"Reading: {projects_path}")

df = pd.read_excel(projects_path)
print(f"Found {len(df)} projects")

# Clean and enhance data
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df['budget_remaining'] = df['budget'] - df['spent_to_date']
df['budget_utilization_%'] = (df['spent_to_date'] / df['budget'] * 100).round(2)

# Risk flag
df['risk_flag'] = df.apply(
    lambda row: 'HIGH' if row['status'] == 'At Risk' or row['budget_utilization_%'] > 90 
    else 'MEDIUM' if row['budget_utilization_%'] > 75 
    else 'LOW', axis=1
)

# Save
output_path = "02_Data/processed/clean_projects.csv"
df.to_csv(output_path, index=False)
print(f"\nSaved to: {output_path}")
print("✓ Done!")

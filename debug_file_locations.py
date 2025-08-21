"""
Debug script to find where files are located
"""

import os
from pathlib import Path

print("Current working directory:", os.getcwd())
print("\nLooking for src folder...")

# Check if src exists
if os.path.exists('src'):
    print("✓ src folder found")
    
    # Check for metrics folder
    if os.path.exists('src/metrics'):
        print("✓ src/metrics folder found")
        
        # List all folders in metrics
        print("\nFolders in src/metrics:")
        for item in os.listdir('src/metrics'):
            item_path = os.path.join('src/metrics', item)
            if os.path.isdir(item_path):
                print(f"  - {item}/")
                
                # List files in each subfolder
                files = os.listdir(item_path)
                for file in files[:5]:  # Show first 5 files
                    print(f"    • {file}")
                if len(files) > 5:
                    print(f"    ... and {len(files) - 5} more files")
    else:
        print("✗ src/metrics folder NOT found")
else:
    print("✗ src folder NOT found")

print("\n" + "="*50)
print("Checking specific CFO files:")
print("="*50)

# Check for specific CFO files
cfo_files = [
    'src/metrics/cfo/cfo_budget_vs_actual_module.py',
    'src/metrics/cfo/cfo_budget_vs_actual_examples.csv',
    'src/metrics/cfo/cfo_contract_expiration_alerts_module.py',
    'src/metrics/cfo/cfo_contract_expiration_alerts_examples.csv'
]

for file_path in cfo_files:
    if os.path.exists(file_path):
        print(f"✓ Found: {file_path}")
        
        # If it's a CSV, show columns
        if file_path.endswith('.csv'):
            try:
                import pandas as pd
                df = pd.read_csv(file_path)
                print(f"  Columns: {list(df.columns)}")
            except Exception as e:
                print(f"  Error reading CSV: {e}")
    else:
        print(f"✗ NOT found: {file_path}")

print("\n" + "="*50)
print("Looking for dashboard files:")
print("="*50)

dashboard_files = [
    'src/dashboard/metric_registry.py',
    'src/dashboard/dashboard_metric_loader.py',
    'src/dashboard/fully_integrated_dashboard.py'
]

for file_path in dashboard_files:
    if os.path.exists(file_path):
        print(f"✓ Found: {file_path}")
    else:
        print(f"✗ NOT found: {file_path}")
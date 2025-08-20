import os
import pandas as pd

print("Debug: Checking file paths...\n")

# Check current directory
print(f"Current working directory: {os.getcwd()}")

# Check if raw data exists
raw_path = "02_Data/raw/vendors.xlsx"
if os.path.exists(raw_path):
    print(f"✓ Found: {raw_path}")
    df = pd.read_excel(raw_path)
    print(f"  Contains {len(df)} rows")
else:
    print(f"✗ Missing: {raw_path}")

# Check if processed folder exists
processed_path = "02_Data/processed"
if os.path.exists(processed_path):
    print(f"✓ Processed folder exists")
else:
    print(f"✗ Processed folder missing")
    os.makedirs(processed_path, exist_ok=True)
    print(f"  Created: {processed_path}")

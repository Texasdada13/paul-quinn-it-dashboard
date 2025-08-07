import pandas as pd
import os
from datetime import datetime

print("Simple Vendor ETL - Starting...\n")

# Read vendors
vendors_path = "02_Data/raw/vendors.xlsx"
print(f"Reading: {vendors_path}")

df = pd.read_excel(vendors_path)
print(f"Found {len(df)} vendors")
print(f"Columns: {list(df.columns)}")

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df['processed_date'] = datetime.now()

# Create processed folder
os.makedirs("02_Data/processed", exist_ok=True)

# Save to CSV
output_path = "02_Data/processed/clean_vendors.csv"
df.to_csv(output_path, index=False)
print(f"\nSaved to: {output_path}")

# Verify file was created
if os.path.exists(output_path):
    print("✓ File created successfully!")
    print(f"  File size: {os.path.getsize(output_path)} bytes")

print("\nDone!")

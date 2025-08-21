"""
Check CSV column names in metrics folders
"""

import pandas as pd
from pathlib import Path
import os

# Get the path to metrics folder
current_dir = Path.cwd()
metrics_dir = current_dir / 'src' / 'metrics'

print("Checking CSV files in metrics folders...\n")

# Check each persona folder
for persona in ['cfo', 'cio', 'cto', 'hbcu']:
    persona_dir = metrics_dir / persona
    if persona_dir.exists():
        print(f"\n{persona.upper()} Metrics:")
        print("-" * 50)
        
        # Find all CSV files
        csv_files = list(persona_dir.glob('*.csv'))
        
        for csv_file in csv_files:
            print(f"\nFile: {csv_file.name}")
            try:
                df = pd.read_csv(csv_file)
                print(f"Columns: {list(df.columns)}")
                print(f"Shape: {df.shape}")
            except Exception as e:
                print(f"Error reading file: {e}")
                
print("\n\nSpecifically checking budget variance file...")
budget_file = metrics_dir / 'cfo' / 'cfo_budget_vs_actual_examples.csv'
if budget_file.exists():
    df = pd.read_csv(budget_file)
    print(f"Budget variance columns: {list(df.columns)}")
    print(f"First few rows:")
    print(df.head())
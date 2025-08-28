"""
Diagnose CIO Dashboard Issues
This script will identify the exact problem with your CIO metrics
"""

import os
import sys
import pandas as pd

def diagnose_cio_metrics():
    """Diagnose what's wrong with the CIO metrics setup"""
    
    print("=" * 60)
    print("CIO METRICS DIAGNOSTIC TOOL")
    print("=" * 60)
    
    # Check directory structure
    print("\n1. CHECKING DIRECTORY STRUCTURE:")
    print("-" * 40)
    
    # Check if metrics/cio exists
    if os.path.exists('metrics/cio'):
        print("✓ metrics/cio directory exists")
        
        # List all files in metrics/cio
        print("\nFiles in metrics/cio:")
        files = os.listdir('metrics/cio')
        csv_files = []
        py_files = []
        
        for file in sorted(files):
            if file.endswith('.csv'):
                csv_files.append(file)
                size = os.path.getsize(os.path.join('metrics/cio', file))
                print(f"  📄 {file} ({size} bytes)")
            elif file.endswith('.py'):
                py_files.append(file)
                print(f"  🐍 {file}")
        
        print(f"\nFound {len(csv_files)} CSV files and {len(py_files)} Python files")
    else:
        print("✗ metrics/cio directory NOT found")
        return
    
    # Check what the __init__.py expects vs what exists
    print("\n2. CHECKING EXPECTED VS ACTUAL FILES:")
    print("-" * 40)
    
    expected_files = [
        'app_cost_analysis_metrics.csv',
        'business_unit_it_spend.csv',
        'digital_transformation_metrics.csv',
        'risk_metrics.csv',
        'strategic_alignment_metrics.csv',
        'vendor_metrics.csv'
    ]
    
    print("Files expected by __init__.py:")
    for expected in expected_files:
        exists = expected in csv_files
        if exists:
            print(f"  ✓ {expected}")
        else:
            # Check for similar files
            similar = [f for f in csv_files if expected.split('.')[0] in f]
            if similar:
                print(f"  ✗ {expected} NOT FOUND, but found similar: {similar}")
            else:
                print(f"  ✗ {expected} NOT FOUND")
    
    # Check CSV file contents
    print("\n3. CHECKING CSV FILE CONTENTS:")
    print("-" * 40)
    
    for csv_file in csv_files[:6]:  # Check first 6 CSV files
        filepath = os.path.join('metrics/cio', csv_file)
        try:
            df = pd.read_csv(filepath)
            print(f"\n{csv_file}:")
            print(f"  - Rows: {len(df)}")
            print(f"  - Columns: {list(df.columns)[:5]}{'...' if len(df.columns) > 5 else ''}")
            
            # Check for key columns
            key_columns = {
                'app_cost_analysis': ['date', 'application', 'monthly_cost', 'utilization_rate'],
                'business_unit_it_spend': ['date', 'business_unit', 'monthly_budget', 'monthly_spend'],
                'digital_transformation': ['date', 'transformation_score', 'online_adoption_rate'],
                'risk': ['date', 'risk_category', 'risk_heat_map'],
                'strategic_alignment': ['date', 'initiative', 'alignment_score'],
                'vendor': ['date', 'vendor', 'satisfaction_score', 'annual_spend']
            }
            
            # Find which metric this file is for
            for metric_type, required_cols in key_columns.items():
                if metric_type in csv_file.lower():
                    missing_cols = [col for col in required_cols if col not in df.columns]
                    if missing_cols:
                        print(f"  ⚠️ Missing expected columns: {missing_cols}")
                    break
                    
        except Exception as e:
            print(f"\n{csv_file}: ✗ Error reading file: {e}")
    
    # Test import
    print("\n4. TESTING MODULE IMPORT:")
    print("-" * 40)
    
    try:
        sys.path.insert(0, os.getcwd())
        from metrics.cio import CIO_METRICS, get_available_metrics
        print("✓ Successfully imported CIO metrics module")
        print(f"  Available functions: {list(CIO_METRICS.keys())}")
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    # Provide recommendations
    print("\n5. RECOMMENDATIONS:")
    print("-" * 40)
    
    # Check if we need to rename files
    rename_needed = False
    for expected in expected_files:
        if expected not in csv_files:
            rename_needed = True
            break
    
    if rename_needed:
        print("⚠️ File naming issue detected. You need to rename some files.")
        print("\nRun the fix_file_names() function below to automatically fix this.")
    else:
        print("✓ All expected files are present")
    
    return csv_files, expected_files

def fix_file_names():
    """Fix file naming issues by creating properly named copies"""
    
    print("\n" + "=" * 60)
    print("FIXING FILE NAMES")
    print("=" * 60)
    
    # Mapping of what we have to what we need
    file_mappings = {
        'app_cost_analysis_dashboard_examples_backup.csv': 'app_cost_analysis_metrics.csv',
        'business_unit_it_spend_examples_backup.csv': 'business_unit_it_spend.csv',
        'digital_transformation_dashboard_examples_backup.csv': 'digital_transformation_metrics.csv',
        'risk_dashboard_metrics_examples_backup.csv': 'risk_metrics.csv',
        'strategic_alignment_dashboard_examples_backup.csv': 'strategic_alignment_metrics.csv',
        # Add more mappings as needed
    }
    
    cio_dir = 'metrics/cio'
    
    for old_name, new_name in file_mappings.items():
        old_path = os.path.join(cio_dir, old_name)
        new_path = os.path.join(cio_dir, new_name)
        
        if os.path.exists(old_path) and not os.path.exists(new_path):
            try:
                # Read the old file
                df = pd.read_csv(old_path)
                # Save with new name
                df.to_csv(new_path, index=False)
                print(f"✓ Created {new_name} from {old_name}")
            except Exception as e:
                print(f"✗ Failed to create {new_name}: {e}")
        elif os.path.exists(new_path):
            print(f"✓ {new_name} already exists")
    
    # Handle vendor metrics specially if needed
    if not os.path.exists(os.path.join(cio_dir, 'vendor_metrics.csv')):
        # Look for any vendor-related file
        vendor_files = [f for f in os.listdir(cio_dir) if 'vendor' in f.lower() and f.endswith('.csv')]
        if vendor_files:
            old_path = os.path.join(cio_dir, vendor_files[0])
            new_path = os.path.join(cio_dir, 'vendor_metrics.csv')
            try:
                df = pd.read_csv(old_path)
                df.to_csv(new_path, index=False)
                print(f"✓ Created vendor_metrics.csv from {vendor_files[0]}")
            except Exception as e:
                print(f"✗ Failed to create vendor_metrics.csv: {e}")

if __name__ == "__main__":
    # Run diagnostic
    csv_files, expected_files = diagnose_cio_metrics()
    
    # Ask if user wants to fix issues
    print("\n" + "=" * 60)
    response = input("\nWould you like to automatically fix file naming issues? (y/n): ")
    
    if response.lower() == 'y':
        fix_file_names()
        print("\n✅ File fixing complete. Please restart your dashboard.")
    else:
        print("\nTo manually fix, ensure these files exist in metrics/cio/:")
        for f in expected_files:
            print(f"  - {f}")
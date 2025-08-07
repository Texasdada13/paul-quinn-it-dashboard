"""
Simple ETL script for vendor data
This script reads Excel files and prepares them for Power BI
"""

import pandas as pd
import os
from datetime import datetime

# Get the path to your data folder
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
data_folder = os.path.join(project_root, "02_Data")

def read_vendor_data(filename):
    """Read vendor data from Excel file"""
    file_path = os.path.join(data_folder, "raw", filename)
    print(f"Reading: {file_path}")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Loaded {len(df)} vendors")
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        print(f"Please put your Excel file in: {os.path.join(data_folder, 'raw')}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def clean_vendor_data(df):
    """Clean and standardize vendor data"""
    print("Cleaning data...")
    
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Add processing timestamp
    df['processed_date'] = datetime.now()
    
    # Remove duplicates
    original_count = len(df)
    df = df.drop_duplicates()
    if len(df) < original_count:
        print(f"Removed {original_count - len(df)} duplicate rows")
    
    return df

def save_for_powerbi(df, output_name):
    """Save cleaned data for Power BI"""
    output_path = os.path.join(data_folder, "processed", f"{output_name}.csv")
    
    # Create processed folder if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Saved to: {output_path}")
    print(f"You can now import this into Power BI!")
    
    return output_path

# Run the ETL process
if __name__ == "__main__":
    print("Paul Quinn Vendor ETL Process\n")
    
    # Try to read vendor data
    vendors = read_vendor_data("vendors.xlsx")
    
    if vendors is not None:
        # Clean the data
        clean_vendors = clean_vendor_data(vendors)
        
        # Save for Power BI
        output_file = save_for_powerbi(clean_vendors, "clean_vendors")
        
        print("\nETL Complete! Next steps:")
        print("1. Open Power BI Desktop")
        print("2. Get Data -> Text/CSV")
        print(f"3. Browse to: {output_file}")
        print("4. Load and create your visualizations!")
    else:
        print("\nNo vendor data found.")
        print("Please add 'vendors.xlsx' to the '02_Data/raw' folder")

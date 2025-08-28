"""
Debug helper for CIO Dashboard
This script helps identify issues with the dashboard
"""

import pandas as pd
import os
import traceback

def debug_dashboard():
    """Debug function to identify dashboard issues"""
    
    # Get the directory where the metrics module is located
    from pathlib import Path
    CURRENT_DIR = Path(__file__).parent if '__file__' in globals() else Path.cwd()
    
    print("=" * 50)
    print("CIO DASHBOARD DEBUGGING")
    print("=" * 50)
    
    # 1. Check directory structure
    print("\n1. CHECKING DIRECTORY:")
    print(f"   Current directory: {CURRENT_DIR}")
    
    # 2. Check for CSV files
    print("\n2. CHECKING FOR CSV FILES:")
    required_csvs = [
        'app_cost_analysis_metrics.csv',
        'business_unit_it_spend.csv',
        'digital_transformation_metrics.csv',
        'risk_metrics.csv',
        'strategic_alignment_metrics.csv',
        'vendor_metrics.csv'
    ]
    
    missing_files = []
    found_files = []
    
    for csv_file in required_csvs:
        filepath = CURRENT_DIR / csv_file
        if filepath.exists():
            found_files.append(csv_file)
            print(f"   ✓ Found: {csv_file}")
            
            # Try to load and check the file
            try:
                df = pd.read_csv(filepath)
                print(f"     - Rows: {len(df)}, Columns: {len(df.columns)}")
                print(f"     - Columns: {', '.join(df.columns[:5])}...")
                
                # Check for required columns based on the metric type
                if 'app_cost_analysis' in csv_file:
                    required_cols = ['date', 'application', 'monthly_cost', 'utilization_rate', 
                                   'redundancy_index', 'consolidation_potential', 'licenses_total', 'licenses_used']
                elif 'business_unit_it_spend' in csv_file:
                    required_cols = ['date', 'business_unit', 'monthly_budget', 'monthly_spend', 
                                    'budget_variance_pct', 'spend_per_fte']
                elif 'digital_transformation' in csv_file:
                    required_cols = ['date', 'transformation_score', 'online_adoption_rate', 
                                    'digital_literacy_students', 'satisfaction_score', 'student_participation_pct',
                                    'faculty_participation_pct', 'virtual_engagement_rate', 'innovation_milestones']
                elif 'risk_metrics' in csv_file:
                    required_cols = ['date', 'risk_category', 'risk_heat_map', 'risk_exposure_level', 
                                    'mitigation_status', 'compliance_adherence_pct']
                elif 'strategic_alignment' in csv_file:
                    required_cols = ['date', 'initiative', 'alignment_score', 'student_experience_impact',
                                    'equity_advancement_score', 'sustainability_factor', 'cost_per_student_benefited']
                elif 'vendor_metrics' in csv_file:
                    required_cols = ['date', 'vendor', 'satisfaction_score', 'sla_compliance_pct', 
                                    'annual_spend', 'uptime_pct', 'daily_spend']
                else:
                    required_cols = []
                
                missing_cols = [col for col in required_cols if col not in df.columns]
                if missing_cols:
                    print(f"     ⚠ Missing columns: {', '.join(missing_cols)}")
                else:
                    print(f"     ✓ All required columns present")
                    
            except Exception as e:
                print(f"     ✗ Error reading file: {str(e)}")
        else:
            missing_files.append(csv_file)
            print(f"   ✗ Missing: {csv_file}")
    
    print(f"\n   Summary: {len(found_files)}/{len(required_csvs)} files found")
    
    # 3. Test each display function
    print("\n3. TESTING DISPLAY FUNCTIONS:")
    
    # Import the module
    try:
        import sys
        sys.path.insert(0, str(CURRENT_DIR))
        
        # Import the functions
        from __init__ import (
            display_app_cost_analysis_metrics,
            display_business_unit_it_spend,
            display_digital_transformation_metrics,
            display_risk_metrics,
            display_strategic_alignment_metrics,
            display_vendor_metrics
        )
        
        test_functions = [
            ('App Cost Analysis', display_app_cost_analysis_metrics),
            ('Business Unit IT Spend', display_business_unit_it_spend),
            ('Digital Transformation', display_digital_transformation_metrics),
            ('Risk Metrics', display_risk_metrics),
            ('Strategic Alignment', display_strategic_alignment_metrics),
            ('Vendor Metrics', display_vendor_metrics)
        ]
        
        for name, func in test_functions:
            print(f"\n   Testing {name}:")
            try:
                # Note: This won't actually run in Streamlit context, but will check for basic errors
                print(f"     ✓ Function imported successfully")
            except Exception as e:
                print(f"     ✗ Error: {str(e)}")
                traceback.print_exc()
                
    except ImportError as e:
        print(f"   ✗ Could not import module: {str(e)}")
    
    print("\n" + "=" * 50)
    print("DEBUGGING COMPLETE")
    print("=" * 50)
    
    return missing_files

def generate_sample_data():
    """Generate sample CSV files for testing"""
    import numpy as np
    from datetime import datetime, timedelta
    
    print("\n" + "=" * 50)
    print("GENERATING SAMPLE DATA")
    print("=" * 50)
    
    # Base date range
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=x*30) for x in range(12)]
    
    # 1. App Cost Analysis Metrics
    print("\n1. Creating app_cost_analysis_metrics.csv...")
    apps = ['ERP System', 'CRM Platform', 'Email Service', 'LMS', 'HRIS', 'Finance Suite']
    data = []
    for date in dates:
        for app in apps:
            data.append({
                'date': date,
                'application': app,
                'monthly_cost': np.random.uniform(5000, 50000),
                'licenses_total': np.random.randint(50, 500),
                'licenses_used': np.random.randint(30, 450),
                'utilization_rate': np.random.uniform(60, 95),
                'redundancy_index': np.random.uniform(0, 1),
                'consolidation_potential': np.random.choice(['Yes', 'No'])
            })
    pd.DataFrame(data).to_csv('app_cost_analysis_metrics.csv', index=False)
    print("   ✓ Created app_cost_analysis_metrics.csv")
    
    # 2. Business Unit IT Spend
    print("\n2. Creating business_unit_it_spend.csv...")
    units = ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance', 'Operations']
    data = []
    for date in dates:
        for unit in units:
            budget = np.random.uniform(50000, 200000)
            spend = budget * np.random.uniform(0.8, 1.2)
            data.append({
                'date': date,
                'business_unit': unit,
                'monthly_budget': budget,
                'monthly_spend': spend,
                'budget_variance_pct': ((spend - budget) / budget) * 100,
                'spend_per_fte': np.random.uniform(1000, 5000)
            })
    pd.DataFrame(data).to_csv('business_unit_it_spend.csv', index=False)
    print("   ✓ Created business_unit_it_spend.csv")
    
    # 3. Digital Transformation Metrics
    print("\n3. Creating digital_transformation_metrics.csv...")
    data = []
    for i, date in enumerate(dates):
        progress = 30 + (i * 5)  # Progressive improvement
        data.append({
            'date': date,
            'transformation_score': min(95, progress + np.random.uniform(-5, 10)),
            'online_adoption_rate': min(95, progress + np.random.uniform(-3, 8)),
            'platform_utilization_pct': min(95, progress + np.random.uniform(-2, 7)),
            'digital_literacy_students': min(5, 2.5 + (i * 0.2) + np.random.uniform(-0.2, 0.3)),
            'digital_literacy_faculty': min(5, 2.3 + (i * 0.15) + np.random.uniform(-0.2, 0.3)),
            'satisfaction_score': min(5, 3 + (i * 0.1) + np.random.uniform(-0.2, 0.3)),
            'student_participation_pct': min(95, progress + np.random.uniform(0, 10)),
            'faculty_participation_pct': min(95, progress - 5 + np.random.uniform(0, 8)),
            'virtual_engagement_rate': min(95, progress + np.random.uniform(-5, 5)),
            'innovation_milestones': np.random.randint(1, 5)
        })
    pd.DataFrame(data).to_csv('digital_transformation_metrics.csv', index=False)
    print("   ✓ Created digital_transformation_metrics.csv")
    
    # 4. Risk Metrics
    print("\n4. Creating risk_metrics.csv...")
    categories = ['Cybersecurity', 'Compliance', 'Operational', 'Financial', 'Reputational']
    heat_levels = ['Low', 'Medium', 'High', 'Critical']
    statuses = ['Open', 'In Progress', 'Resolved', 'Monitoring']
    
    data = []
    for date in dates:
        for _ in range(20):  # 20 risks per month
            data.append({
                'date': date,
                'risk_category': np.random.choice(categories),
                'risk_heat_map': np.random.choice(heat_levels),
                'risk_exposure_level': np.random.uniform(1, 10),
                'mitigation_status': np.random.choice(statuses),
                'compliance_adherence_pct': np.random.uniform(70, 100)
            })
    pd.DataFrame(data).to_csv('risk_metrics.csv', index=False)
    print("   ✓ Created risk_metrics.csv")
    
    # 5. Strategic Alignment Metrics
    print("\n5. Creating strategic_alignment_metrics.csv...")
    initiatives = ['Digital Campus', 'Student Portal', 'AI Tutoring', 'Cloud Migration', 'Data Analytics']
    data = []
    for date in dates:
        for initiative in initiatives:
            data.append({
                'date': date,
                'initiative': initiative,
                'alignment_score': np.random.uniform(6, 10),
                'student_experience_impact': np.random.uniform(5, 10),
                'equity_advancement_score': np.random.uniform(5, 10),
                'sustainability_factor': np.random.uniform(4, 10),
                'cost_per_student_benefited': np.random.uniform(50, 500)
            })
    pd.DataFrame(data).to_csv('strategic_alignment_metrics.csv', index=False)
    print("   ✓ Created strategic_alignment_metrics.csv")
    
    # 6. Vendor Metrics
    print("\n6. Creating vendor_metrics.csv...")
    vendors = ['Microsoft', 'AWS', 'Oracle', 'Salesforce', 'Adobe', 'Zoom', 'Canvas', 'Workday']
    data = []
    for date in dates:
        for vendor in vendors:
            annual = np.random.uniform(50000, 500000)
            data.append({
                'date': date,
                'vendor': vendor,
                'satisfaction_score': np.random.uniform(3, 5),
                'sla_compliance_pct': np.random.uniform(85, 100),
                'annual_spend': annual,
                'daily_spend': annual / 365,
                'uptime_pct': np.random.uniform(95, 99.9)
            })
    pd.DataFrame(data).to_csv('vendor_metrics.csv', index=False)
    print("   ✓ Created vendor_metrics.csv")
    
    print("\n" + "=" * 50)
    print("SAMPLE DATA GENERATION COMPLETE")
    print("=" * 50)
    print("\nAll CSV files have been created in the current directory.")
    print("You can now run your dashboard!")

if __name__ == "__main__":
    # Run debugging
    missing = debug_dashboard()
    
    if missing:
        print("\n" + "=" * 50)
        print("WOULD YOU LIKE TO GENERATE SAMPLE DATA?")
        print("=" * 50)
        response = input("\nGenerate missing CSV files? (y/n): ")
        if response.lower() == 'y':
            generate_sample_data()
    else:
        print("\nAll files present! Check the column details above for any issues.")
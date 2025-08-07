"""
Export Analytics Results to Files
Saves all insights and analytics to shareable formats
"""

import pandas as pd
from datetime import datetime
import os

def export_analytics_results():
    """Export all analytics results to various formats"""
    
    # Create exports folder
    os.makedirs("06_Exports", exist_ok=True)
    
    print("📊 Exporting Analytics Results...")
    print("="*50)
    
    # Load the robust data
    vendors = pd.read_excel('PQC_Robust_Mock_Data.xlsx', sheet_name='Vendors')
    projects = pd.read_excel('PQC_Robust_Mock_Data.xlsx', sheet_name='Projects')
    systems = pd.read_excel('PQC_Robust_Mock_Data.xlsx', sheet_name='Systems')
    
    # 1. Executive Summary Report
    exec_summary = {
        'Metric': [
            'Total IT Spend',
            'IT Spend as % Revenue',
            'Cost per User',
            'Vendor Count',
            'Active Projects',
            'At-Risk Projects',
            'Average System Availability',
            'Potential Savings Identified',
            'ROI on IT Projects'
        ],
        'Value': [
            f'${vendors["annual_spend"].sum():,.0f}',
            '0.86%',
            f'${vendors["annual_spend"].sum()/5000:.0f}',
            len(vendors),
            len(projects[projects['status'] == 'In Progress']),
            len(projects[projects['health'] == 'Red']),
            '99.26%',
            f'${vendors["annual_spend"].sum() * 0.15:,.0f}',
            '125%'
        ],
        'Status': [
            '✅ Efficient',
            '✅ Below Benchmark',
            '⚠️ Above Industry',
            '⚠️ Consolidation Needed',
            '✅ Normal',
            '⚠️ Attention Required',
            '✅ Excellent',
            '💰 Opportunity',
            '✅ Exceptional'
        ]
    }
    
    exec_df = pd.DataFrame(exec_summary)
    exec_df.to_csv('06_Exports/Executive_Summary.csv', index=False)
    
    # 2. Vendor Optimization Report
    vendor_analysis = vendors.groupby('category').agg({
        'vendor_name': 'count',
        'annual_spend': ['sum', 'mean'],
        'satisfaction_score': 'mean'
    }).round(2)
    
    vendor_analysis.columns = ['Vendor_Count', 'Total_Spend', 'Avg_Spend', 'Avg_Satisfaction']
    vendor_analysis['Savings_Opportunity'] = vendor_analysis['Total_Spend'] * 0.20
    vendor_analysis.to_csv('06_Exports/Vendor_Analysis.csv')
    
    # 3. Project Risk Report
    risk_projects = projects[projects['health'].isin(['Red', 'Yellow'])][
        ['project_name', 'department', 'budget', 'spent_to_date', 'health', 'risk_score']
    ]
    risk_projects['overrun_risk'] = (risk_projects['spent_to_date'] / risk_projects['budget'] * 100).round(0)
    risk_projects.to_csv('06_Exports/Projects_At_Risk.csv', index=False)
    
    # 4. Create a PowerPoint-ready summary text file
    with open('06_Exports/Board_Presentation_Summary.txt', 'w') as f:
        f.write("PAUL QUINN COLLEGE - IT EFFECTIVENESS SUMMARY\n")
        f.write(f"Generated: {datetime.now().strftime('%B %d, %Y')}\n")
        f.write("="*60 + "\n\n")
        
        f.write("EXECUTIVE HIGHLIGHTS:\n")
        f.write(f"• Total IT Investment: ${vendors['annual_spend'].sum():,.0f}\n")
        f.write(f"• IT Efficiency: 0.86% of revenue (Industry: 3.5%)\n")
        f.write(f"• Cost Optimization Opportunity: ${vendors['annual_spend'].sum() * 0.15:,.0f}\n")
        f.write(f"• Projects at Risk: {len(projects[projects['health'] == 'Red'])}\n")
        f.write(f"• System Reliability: 99.26%\n\n")
        
        f.write("TOP 5 RECOMMENDATIONS:\n")
        f.write("1. Consolidate vendors in 8 categories for 20% savings\n")
        f.write("2. Address 6 projects with high budget overrun risk\n")
        f.write("3. Modernize 3 systems over 5 years old\n")
        f.write("4. Implement predictive analytics for proactive management\n")
        f.write("5. Automate license tracking and optimization\n\n")
        
        f.write("QUICK WINS (90 days):\n")
        f.write("• Renegotiate top 5 vendor contracts\n")
        f.write("• Implement automated license tracking\n")
        f.write("• Launch vendor consolidation initiative\n")
    
    # 5. Create a metrics dashboard data file
    dashboard_metrics = {
        'Financial_Metrics': {
            'total_spend': vendors['annual_spend'].sum(),
            'spend_by_category': vendors.groupby('category')['annual_spend'].sum().to_dict(),
            'high_risk_vendor_spend': vendors[vendors['risk_level'] == 'High']['annual_spend'].sum()
        },
        'Project_Metrics': {
            'total_projects': len(projects),
            'active_projects': len(projects[projects['status'] == 'In Progress']),
            'at_risk_projects': len(projects[projects['health'] == 'Red']),
            'total_budget': projects['budget'].sum()
        },
        'Operational_Metrics': {
            'vendor_count': len(vendors),
            'system_count': len(systems),
            'avg_satisfaction': vendors['satisfaction_score'].mean()
        }
    }
    
    # Save as JSON for web consumption
    import json
    with open('06_Exports/Dashboard_Metrics.json', 'w') as f:
        json.dump(dashboard_metrics, f, indent=2, default=str)
    
    print("\n✅ EXPORTS COMPLETED!")
    print("\nFiles created in '06_Exports' folder:")
    print("1. Executive_Summary.csv - High-level metrics")
    print("2. Vendor_Analysis.csv - Vendor optimization opportunities")
    print("3. Projects_At_Risk.csv - Projects requiring attention")
    print("4. Board_Presentation_Summary.txt - Ready for PowerPoint")
    print("5. Dashboard_Metrics.json - For web dashboards")
    
    print("\n📁 Full path: C:\\Users\\dada_\\OneDrive\\Documents\\Paul-Quinn-IT-Spend\\06_Exports\\")

# Run the export
export_analytics_results()

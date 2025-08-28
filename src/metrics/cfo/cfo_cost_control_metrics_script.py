# Creating a comprehensive breakdown for CFO IT Cost Control, Compliance, and ROI metrics
import pandas as pd

# CFO Cost Control Metrics Breakdown
cost_control_metrics = {
    'Metric Category': [
        'Budget Variance Analysis',
        'Budget Variance Analysis', 
        'Budget Variance Analysis',
        'License Optimization',
        'License Optimization',
        'License Optimization',
        'Vendor Cost Management',
        'Vendor Cost Management',
        'Vendor Cost Management',
        'ROI Measurement',
        'ROI Measurement',
        'ROI Measurement',
        'Compliance Tracking',
        'Compliance Tracking',
        'Compliance Tracking',
        'Cost Forecasting',
        'Cost Forecasting',
        'Cost Forecasting'
    ],
    'Specific Metric': [
        'Budget vs Actual Spend Variance',
        'Monthly/Quarterly Spend Trend',
        'Cost per Project/Department',
        'License Utilization Rate',
        'Unused License Cost',
        'Cost per Active User',
        'Vendor Spend Concentration Risk',
        'Contract Renewal Cost Analysis',
        'Vendor Performance Score',
        'IT Investment ROI',
        'Cost Savings from Initiatives',
        'Payback Period Tracking',
        'Audit Compliance Score',
        'Regulatory Compliance Cost',
        'Non-compliance Risk Exposure',
        'Annual IT Spend Forecast',
        'Cost Growth Rate Prediction',
        'Budget Allocation Optimization'
    ],
    'Formula/Calculation': [
        '((Actual Spend - Budgeted Amount) / Budgeted Amount) * 100',
        'Month-over-month % change in spend',
        'Total IT Spend / Number of Projects or Departments',
        '(Active Users / Total Licensed Seats) * 100',
        'Total License Cost - (Active Users * Cost per License)',
        'Total License Cost / Number of Active Users',
        '(Top 3 Vendor Spend / Total Vendor Spend) * 100',
        '(Renewal Cost - Current Cost) / Current Cost * 100',
        'Weighted average of satisfaction, SLA compliance, cost efficiency',
        '(Financial Benefits - IT Investment Cost) / IT Investment Cost * 100',
        'Previous Year Costs - Current Year Costs for same services',
        'IT Investment Cost / Annual Savings Generated',
        'Met Requirements / Total Requirements * 100',
        'Total cost of compliance activities and tools',
        'Potential fines + remediation costs for non-compliance',
        'Historical spend trend + planned initiatives cost',
        'Year-over-year IT spend growth percentage',
        'Budget allocation based on ROI and strategic priorities'
    ],
    'Target/Benchmark': [
        '±5% variance acceptable, <10% concerning',
        '<15% growth year-over-year for mature organizations',
        'Benchmark against peer institutions',
        '>85% utilization rate considered optimal',
        '<10% of total license spend',
        'Minimize while maintaining service quality',
        '<60% concentration risk (diversification)',
        'Target <5% annual increase',
        '>4.0/5.0 satisfaction score',
        '>20% ROI for strategic IT investments',
        'Target 5-10% annual cost savings',
        '<3 years payback for major investments',
        '>95% compliance score',
        '<2% of total IT budget',
        'Minimize through proactive compliance',
        '±10% accuracy compared to actual spend',
        'Align with institutional growth rate',
        'Focus 60% on operations, 40% on innovation'
    ],
    'Data Sources': [
        'Budget system, expense tracking, project management tools',
        'Financial systems, monthly expense reports',
        'Project accounting, departmental cost allocation',
        'License management systems, user activity logs',
        'License management, usage analytics',
        'License costs, user management systems',
        'Vendor management, procurement systems',
        'Contract management, vendor negotiations',
        'Vendor scorecards, SLA monitoring, satisfaction surveys',
        'Financial systems, project outcomes measurement',
        'Year-over-year cost analysis, efficiency metrics',
        'Investment tracking, benefits realization',
        'Compliance audits, regulatory checklists',
        'Compliance tool costs, audit fees, staff time',
        'Risk assessments, regulatory penalty databases',
        'Historical data, planned projects, inflation rates',
        'Multi-year spend analysis, trend extrapolation',
        'Strategic planning, ROI analysis, priority matrices'
    ],
    'Alert Thresholds': [
        '>10% over budget, >5% under budget',
        '>20% month-over-month increase',
        'Outlier departments spending >150% of average',
        '<80% utilization rate',
        '>15% unused license cost',
        'Increasing cost per user trends',
        '>70% vendor concentration',
        '>10% renewal increase',
        '<3.5/5.0 satisfaction score',
        '<15% ROI on major investments',
        'Negative cost savings trends',
        '>5 year payback period',
        '<90% compliance score',
        '>3% of IT budget on compliance',
        'High risk compliance gaps identified',
        '>15% forecast variance',
        '>25% annual growth rate',
        'Imbalanced allocation ratios'
    ]
}

df_cost_control = pd.DataFrame(cost_control_metrics)

# Display the breakdown
print("CFO IT COST CONTROL, COMPLIANCE & ROI METRICS BREAKDOWN")
print("=" * 60)
print()

# Group by category and display
for category in df_cost_control['Metric Category'].unique():
    category_data = df_cost_control[df_cost_control['Metric Category'] == category]
    print(f"\n🎯 {category.upper()}")
    print("-" * 40)
    
    for idx, row in category_data.iterrows():
        print(f"\n📊 {row['Specific Metric']}")
        print(f"   Formula: {row['Formula/Calculation']}")
        print(f"   Target: {row['Target/Benchmark']}")
        print(f"   Data Source: {row['Data Sources']}")
        print(f"   Alert: {row['Alert Thresholds']}")

# Save to CSV for easy reference
df_cost_control.to_csv('cfo_cost_control_metrics.csv', index=False)
print(f"\n\n✅ Detailed breakdown saved to 'cfo_cost_control_metrics.csv'")
print(f"📋 Total metrics defined: {len(df_cost_control)}")
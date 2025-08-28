# Let's analyze your current code and data structure against the required CFO metrics
import pandas as pd

# Your current data structure from app.py
current_data = {
    'projects': ['Project Name', 'Status', 'Budget', 'Spent', 'Completion', 'Risk Level', 'End Date'],
    'vendors': ['Vendor', 'Annual Spend', 'Contract End', 'Satisfaction'],
    'usage': ['System', 'Active Users', 'Total Licenses', 'Utilization %']
}

# Required CFO metrics from your query
required_metrics = [
    "Budget vs. Actual Spend Analysis with variance alerts",
    "Total IT Spend breakdown by project, vendor, and functional area with 3-year historical trends", 
    "Cost per Business Unit/Project allocation",
    "Vendor spend optimization - underutilized licenses and overlapping subscriptions",
    "Contract expiration alerts",
    "Benchmarking against peer HBCUs",
    "ROI calculations for IT investments tied to student success metrics",
    "Compliance reporting capabilities for grant funding requirements"
]

# Analysis of what's covered vs missing
coverage_analysis = {
    'Required Metric': required_metrics,
    'Currently Addressed': [
        'PARTIALLY - You have Budget and Spent fields but no variance calculation or alerts',
        'PARTIALLY - You have vendor spend but missing 3-year trends and functional area breakdown',
        'MISSING - No business unit/department allocation in current data',
        'PARTIALLY - You have utilization % but missing license optimization analysis',
        'MISSING - You have Contract End dates but no alert mechanism',
        'MISSING - No peer HBCU benchmarking data or functionality',
        'MISSING - No ROI calculations or student success metrics linkage',
        'MISSING - No compliance reporting or grant funding tracking'
    ],
    'Data Gaps': [
        'Need variance calculation, alert thresholds, historical budget data',
        'Need 3-year historical data, functional area categories, trend analysis',
        'Need department/business unit fields, cost allocation logic',
        'Need unused license cost, overlapping subscription detection',
        'Need alert system, renewal timeline tracking',
        'Need peer institution data, benchmarking framework',
        'Need ROI calculation fields, student success outcome metrics',
        'Need compliance status fields, grant requirements tracking'
    ],
    'Implementation Priority': [
        'HIGH - Core CFO need',
        'HIGH - Essential for reporting',
        'MEDIUM - Important for accountability',
        'HIGH - Significant cost savings opportunity',
        'MEDIUM - Risk management',
        'LOW - Nice to have for justification',
        'MEDIUM - Strategic value demonstration',
        'HIGH - Critical for HBCU funding'
    ]
}

df_analysis = pd.DataFrame(coverage_analysis)

print("METRIC COVERAGE ANALYSIS FOR YOUR CURRENT DASHBOARD")
print("=" * 60)
print()

for idx, row in df_analysis.iterrows():
    print(f"📊 {row['Required Metric']}")
    print(f"   Status: {row['Currently Addressed']}")
    print(f"   Gaps: {row['Data Gaps']}")
    print(f"   Priority: {row['Implementation Priority']}")
    print()

# Summary statistics
total_metrics = len(required_metrics)
fully_addressed = sum(1 for status in df_analysis['Currently Addressed'] if status.startswith('YES'))
partially_addressed = sum(1 for status in df_analysis['Currently Addressed'] if status.startswith('PARTIALLY'))
missing = sum(1 for status in df_analysis['Currently Addressed'] if status.startswith('MISSING'))

print("COVERAGE SUMMARY")
print("=" * 30)
print(f"📈 Total Required Metrics: {total_metrics}")
print(f"✅ Fully Addressed: {fully_addressed} ({fully_addressed/total_metrics*100:.1f}%)")
print(f"🟡 Partially Addressed: {partially_addressed} ({partially_addressed/total_metrics*100:.1f}%)")
print(f"❌ Missing: {missing} ({missing/total_metrics*100:.1f}%)")

# High priority gaps
high_priority_gaps = df_analysis[df_analysis['Implementation Priority'] == 'HIGH']
print(f"\n🚨 HIGH PRIORITY GAPS TO ADDRESS ({len(high_priority_gaps)} items):")
for idx, row in high_priority_gaps.iterrows():
    print(f"   • {row['Required Metric']}")

df_analysis.to_csv('cfo_metric_coverage_analysis.csv', index=False)
print(f"\n💾 Analysis saved to 'cfo_metric_coverage_analysis.csv'")
# Let me fix the high priority analysis
import pandas as pd

# Reload and correct the analysis
coverage_analysis = {
    'Required Metric': [
        "Budget vs. Actual Spend Analysis with variance alerts",
        "Total IT Spend breakdown by project, vendor, and functional area with 3-year historical trends", 
        "Cost per Business Unit/Project allocation",
        "Vendor spend optimization - underutilized licenses and overlapping subscriptions",
        "Contract expiration alerts",
        "Benchmarking against peer HBCUs",
        "ROI calculations for IT investments tied to student success metrics",
        "Compliance reporting capabilities for grant funding requirements"
    ],
    'Currently Addressed': [
        'PARTIALLY',
        'PARTIALLY', 
        'MISSING',
        'PARTIALLY',
        'MISSING',
        'MISSING',
        'MISSING',
        'MISSING'
    ],
    'Implementation Priority': [
        'HIGH',
        'HIGH',
        'MEDIUM', 
        'HIGH',
        'MEDIUM',
        'LOW',
        'MEDIUM',
        'HIGH'
    ]
}

df_analysis = pd.DataFrame(coverage_analysis)

# Identify high priority gaps correctly
high_priority_items = df_analysis[df_analysis['Implementation Priority'] == 'HIGH']
high_priority_gaps = high_priority_items[high_priority_items['Currently Addressed'].isin(['MISSING', 'PARTIALLY'])]

print("🚨 HIGH PRIORITY ITEMS THAT NEED WORK:")
print("=" * 45)
for idx, row in high_priority_gaps.iterrows():
    status_icon = "🟡" if row['Currently Addressed'] == 'PARTIALLY' else "❌"
    print(f"{status_icon} {row['Required Metric']}")
    print(f"   Current Status: {row['Currently Addressed']}")

print(f"\n📊 SUMMARY:")
print(f"   • {len(high_priority_gaps)} HIGH priority items need attention")
print(f"   • {len(df_analysis[df_analysis['Currently Addressed'] == 'MISSING'])} metrics completely missing")
print(f"   • {len(df_analysis[df_analysis['Currently Addressed'] == 'PARTIALLY'])} metrics partially implemented")

# What needs to be added to your current data structure
print(f"\n🔧 IMMEDIATE DATA STRUCTURE ENHANCEMENTS NEEDED:")
print("=" * 50)

enhancements = [
    "Add variance calculation fields (Budget - Spent, % variance)",
    "Add historical data tables (3-year spend trends)",
    "Add functional area/department categorization",
    "Add license cost fields and unused license calculations", 
    "Add contract alert mechanisms and renewal tracking",
    "Add compliance status and grant funding fields",
    "Add ROI calculation fields and student success metrics"
]

for i, enhancement in enumerate(enhancements, 1):
    print(f"{i}. {enhancement}")

print(f"\n💡 RECOMMENDATION:")
print("Focus on the 4 HIGH priority items first:")
print("1. Budget variance calculations and alerts")
print("2. Historical spend trends and functional area breakdown") 
print("3. License optimization analysis")
print("4. Compliance reporting for grant funding")
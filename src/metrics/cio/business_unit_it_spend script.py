import pandas as pd
import numpy as np

# Define metrics for IT spend by business unit to identify outliers and shape demand
unit_metrics = [
    ('Total IT Spend', 'Total annual IT expenditures by business unit'),
    ('Operational Spend', 'Annual IT spending for regular operations per unit'),
    ('Project Spend', 'Annual IT spending on major initiatives/projects per unit'),
    ('Spend Per FTE', 'Total IT spend divided by full-time equivalent staff/faculty in the unit'),
    ('Annual Spend Growth Rate', 'Year-over-year change in IT spend for the unit'),
    ('Budget Variance', 'Difference between actual and budgeted spend (percent)'),
    ('Capital vs Operational Ratio', 'Proportion of investment spend to operating costs'),
    ('Allocation to Innovation', 'Percent of unit IT budget dedicated to innovation/digital'),
    ('Demand Driver Index', 'Index score based on campus usage, new programs, strategic drivers'),
    ('Cost Efficiency Index', 'Efficiency score based on service delivery/output per dollar'),
    ('High-Cost Outlier Flag', 'Indicator for units above certain spend thresholds'),
    ('Historical Spend Trend', 'Multi-year spend trend (up, down, stable)'),
    ('Proportion of Total IT Budget', 'Percentage of college-wide IT budget allocated to unit'),
    ('Peer Benchmark Spend', 'Comparison of unit’s spend to similar units at other institutions'),
]

business_units = [
    'Academic Affairs', 'Student Affairs', 'IT Operations', 'Finance & Admin',
    'Registrar', 'Institutional Research', 'Library', 'Athletics'
]
np.random.seed(59)
units_example_data = []
for metric, description in unit_metrics:
    for unit in business_units:
        if 'Spend' in metric:
            value = f"${np.random.randint(50000,800000):,}"
        elif 'Variance' in metric or 'Allocation' in metric or 'Ratio' in metric or 'Proportion' in metric or 'Growth' in metric:
            value = f"{np.round(np.random.uniform(-10,50),1)}%"
        elif 'Index' in metric or 'Efficiency' in metric:
            value = np.round(np.random.uniform(0.3,1.0),2)
        elif 'Flag' in metric:
            value = np.random.choice(['Yes','No'])
        elif 'Trend' in metric:
            value = np.random.choice(['Up','Down','Stable'])
        elif 'Peer Benchmark' in metric:
            value = f"{np.round(np.random.uniform(0.7,1.3),2)}x peer"
        else:
            value = 'N/A'
        units_example_data.append((unit, metric, description, value))

unit_dashboard_df = pd.DataFrame(units_example_data, columns=['Business_Unit','Metric','Description','Example'])
unit_dashboard_df.to_csv('business_unit_it_spend_examples.csv', index=False)
print('Business unit IT spend metrics CSV with examples saved.')

# Optional module template
script_unit = '''\n# Business Unit IT Spend Metrics Module\nunit_metric_definitions = [\n    { 'metric': 'Total IT Spend', 'description': 'Total annual IT expenditures by business unit' },\n    { 'metric': 'High-Cost Outlier Flag', 'description': 'Indicator for units above spend threshold' },\n    # ... continued for all metrics ...\n]\n\nimport pandas as pd\n\n# Example business unit IT spend data\nunit_records = [\n    ('IT Operations', 'Total IT Spend', '$425,000'),\n    ('Academic Affairs', 'High-Cost Outlier Flag', 'Yes'),\n]\n\ndf_unit = pd.DataFrame(unit_records, columns=['Business_Unit','Metric','Value'])\n\n# Flag high-cost outlier units\ndef flag_high_cost_units(df):\n    return df[(df['Metric'] == 'High-Cost Outlier Flag') & (df['Value'] == 'Yes')]\n\n# Usage\nhigh_costs = flag_high_cost_units(df_unit)\nprint(high_costs)\n'''
with open('business_unit_it_spend_module.py', 'w') as f:
    f.write(script_unit)
print('Business unit IT spend metrics module Python script saved.')
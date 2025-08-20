
# HBCU Resource Maximization Metrics Module
hbcu_metric_definitions = [
    { 'metric': 'Instructional Spending Ratio', 'description': 'Instruction spend ÷ total revenue' },
    { 'metric': 'Mission Alignment Index', 'description': 'Degree of equity/mission fit of spend' },
    # ... continued ...
]

import pandas as pd

hbcu_records = [
    ('Instructional Spending Ratio', 'HBCU: 1.20, Private NP: 0.78'),
    ('Mission Alignment Index', 8.9),
]

df_hbcu = pd.DataFrame(hbcu_records, columns=['Metric','Value'])

# Dashboard logic: flag below-benchmark spending ratios
def flag_spending_issues(df):
    below_ratio = df[(df['Metric'] == 'Instructional Spending Ratio') & (df['Value'].str.contains('HBCU')) & (df['Value'].str.extract(r'HBCU: ([0-9.]+)')[0].astype(float) < 1.0)]
    return below_ratio
# Usage
issues = flag_spending_issues(df_hbcu)
print(issues)

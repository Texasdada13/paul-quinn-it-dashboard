
# Application Total Cost Analysis Metrics
cost_metric_definitions = [
    { 'metric': 'Total Cost of Ownership (TCO)', 'description': 'Sum of all costs over lifecycle' },
    { 'metric': 'Utilization Rate (%)', 'description': 'Percent of seats/features in use' },
    # ... continued for all metrics ...
]

import pandas as pd

# Example application cost records
cost_records = [
    ('Office 365', 'Total Cost of Ownership (TCO)', '$85,200'),
    ('Slack', 'Redundancy Index', 0.79),
]

df_cost = pd.DataFrame(cost_records, columns=['Application','Metric','Value'])

# Flag systems with low utilization or high redundancy
def flag_redundant_systems(df):
    rst = df[(df['Metric'] == 'Utilization Rate (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) < 60)]
    red = df[(df['Metric'] == 'Redundancy Index') & (df['Value'] > 0.5)]
    return pd.concat([rst,red])
# Usage
repeats = flag_redundant_systems(df_cost)
print(repeats)

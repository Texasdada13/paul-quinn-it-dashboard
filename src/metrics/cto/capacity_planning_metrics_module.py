
# Capacity Planning & Scaling Metrics Module
capacity_metric_definitions = [
    { 'metric': 'Peak Utilization (%)', 'description': 'Highest recorded usage over interval' },
    { 'metric': 'Scaling Recommendation', 'description': 'Advisory action: scale up/out/maintain' },
    # ... continued for all metrics ...
]

import pandas as pd

capacity_records = [
    ('Core Network', 'Peak Utilization (%)', '94.1%'),
    ('Campus WiFi', 'Scaling Recommendation', 'Scale Up'),
]

df_capacity = pd.DataFrame(capacity_records, columns=['Component','Metric','Value'])

# Dashboard logic: flag components nearing threshold or recommended for scaling
# Utilization >85% or buffer <15%
def flag_scaling_needed(df):
    near_peak = df[(df['Metric'] == 'Peak Utilization (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) > 85)]
    low_buffer = df[(df['Metric'] == 'Current Buffer Capacity (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) < 15)]
    scaling_recommend = df[(df['Metric'] == 'Scaling Recommendation') & (df['Value'].isin(['Scale Up','Scale Out','Investigate Bottleneck']))]
    return pd.concat([near_peak,low_buffer,scaling_recommend])
# Usage
issues = flag_scaling_needed(df_capacity)
print(issues)

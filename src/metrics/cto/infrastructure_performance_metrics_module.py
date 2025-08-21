
# Infrastructure Performance Metrics Module
infra_metric_definitions = [
    { 'metric': 'System Uptime (%)', 'description': 'Percent of time service is operational' },
    { 'metric': 'Error Rate (%)', 'description': 'Percent failed requests' },
    # ... continued for all metrics ...
]

import pandas as pd

infra_records = [
    ('Network', 'System Uptime (%)', '99.95%'),
    ('VPN Gateway', 'Error Rate (%)', '1.2%'),
]

df_infra = pd.DataFrame(infra_records, columns=['Infrastructure','Metric','Value'])

# Flag infra systems with low uptime or high error rates
def flag_low_perf(df):
    low_uptime = df[(df['Metric'] == 'System Uptime (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) < 97)]
    high_error = df[(df['Metric'] == 'Error Rate (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) > 5)]
    return pd.concat([low_uptime,high_error])
# Usage
issues = flag_low_perf(df_infra)
print(issues)

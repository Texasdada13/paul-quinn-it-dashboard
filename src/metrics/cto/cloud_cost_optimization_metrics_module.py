
# Cloud Cost & Resource Optimization Metrics Module
cloud_metric_definitions = [
    { 'metric': 'Resource Utilization (%)', 'description': 'Percent utilization of provisioned resources' },
    { 'metric': 'Right-Sizing Status', 'description': 'Is instance right-sized for workload' },
    # ... continued for all metrics ...
]

import pandas as pd

cloud_records = [
    ('AWS EC2', 'Resource Utilization (%)', '47.9%'),
    ('Zoom Cloud', 'Idle Resource Cost ($)', '$6,400'),
]

df_cloud = pd.DataFrame(cloud_records, columns=['Service','Metric','Value'])

# Flag underutilized or costly cloud resources
def flag_cloud_issues(df):
    # Utilization <60% or Idle cost >5000
    low_util = df[(df['Metric'] == 'Resource Utilization (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) < 60)]
    high_idle = df[(df['Metric'] == 'Idle Resource Cost ($)') & (df['Value'].apply(lambda x: float(x.replace('$','').replace(',','')) if isinstance(x,str) else 0) > 5000)]
    return pd.concat([low_util,high_idle])
# Usage
issues = flag_cloud_issues(df_cloud)
print(issues)
